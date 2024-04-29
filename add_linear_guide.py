import bpy
import math
import mathutils
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple



import romly_utils

# romly_utilsの再読み込み（Blenderを再起動しなくてもよくなる）
import importlib
importlib.reload(romly_utils)










class LinearGuideSpec(NamedTuple):
	Wr: float
	Hr: float
	outer_hole_diameter: float
	outer_hole_depth: float
	inner_hole_diameter: float
	hole_pitch: float

SCREW_SPECS = {
	'mgn07': LinearGuideSpec(Wr=7, Hr=4.8, outer_hole_diameter=4.2, outer_hole_depth=2.3, inner_hole_diameter=2.4, hole_pitch=15),
	'mgn09': LinearGuideSpec(Wr=9, Hr=6.5, outer_hole_diameter=6.0, outer_hole_depth=3.5, inner_hole_diameter=3.5, hole_pitch=20),
	'mgn12': LinearGuideSpec(Wr=12, Hr=8, outer_hole_diameter=6.0, outer_hole_depth=4.5, inner_hole_diameter=3.5, hole_pitch=25),
	'mgn15': LinearGuideSpec(Wr=15, Hr=10, outer_hole_diameter=6.0, outer_hole_depth=4.5, inner_hole_diameter=3.5, hole_pitch=40),
}

LINEAR_GUIDE_SIZE_ITEMS = [
	('mgn07', 'MGN7', 'Set specs to MGN07 size'),
	('mgn09', 'MGN9', 'Set specs to MGN09 size'),
	('mgn12', 'MGN12', 'Set specs to MGN12 size'),
	('mgn15', 'MGN15', 'Set specs to MGN15 size'),
]

def update_spec(self, context):
	"""プロパティのパネルでM2〜M8などのボタンを押した時の処理。プロパティの値を押したボタンに合わせてセットする。"""

	# 指定されたスクリューサイズに基づいて直径とピッチを設定
	spec = SCREW_SPECS.get(self.val_spec)
	if spec:
		self.val_rail_width = spec.Wr
		self.val_rail_height = spec.Hr
		self.val_rail_outer_hole_diameter = spec.outer_hole_diameter
		self.val_rail_outer_hole_depth = spec.outer_hole_depth
		self.val_rail_inner_hole_diameter = spec.inner_hole_diameter
		self.val_rail_hole_pitch = spec.hole_pitch

