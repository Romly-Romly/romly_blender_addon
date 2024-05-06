import bpy
import math
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple, Literal



from . import romly_utils










LENGTH_SPECIFICATION_FREE_LENGTH = 'free_length'
LENGTH_SPECIFICATION_COILS = 'coils'










class ROMLYADDON_OT_add_compression_spring(bpy.types.Operator):
	bl_idname = 'romlyaddon.add_compression_spring'
	bl_label = bpy.app.translations.pgettext_iface('Add Compression Spring')
	bl_description = 'Construct a Compression Spring'
	bl_options = {'REGISTER', 'UNDO'}

	# 線径
	val_wire_diameter: FloatProperty(name='Wire Diameter', description='The diameter of the wire', default=1.0, min=0.01, soft_max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)

	# 外径
	val_outer_diameter: FloatProperty(name='Outer Diameter', description='The outer diameter of the spring', default=10.0, min=0.01, soft_max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)

	# ピッチ
	val_pitch: FloatProperty(name='Pitch', description='The pitch of the spring', default=3.0, min=0.01, soft_max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)

	LENGTH_SPECIFICATION_ITEMS = [
		(LENGTH_SPECIFICATION_FREE_LENGTH, 'Free Length', 'Specify the free length of the spring'),
		(LENGTH_SPECIFICATION_COILS, 'Coils', 'Specify the number of coils to determine the spring length'),
	]
	val_length_specification: EnumProperty(name='Length Specification', items=LENGTH_SPECIFICATION_ITEMS, default='free_length')

	# 巻数（自由長と排他）
	val_coils: FloatProperty(name='Coils', description='The number of active coils', default=10, min=0, soft_max=100.0, precision=2, step=1)

	# 自由長（巻数と排他）
	val_free_length: FloatProperty(name='Free Length', description='The free length of the spring. This will be the total height of the spring', default=10, min=0, soft_max=100.0, precision=2, step=1, unit=bpy.utils.units.categories.LENGTH)

	# 座巻
	val_dead_coils_top: FloatProperty(name='Dead Coils (Top)', description='The number of dead coils at the top', default=1, min=0, soft_max=3, precision=2, step=1)
	val_dead_coils_bottom: FloatProperty(name='Dead Coils (Bottom)', description='The number of dead coils at the bottom', default=1, min=0, soft_max=3, precision=2, step=1)

	# 巻き方向
	val_direction: EnumProperty(name='Direction', items=[
		('right', 'Right Hand Wind', 'Make the spring wind direction right hand wind (clockwise)'),
		('left', 'Left Hand Wind', 'Make the spring wind direction left hand wind (counter-clockwise)')], default='right')

	# 端を研削するか
	val_ground_ends: BoolProperty(name='Ground Ends', default=False)

	# 線のセグメント数
	val_wire_segments: IntProperty(name='Wire Segments', description='The number of segments of the wire', default=16, min=3, soft_max=48, max=128, step=1)

	# バネ全体のセグメント数
	val_outer_diameter_segments: IntProperty(name='Outer Diameter Segments', description='The number of segments of the outer diameter', default=32, min=3, soft_max=64, max=128, step=1)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col.prop(self, 'val_wire_diameter')
		col.prop(self, 'val_outer_diameter')
		col.prop(self, 'val_pitch')
		row = col.row(align=True)
		row.prop(self, 'val_direction', expand=True)
		col.prop(self, 'val_ground_ends')
		col.separator()

		row = col.row(align=True)
		row.prop(self, 'val_length_specification', expand=True)
		if self.val_length_specification == LENGTH_SPECIFICATION_COILS:
			s = bpy.app.translations.pgettext_iface('Free Length: {value}').format(value=romly_utils.units_to_string(self.get_free_length(self.val_ground_ends), category=bpy.utils.units.categories.LENGTH))
			row = col.row(align=True)
			row.alignment = 'RIGHT'
			row.label(text=s)
			col.prop(self, 'val_coils')
		else:
			col.prop(self, 'val_free_length')
			top_coils, bottom_coils, coils = self.calc_coils_from_free_length()
			s = bpy.app.translations.pgettext_iface('Active Coils: {value}').format(value=romly_utils.remove_decimal_trailing_zeros(round(coils, 2)))
			row = col.row(align=True)
			row.alignment = 'RIGHT'
			row.label(text=s)
		dead_coils = col.column(align=True)
		dead_coils.prop(self, 'val_dead_coils_top')
		dead_coils.prop(self, 'val_dead_coils_bottom')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_wire_segments')
		col.prop(self, 'val_outer_diameter_segments')



	def get_free_length(self, ground_ends: bool = False) -> float:
		active_coil_length = self.val_pitch * self.val_coils
		dead_coil_length_top = self.val_wire_diameter * self.val_dead_coils_top
		dead_coil_length_bottom = self.val_wire_diameter * self.val_dead_coils_bottom
		result = active_coil_length + dead_coil_length_top + dead_coil_length_bottom + self.val_wire_diameter
		if ground_ends:
			result -= self.val_wire_diameter
		return result



	def calc_coils_from_free_length(self) -> tuple[float, float, float]:
		"""
		自由長制限で巻ける座巻数と有効巻数をそれぞれ算出する。

		Returns
		-------
		tuple[float, float, float]
			座巻数（上部）、座巻数（下部）、有効巻数。
		"""
		length_remain = (self.val_free_length + self.val_wire_diameter) if self.val_ground_ends else self.val_free_length

		# 現在の自由長で巻ける、ピッチを考慮しない最大巻数
		max_coils = (length_remain - self.val_wire_diameter) / self.val_wire_diameter
		bottom_coils = min(self.val_dead_coils_bottom, max_coils)
		length_remain -= bottom_coils * self.val_wire_diameter

		# 座巻部分（上部）
		max_coils = (length_remain - self.val_wire_diameter) / self.val_wire_diameter
		top_coils = min(self.val_dead_coils_top, max_coils)
		length_remain -= top_coils * self.val_wire_diameter

		# 有効巻数部分
		coils = max(0, (length_remain - self.val_wire_diameter) / self.val_pitch)

		return top_coils, bottom_coils, coils



	def add_coils(self, vertices, faces, num_vertices: int, coils: float, offset: float):
		if coils <= 0:
			return

		full_rotation = math.floor(coils)
		remain_rotation = coils - full_rotation
		ccw = self.val_direction == 'left'
		for _ in range(full_rotation):
			romly_utils.add_revolved_surface(vertices=vertices, faces=faces, rotation_vertex_count=num_vertices, segments=self.val_outer_diameter_segments, close=True, z_offset=offset, ccw=ccw)
		romly_utils.add_revolved_surface(vertices=vertices, faces=faces, rotation_vertex_count=num_vertices, segments=self.val_outer_diameter_segments, close=True, z_offset=offset, rotation_degree=remain_rotation * 360, ccw=ccw)



	def execute(self, context):

		# 円の頂点群と面を生成
		center_x = self.val_outer_diameter / 2 - self.val_wire_diameter / 2
		if self.val_direction == 'right':
			center_x = -center_x
		vertices = romly_utils.make_circle_vertices(radius=self.val_wire_diameter / 2, num_vertices=self.val_wire_segments, center=(center_x, 0, 0), normal_vector=(0, -1, 0))
		faces = [list(range(len(vertices)))]



		# 回転体を作成
		count = len(vertices)

		if self.val_length_specification == LENGTH_SPECIFICATION_COILS:
			# 巻数で指定する場合。単純にそれぞれの巻数分のコイルを作成していく

			# 座巻部分（下部）
			self.add_coils(vertices, faces, num_vertices=count, coils=self.val_dead_coils_bottom, offset=self.val_wire_diameter)
			# 有効巻数部分
			self.add_coils(vertices, faces, num_vertices=count, coils=self.val_coils, offset=self.val_pitch)
			# 座巻部分（上部）
			self.add_coils(vertices, faces, num_vertices=count, coils=self.val_dead_coils_top, offset=self.val_wire_diameter)
		else:
			top_coils, bottom_coils, coils = self.calc_coils_from_free_length()

			# 座巻部分（下部）
			self.add_coils(vertices, faces, num_vertices=count, coils=bottom_coils, offset=self.val_wire_diameter)
			# 有効巻数部分
			self.add_coils(vertices, faces, num_vertices=count, coils=coils, offset=self.val_pitch)
			# 座巻部分（上部）
			self.add_coils(vertices, faces, num_vertices=count, coils=top_coils, offset=self.val_wire_diameter)



		# 回転体の蓋となる面
		faces.append(list(range(len(vertices) - count, len(vertices))))



		# オブジェクトを作成
		obj = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=vertices, faces=faces))
		bpy.context.collection.objects.link(obj)



		# 端を研削する場合
		if self.val_ground_ends:
			enough_big = self.val_outer_diameter * 2
			cutter = romly_utils.create_box_from_corners(corner1=(-enough_big, -enough_big, 0), corner2=(enough_big, enough_big, -self.val_wire_diameter * 2))
			romly_utils.apply_boolean_object(obj, cutter)
			z = 0
			if self.val_length_specification == LENGTH_SPECIFICATION_COILS:
				z = self.get_free_length(True)
			else:
				z = self.val_free_length
			cutter = romly_utils.create_box_from_corners(corner1=(-enough_big, -enough_big, z), corner2=(enough_big, enough_big, z + self.val_wire_diameter * 2))
			romly_utils.apply_boolean_object(obj, cutter)



		# オブジェクトを3Dカーソル位置へ移動
		obj.location = bpy.context.scene.cursor.location

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}










# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.operator(ROMLYADDON_OT_add_compression_spring.bl_idname, text=bpy.app.translations.pgettext_iface('Add Compression Spring'), icon='MESH_CAPSULE')





classes = [
	ROMLYADDON_OT_add_compression_spring,
]



def register():
	# 翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	# 翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
