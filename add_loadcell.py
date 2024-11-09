import bpy
import math
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple, Literal



from . import romly_utils










class LoadCellSpec(NamedTuple):
	size: tuple[float, float, float]
	thin_part_size: tuple[float, float]
	hole_diameter: float
	center_hole_diameter: float
	hole_distance: float
	hole_bridge_height: float
	screw_hole_distance_a: float
	screw_hole_distance_b: float
	screw_hole_distance_x: float
	screw_hole_front: tuple[str, bool]
	screw_hole_back: tuple[str, bool]



LOADCELL_SPECS = {
	'normal': LoadCellSpec(size=(12.7, 80, 12.7), thin_part_size=(0, 0),
		hole_distance=7, hole_diameter=11, center_hole_diameter=0, hole_bridge_height=0,
		screw_hole_distance_a=40, screw_hole_distance_b=15, screw_hole_distance_x=0,
		screw_hole_front=('m4', True), screw_hole_back=('m5', True)),
	'small': LoadCellSpec(size=(12.7, 75, 12.7), thin_part_size=(0, 0),
		hole_distance=7, hole_diameter=11, center_hole_diameter=0, hole_bridge_height=0,
		screw_hole_distance_a=44, screw_hole_distance_b=10, screw_hole_distance_x=0,
		screw_hole_front=('m4', True), screw_hole_back=('m4', True)),
	'tiny': LoadCellSpec(size=(9, 45, 6), thin_part_size=(0, 0),
		hole_distance=7, hole_diameter=5, center_hole_diameter=3, hole_bridge_height=0,
		screw_hole_distance_a=22, screw_hole_distance_b=(37 - 22) / 2, screw_hole_distance_x=0,
		screw_hole_front=('m3', True), screw_hole_back=('m3', True)),
	'i-shape': LoadCellSpec(size=(12, 47, 6), thin_part_size=(7.5, 34),
		hole_distance=20, hole_diameter=6 - 0.35 * 2, center_hole_diameter=0, hole_bridge_height=2,
		screw_hole_distance_a=40, screw_hole_distance_b=0, screw_hole_distance_x=6,
		screw_hole_front=('m3', False), screw_hole_back=('m3', True)),
}