class ROMLYADDON_OT_add_linear_guide_rail(bpy.types.Operator):
	"""リニアガイドのレールを作成するオペレーター。"""
	bl_idname = 'romlyaddon.add_linear_guide_rail'
	bl_label = bpy.app.translations.pgettext_iface('Add Linear Guide Rail')
	bl_description = 'Construct a Rail for Linear Guide Rail'
	bl_options = {'REGISTER', 'UNDO'}

	DEFAULT_SIZE = 'mgn09'
	val_spec: EnumProperty(name='Size', items=LINEAR_GUIDE_SIZE_ITEMS, default=DEFAULT_SIZE, update=update_spec)

	val_rail_width: FloatProperty(name='Width', description='Width of the rail', default=SCREW_SPECS[DEFAULT_SIZE].Wr, min=1, soft_max=15.0, unit=bpy.utils.units.categories.LENGTH)
	val_rail_height: FloatProperty(name='Height', description='Height (Thickness) of the rail', default=SCREW_SPECS[DEFAULT_SIZE].Hr, min=1, soft_max=10.0, unit=bpy.utils.units.categories.LENGTH)

	# レールの長さ
	val_rail_length: FloatProperty(name='Length', description='Full length of the rail', default=100.0, min=50, soft_max=1000.0, unit=bpy.utils.units.categories.LENGTH)

	val_rail_outer_hole_diameter: FloatProperty(name='Outer Diameter', description='Outer Diameter of each hole', default=SCREW_SPECS[DEFAULT_SIZE].outer_hole_diameter, min=1, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH)
	val_rail_inner_hole_diameter: FloatProperty(name='Inner Diameter', description='Inner Diameter of each hole', default=SCREW_SPECS[DEFAULT_SIZE].inner_hole_diameter, min=1, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH)
	val_rail_outer_hole_depth: FloatProperty(name='Outer Hole Depth', description='Depth of outer hole', default=SCREW_SPECS[DEFAULT_SIZE].outer_hole_depth, min=1, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH)
	val_rail_hole_pitch: FloatProperty(name='Hole Pitch', description='Hole Pitch', default=SCREW_SPECS[DEFAULT_SIZE].hole_pitch, min=1, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH)

	val_first_hole_offset: FloatProperty(name='First Hole Offset', description='First Hole Offset', default=5, min=0, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH)

	val_hole_segments: IntProperty(name='Hole Segments', description='Hole Segments', default=32, min=3, soft_max=64, max=128)

	val_slit_diameter: FloatProperty(name='Slit Diameter', description='Slit Diameter', default=1.5, min=1, soft_max=2.0, unit=bpy.utils.units.categories.LENGTH)
	val_slit_offset: FloatProperty(name='Slit Position', description='Position of the slits (from the surface)', default=2.0, min=0.5, soft_max=10.0, unit=bpy.utils.units.categories.LENGTH)
	val_slit_segments: IntProperty(name='Slit Segments', description='Slit Segments', default=24, min=3, soft_max=32, max=64)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		row = col.row(align=True)
		row.prop(self, 'val_spec', expand=True)

		box = col.box()
		box_col = box.column()
		row = box_col.row(align=True)
		row.prop(self, 'val_rail_width')
		row.prop(self, 'val_rail_height')
		box_col.separator()
		split = box_col.split(factor=0.2, align=True)
		split.label(text='Hole Diameter')
		row = split.row(align=True)
		row.prop(self, 'val_rail_outer_hole_diameter', text='Outer')
		row.prop(self, 'val_rail_inner_hole_diameter', text='Inner')
		box_col.prop(self, 'val_rail_outer_hole_depth')
		box_col.prop(self, 'val_rail_hole_pitch')
		col.separator()

		col.prop(self, 'val_rail_length')
		col.prop(self, 'val_first_hole_offset')
		col.separator()

		split = col.split(factor=0.1, align=True)
		split.label(text='Slit')
		row = split.row(align=True)
		row.prop(self, 'val_slit_diameter', text='Diameter')
		row.prop(self, 'val_slit_offset', text='Offset')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_hole_segments')
		col.prop(self, 'val_slit_segments')



	def execute(self, context):
		obj = romly_utils.create_box(Vector((self.val_rail_width, self.val_rail_height, self.val_rail_length)), offset=Vector((0, -self.val_rail_height / 2, self.val_rail_length / 2)))

		obj_name = 'Linear Guide Rail'

		obj.name = bpy.app.translations.pgettext_data(obj_name)
		bpy.context.collection.objects.link(obj)



		# Z軸と平行な辺を選択し、Bevel Weightを設定
		bpy.context.view_layer.objects.active = obj
		romly_utils.select_edges_by_condition(lambda edge: not romly_utils.is_edge_along_z_axis(edge))
		romly_utils.set_bevel_weight(obj)

		# ベベルモディファイアを追加、適用
		bevel_modifier = obj.modifiers.new(name='Bevel', type='BEVEL')
		bevel_modifier.offset_type = 'OFFSET'
		bevel_modifier.use_clamp_overlap = True
		bevel_modifier.limit_method = 'WEIGHT'
		bevel_modifier.width = 0.3
		bevel_modifier.segments = 1
		bevel_modifier.profile = 0.5
		bpy.ops.object.modifier_apply(modifier=bevel_modifier.name)



		# 穴を開ける
		hole_z = self.val_first_hole_offset
		while hole_z <= self.val_rail_length:

			hole_vertices = romly_utils.make_circle_vertices(radius=self.val_rail_outer_hole_diameter / 2, num_vertices=self.val_hole_segments, center=(0, -self.val_rail_height + self.val_rail_outer_hole_depth, hole_z), normal_vector=(0, 1, 0))
			hole_faces = [list(range(len(hole_vertices)))]
			romly_utils.extrude_face(hole_vertices, faces=hole_faces, extrude_vertex_indices=list(range(len(hole_vertices))), offset=Vector((0, -self.val_rail_outer_hole_depth * 2, 0)))
			hole_obj = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=hole_vertices, faces=hole_faces))
			bpy.context.collection.objects.link(hole_obj)
			romly_utils.apply_boolean_object(obj, hole_obj);

			hole_vertices = romly_utils.make_circle_vertices(radius=self.val_rail_inner_hole_diameter / 2, num_vertices=self.val_hole_segments, center=(0, 0.1, hole_z), normal_vector=(0, 1, 0))
			hole_faces = [list(range(len(hole_vertices)))]
			romly_utils.extrude_face(hole_vertices, faces=hole_faces, extrude_vertex_indices=list(range(len(hole_vertices))), offset=Vector((0, -self.val_rail_height + 0.2, 0)))
			hole_obj = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=hole_vertices, faces=hole_faces))
			bpy.context.collection.objects.link(hole_obj)
			romly_utils.apply_boolean_object(obj, hole_obj);

			hole_z += self.val_rail_hole_pitch



		# ボール溝を作る
		hole_vertices = romly_utils.make_circle_vertices(radius=self.val_slit_diameter / 2, num_vertices=self.val_slit_segments, center=(-self.val_rail_width / 2, -self.val_rail_height + self.val_slit_offset, -0.1), normal_vector=(0, 0, 1))
		hole_faces = [list(range(len(hole_vertices)))]
		romly_utils.extrude_face(hole_vertices, faces=hole_faces, extrude_vertex_indices=list(range(len(hole_vertices))), offset=Vector((0, 0, self.val_rail_length + 0.2)))
		hole_obj = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=hole_vertices, faces=hole_faces))
		bpy.context.collection.objects.link(hole_obj)
		romly_utils.apply_boolean_object(obj, hole_obj);

		hole_vertices = romly_utils.make_circle_vertices(radius=self.val_slit_diameter / 2, num_vertices=self.val_slit_segments, center=(self.val_rail_width / 2, -self.val_rail_height + self.val_slit_offset, -0.1), normal_vector=(0, 0, 1))
		hole_faces = [list(range(len(hole_vertices)))]
		romly_utils.extrude_face(hole_vertices, faces=hole_faces, extrude_vertex_indices=list(range(len(hole_vertices))), offset=Vector((0, 0, self.val_rail_length + 0.2)))
		hole_obj = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=hole_vertices, faces=hole_faces))
		bpy.context.collection.objects.link(hole_obj)
		romly_utils.apply_boolean_object(obj, hole_obj);




		# オブジェクトを3Dカーソル位置へ移動
		obj.location = bpy.context.scene.cursor.location

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}










class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = 'ROMLYADDON_MT_romly_add_mesh_menu_parent'
	bl_label = 'Romly'
	bl_description = 'Romly Addon Menu'



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_linear_guide_rail.bl_idname, text=bpy.app.translations.pgettext_iface('Add Linear Guide Rail'), icon='FIXED_SIZE')









# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_linear_guide_rail,
	ROMLYADDON_MT_romly_add_mesh_menu_parent,
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