def create_loadcell(
		size: tuple[float, float, float], thin_part_size: tuple[float, float],
		hole_diameter: float, hole_distance: float, center_hole_diameter: float, hole_segments: int, hole_bridge_height: float,
		screw_hole_distance_a: float, screw_hole_distance_b: float, screw_hole_distance_x: float,
		screw_hole_front: tuple[str, bool], screw_hole_back: tuple[str, bool], screw_hole_segments: int) -> bpy.types.Object:

	# 長方形を作る
	loadcell_obj = romly_utils.create_box(size=size)


	# 中央の細くなっている部分を削る（削る部分にはアールを付ける）
	if thin_part_size[1] > 0:
		cutter = romly_utils.create_box_from_corners(corner1=(-thin_part_size[0] / 2, -thin_part_size[1] / 2, -size[2]), corner2=(-size[0], thin_part_size[1] / 2, size[2]))
		romly_utils.apply_bevel_modifier_to_edges(cutter, 1.5, lambda edge: romly_utils.is_edge_along_z_axis2(edge), segments=10)
		romly_utils.apply_boolean_object(loadcell_obj, cutter)
		cutter = romly_utils.create_box_from_corners(corner1=(thin_part_size[0] / 2, -thin_part_size[1] / 2, -size[2]), corner2=(size[0], thin_part_size[1] / 2, size[2]))
		romly_utils.apply_bevel_modifier_to_edges(cutter, 1.5, lambda edge: romly_utils.is_edge_along_z_axis2(edge), segments=10)
		romly_utils.apply_boolean_object(loadcell_obj, cutter)




	# 穴を開ける
	if hole_diameter > 0:
		cylinder = romly_utils.create_cylinder(radius=hole_diameter / 2, length_z_plus=size[0], length_z_minus=size[0], segments=hole_segments)
		romly_utils.rotate_object(cylinder, degrees=90, axis='Y')
		cylinder.location = Vector([0, -hole_distance / 2, 0])
		romly_utils.apply_boolean_object(loadcell_obj, cylinder, unlink=False)

		if hole_distance > 0:
			cylinder.location = Vector([0, hole_distance / 2, 0])
			romly_utils.apply_boolean_object(loadcell_obj, cylinder, unlink=False)

		bpy.context.collection.objects.unlink(cylinder)

		# 穴の距離が直径より大きい（穴が離れる）場合は間に四角い穴を開ける
		if hole_bridge_height > 0 and hole_distance > hole_diameter:
			cutter = romly_utils.create_box(size=(size[0] * 2, hole_distance, hole_bridge_height))
			romly_utils.apply_boolean_object(loadcell_obj, cutter)

		# 中心の穴（750gだけにある）
		if center_hole_diameter > 0:
			cylinder = romly_utils.create_cylinder(radius=center_hole_diameter / 2, length_z_plus=size[0], length_z_minus=size[0], segments=hole_segments)
			romly_utils.rotate_object(cylinder, degrees=90, axis='Y')
			romly_utils.apply_boolean_object(loadcell_obj, cylinder)



	def make_screw_holes(screw_hole: tuple[str, bool], y_scale: int) -> None:
		screw_spec = romly_utils.SCREW_SPECS.get(screw_hole[0])
		if not screw_spec:
			return

		cylinder = None
		z_offset = 0
		if screw_hole[1]:
			# ねじ切りありの場合
			cylinder = romly_utils.create_threaded_cylinder(diameter=screw_spec.diameter, length=size[2] + 2, pitch=screw_spec.pitch, lead=1, thread_depth=screw_spec.thread_depth(), segments=screw_hole_segments, bevel_segments=3)
			z_offset = (size[2] + 2) / 2
		else:
			cylinder = romly_utils.create_cylinder(radius=screw_spec.diameter / 2, length_z_plus=size[2], length_z_minus=size[2], segments=screw_hole_segments)

		x = -screw_hole_distance_x / 2
		for _ in range(2):
			cylinder.location = Vector([x, screw_hole_distance_a / 2 * y_scale, z_offset])
			romly_utils.apply_boolean_object(loadcell_obj, cylinder, unlink=False)

			if screw_hole_distance_b > 0:
				cylinder.location = Vector([x, (screw_hole_distance_a / 2 + screw_hole_distance_b) * y_scale, z_offset])
				romly_utils.apply_boolean_object(loadcell_obj, cylinder, unlink=False)

			x += screw_hole_distance_x

		bpy.context.collection.objects.unlink(cylinder)



	# 手前と後ろのネジ穴を開ける
	make_screw_holes(screw_hole_front, -1)
	make_screw_holes(screw_hole_back, 1)



	return loadcell_obj










def update_templates(self: bpy.types.OperatorProperties, context):
	spec = LOADCELL_SPECS.get(self.val_template)
	if spec:
		self.val_size = spec.size
		self.val_thin_part_size = spec.thin_part_size
		self.val_hole_diameter = spec.hole_diameter
		self.val_hole_bridge_height = spec.hole_bridge_height
		self.val_center_hole_diameter = spec.center_hole_diameter
		self.val_length_between_hole_centers = spec.hole_distance
		self.val_screw_holes_distance_a = spec.screw_hole_distance_a
		self.val_screw_holes_distance_b = spec.screw_hole_distance_b
		self.val_screw_holes_distance_x = spec.screw_hole_distance_x
		self.val_screw_hole_front = spec.screw_hole_front[0]
		self.val_screw_hole_front_threaded = spec.screw_hole_front[1]
		self.val_screw_hole_back = spec.screw_hole_back[0]
		self.val_screw_hole_back_threaded = spec.screw_hole_back[1]










class ROMLYADDON_OT_add_loadcell(bpy.types.Operator):
	bl_idname = 'romlyaddon.add_loadcell'
	bl_label = bpy.app.translations.pgettext_iface('Add Loadcell')
	bl_description = 'Construct a Loadcell'
	bl_options = {'REGISTER', 'UNDO'}

	DEFAULT_SPEC = 'normal'

	val_size: FloatVectorProperty(name='Size', description='Overall size of the loadcell', size=3, default=LOADCELL_SPECS[DEFAULT_SPEC].size, precision=3, subtype='TRANSLATION', unit=bpy.utils.units.categories.LENGTH)

	# 中央の細くなっている部分
	val_thin_part_size: FloatVectorProperty(name='Thin Part', description='Width and length of the middle narrow part', size=2, default=LOADCELL_SPECS[DEFAULT_SPEC].thin_part_size, precision=3, subtype='TRANSLATION', unit=bpy.utils.units.categories.LENGTH)

	# 穴の直径
	val_hole_diameter: FloatProperty(name='Cutout Holes Diameter', description='The diameter of the cutout holes', default=LOADCELL_SPECS[DEFAULT_SPEC].hole_diameter, min=0, soft_max=100, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	# 穴の中心位置同士の距離
	val_length_between_hole_centers: FloatProperty(name='Distance Between Cutout Holes', description='Y-axis distance between two cutout holes', default=LOADCELL_SPECS[DEFAULT_SPEC].hole_distance, min=0, soft_max=100, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_hole_bridge_height: FloatProperty(name='Cutout Bridge Height', description='Z-axis height of the bridge between two cutout holes', default=LOADCELL_SPECS[DEFAULT_SPEC].hole_bridge_height, min=0, soft_max=100, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_center_hole_diameter: FloatProperty(name='Center Hole Diameter', description='The diameter of the center hole located between the two cutout holes', default=LOADCELL_SPECS[DEFAULT_SPEC].center_hole_diameter, min=0, soft_max=100, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	# 穴のセグメント数
	val_hole_segments: IntProperty(name='Cutout Hole Segments', default=32, min=3, max=64)

	# 内側のネジ穴同士距離
	val_screw_holes_distance_a: FloatProperty(name='Between Inner Holes', description='The distance between two innermost screw holes', default=LOADCELL_SPECS[DEFAULT_SPEC].screw_hole_distance_a, min=0, soft_max=100, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	# ネジ穴同士の距離
	val_screw_holes_distance_b: FloatProperty(name='Between Front/Rear Holes', description='The distance between two front/rear screw holes. Setting it to zero results in one screw hole at the front and one at the rear', default=LOADCELL_SPECS[DEFAULT_SPEC].screw_hole_distance_b, min=0, soft_max=100, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_screw_holes_distance_x: FloatProperty(name='In the X Direction', description='The distance between each pair of horizontally aligned screw holes. Setting it to zero aligns the screw holes in a single row', default=LOADCELL_SPECS[DEFAULT_SPEC].screw_hole_distance_x, min=0, soft_max=100, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# ネジ穴の径
	SCREW_HOLE_ITEMS = [('m3', 'M3', ''), ('m4', 'M4', ''), ('m5', 'M5', '')]
	val_screw_hole_front: EnumProperty(name='Screw Hole Front', description='Size of the front screw holes', items=SCREW_HOLE_ITEMS, default=LOADCELL_SPECS[DEFAULT_SPEC].screw_hole_front[0])
	val_screw_hole_back: EnumProperty(name='Screw Hole Back', description='Size of the rear screw holes', items=SCREW_HOLE_ITEMS, default=LOADCELL_SPECS[DEFAULT_SPEC].screw_hole_back[0])
	val_screw_hole_front_threaded: BoolProperty(name='Threaded', description="Thread the front screw holes. You also need to check the 'Enable Threading'", default=LOADCELL_SPECS[DEFAULT_SPEC].screw_hole_front[1])
	val_screw_hole_back_threaded: BoolProperty(name='Threaded', description="Thread the rear screw holes. You also need to check the 'Enable Threading'", default=LOADCELL_SPECS[DEFAULT_SPEC].screw_hole_back[1])
	val_screw_hole_segments: IntProperty(name='Screw Hole Segments', description='Screw Hole Segments', default=32, min=3, max=64)
	val_screw_hole_threaded: BoolProperty(name='Enable Threading', description='Checking this option enables threading settings for the front and rear screw holes', default=False)

	# 原点位置
	val_origin_y: EnumProperty(name='Y-Origin', description='The Y-axis origin position of the loadcell object', items=[
		('center', 'Center', ''),
		('front_screw_1', 'Front Screw Hole 1', ''),
		('front_screw_center', 'Front Screw Holes Center', ''),
		('front_screw_2', 'Front Screw Hole 2', ''),
		('back_screw_1', 'Rear Screw Hole 1', ''),
		('back_screw_center', 'Rear Screw Holes Center', ''),
		('back_screw_2', 'Rear Screw Hole 2', '')], default='back_screw_2')
	val_origin_z: EnumProperty(name='Z-Origin', description='The Z-axis origin position of the loadcell object', items=[
		('top', 'Top', ''), ('center', 'Center', ''), ('bottom', 'Bottom', '')], default='center')

	# テンプレート
	val_template: EnumProperty(name='Templates', items=[
		('normal', '5kg Size', ''), ('small', '1kg Size', ''), ('tiny', '500g Size', ''), ('i-shape', '100g Size', ''),
	], default='normal', update=update_templates)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		split = col.split(factor=0.4, align=True)
		split.label(text='Template:')
		split.prop(self, 'val_template', text='')
		col.separator()

		col.label(text='Size')
		row = col.row(align=True)
		row.prop(self, 'val_size', text='')
		row = col.row(align=True)
		row.prop(self, 'val_thin_part_size')
		col.separator()

		col.label(text='Cutout')
		col.prop(self, 'val_hole_diameter')
		col.prop(self, 'val_length_between_hole_centers')
		col.prop(self, 'val_hole_bridge_height')
		col.prop(self, 'val_center_hole_diameter')
		col.separator()

		def add_screw_hole_prop(label: str, prop1: str, prop2: str):
			split = col.split(factor=0.15, align=True)
			split.label(text=label)
			split2 = split.split(factor=0.65, align=True)
			row = split2.row(align=True)
			row.prop(self, prop1, expand=True)
			split2.prop(self, prop2)

		col.label(text='Screw Holes Distance')
		col.prop(self, 'val_screw_holes_distance_a')
		col.prop(self, 'val_screw_holes_distance_b')
		col.prop(self, 'val_screw_holes_distance_x')
		col.label(text='Screw Hole Sizes')
		add_screw_hole_prop('Front:', 'val_screw_hole_front', 'val_screw_hole_front_threaded')
		add_screw_hole_prop('Rear:', 'val_screw_hole_back', 'val_screw_hole_back_threaded')
		col.prop(self, 'val_screw_hole_threaded')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_hole_segments')
		col.prop(self, 'val_screw_hole_segments')
		col.prop(self, 'val_origin_y')
		row = col.row(align=True)
		row.label(text='Z-Origin:')
		row.prop(self, 'val_origin_z', expand=True)



	def execute(self, context):
		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')



		obj = create_loadcell(
			size=self.val_size,
			thin_part_size=self.val_thin_part_size,
			hole_diameter=self.val_hole_diameter,
			hole_distance=self.val_length_between_hole_centers,
			center_hole_diameter=self.val_center_hole_diameter,
			hole_segments=self.val_hole_segments,
			hole_bridge_height=self.val_hole_bridge_height,
			screw_hole_distance_a=self.val_screw_holes_distance_a,
			screw_hole_distance_b=self.val_screw_holes_distance_b,
			screw_hole_distance_x=self.val_screw_holes_distance_x,
			screw_hole_front=(self.val_screw_hole_front, self.val_screw_hole_front_threaded and self.val_screw_hole_threaded),
			screw_hole_back=(self.val_screw_hole_back, self.val_screw_hole_back_threaded and self.val_screw_hole_threaded),
			screw_hole_segments=self.val_screw_hole_segments)

		# 原点位置の設定
		y_offset, z_offset = 0, 0
		match self.val_origin_y:
			case 'front_screw_1' | 'back_screw_1':
				y_offset = self.val_screw_holes_distance_a / 2
			case 'front_screw_center' | 'back_screw_center':
				y_offset = self.val_screw_holes_distance_a / 2 + self.val_screw_holes_distance_b / 2
			case 'front_screw_2' | 'back_screw_2':
				y_offset = self.val_screw_holes_distance_a / 2 + self.val_screw_holes_distance_b
		if 'back' in self.val_origin_y:
			y_offset = -y_offset
		match self.val_origin_z:
			case 'top':
				z_offset = -self.val_size[2] / 2
			case 'bottom':
				z_offset = self.val_size[2] / 2
		if y_offset != 0 or z_offset != 0:
			romly_utils.translate_vertices(obj, Vector([0, y_offset, z_offset]))

		# オブジェクトの名前を設定
		obj.name = bpy.app.translations.pgettext_data('Loadcell') + ' ' + romly_utils.units_to_string(self.val_size[1], category=bpy.utils.units.categories.LENGTH, removeSpace=True)



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
	self.layout.operator(ROMLYADDON_OT_add_loadcell.bl_idname, text=bpy.app.translations.pgettext_iface('Add Loadcell'), icon='NLA_PUSHDOWN')





classes = [
	ROMLYADDON_OT_add_loadcell,
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
