import bpy
import math
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple, Literal



from . import romly_utils










# MARK: is_bevel_edge
def is_bevel_edge(edge: bmesh.types.BMEdge) -> bool:
	"""
	リードナットのオブジェクトの指定された辺がベベルすべき辺ならTrueを返す。
	Z軸に平行な辺で、90度の角度にある（平面上にある辺ではない）辺。

	Parameters
	----------
	edge : bmesh.types.BMEdge
		判定対象の辺を指定。

	Returns
	-------
	bool
		ベベルすべき辺ならTrueを返す。
	"""
	# 閾値値の角度を内積の値に変換
	threshold_radian = math.radians(0.1)
	cos_value = math.cos(threshold_radian)

	if math.isclose(edge.verts[0].co[2], edge.verts[1].co[2], abs_tol=0.01):
		# 内積が閾値以下なら、その辺を選択
		dot = romly_utils.calc_linked_face_dot(edge)
		if dot < cos_value:
			return True

	return False










# MARK: ROMLYADDON_OT_add_lead_nut
class ROMLYADDON_OT_add_lead_nut(bpy.types.Operator):
	"""リードナットを作成するオペレーター。"""
	bl_idname = 'romlyaddon.add_lead_nut'
	bl_label = bpy.app.translations.pgettext_iface('Add Lead Nut')
	bl_description = 'Construct a Lead Nut'
	bl_options = {'REGISTER', 'UNDO'}

	val_hole_diameter: FloatProperty(name='Hole Diameter', default=8, min=0.1, max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)

	# プレート部
	val_plate_diameter: FloatProperty(name='Diameter', default=22, min=0, max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)
	val_plate_thickness: FloatProperty(name='Thickness', default=3.5, min=0, max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)
	val_plate_width: FloatProperty(name='Width', description="Specify the width of the flange when it is not circular. If it's a complete circle, set this value to zero", default=0, min=0, max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)

	val_shaft_diameter: FloatProperty(name='Shaft Diameter', default=10, min=0.1, max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)
	val_shaft_length_above: FloatProperty(name='Shaft Length Above', default=1.5, min=0, max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)
	val_shaft_length_below: FloatProperty(name='Shaft Length Below', default=10, min=0.1, max=100.0, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)

	# ネジ穴の中心位置の直径
	val_screw_holes_center_diameter: FloatProperty(name='Center Position Diameter', default=16, min=1, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3)
	# ネジ穴の直径
	val_screw_holes_diameter: FloatProperty(name='Diameter', default=3.5, min=1, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3)
	# ネジ穴の数（片面）
	val_screw_hole_count: IntProperty(name='Count', description='The number of screw holes on one side. The total number of screw holes will be twice this value', default=2, min=1, soft_max=4, step=1)
	# ネジ穴の間隔（角度）
	val_screw_hole_angular_pitch: FloatProperty(name='Angle', description='The angle between each screw hole', default=math.radians(90), min=math.radians(5), soft_max=math.radians(90), step=1, precision=3, subtype='ANGLE', unit=bpy.utils.units.categories.ROTATION)

	# プレート部分の縁のベベル
	val_bevel_width: FloatProperty(name='Bevel Width', default=0.1, min=0, soft_max=2, step=1, precision=3, unit=bpy.utils.units.categories.LENGTH)

	val_segments: IntProperty(name='Segments', default=32, min=3, max=128, step=1)

	# ネジ穴のセグメント数
	val_screw_holes_segments: IntProperty(name='Screw Hole Segments', default=16, min=3, max=64, step=1)





	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_hole_diameter')
		col.separator()

		col.label(text='Flange')
		col.prop(self, 'val_plate_diameter')
		row = col.row(align=True)
		row.prop(self, 'val_plate_thickness', text=romly_utils.translate('Thickness', 'IFACE'))	# 'Thickness'はBlender内部の辞書で『幅』に翻訳されてしまうので、自前で翻訳
		row.prop(self, 'val_plate_width')
		col.separator()

		col.prop(self, 'val_shaft_diameter')
		col_shaft_length = col.column(align=True)
		col_shaft_length.prop(self, 'val_shaft_length_above')
		col_shaft_length.prop(self, 'val_shaft_length_below')
		row = col.row(align=True)
		row.alignment = 'RIGHT'
		row.label(text=bpy.app.translations.pgettext_iface('Total Length (Height): {value}').format(value=romly_utils.units_to_string(self.val_plate_thickness + self.val_shaft_length_above + self.val_shaft_length_below)))
		col.separator()

		col.label(text='Screw Holes')
		col.prop(self, 'val_screw_holes_diameter')
		col.prop(self, 'val_screw_holes_center_diameter')
		row = col.row(align=True)
		row.prop(self, 'val_screw_hole_count')
		row.prop(self, 'val_screw_hole_angular_pitch')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_bevel_width')
		col.prop(self, 'val_segments')
		col.prop(self, 'val_screw_holes_segments')



	def execute(self, context):
		# プレート部分を作成
		obj = None
		if self.val_plate_thickness > 0 and self.val_plate_diameter > 0:
			obj = romly_utils.create_cylinder(radius=self.val_plate_diameter / 2, length_z_plus=self.val_plate_thickness, segments=self.val_segments)
		else:
			obj = romly_utils.create_empty_object()

		# シャフト部分を作成して合成
		shaft_obj = None
		if math.isclose(self.val_shaft_length_above, 0, abs_tol=0.01):
			# 中心部がプレートより上に出ない場合、ブーリアンで合成した時に表面に頂点ができてしまうのを防ぐために少し下げる
			shaft_obj = romly_utils.create_cylinder(radius=self.val_shaft_diameter / 2, length_z_plus=self.val_plate_thickness / 2, length_z_minus=self.val_shaft_length_below, segments=self.val_segments)
		else:
			shaft_obj = romly_utils.create_cylinder(radius=self.val_shaft_diameter / 2, length_z_plus=self.val_shaft_length_above + self.val_plate_thickness, length_z_minus=self.val_shaft_length_below, segments=self.val_segments)
		romly_utils.apply_boolean_object(object=obj, boolObject=shaft_obj, operation='UNION')



		# ベベルを作成
		if self.val_bevel_width > 0:
			romly_utils.apply_bevel_modifier_to_edges(obj, self.val_bevel_width, lambda edge: is_bevel_edge(edge))
			romly_utils.clear_bevel_weight(obj)



		# プレートが円形でない場合のカット
		if self.val_plate_width > 0:
			x1 = self.val_plate_width / 2
			x2 = self.val_plate_diameter
			y1 = self.val_plate_diameter
			z1 = self.val_plate_thickness + 0.5
			z2 = -0.5
			cutter = romly_utils.create_box_from_corners(corner1=(-x1, y1, z1), corner2=(-x2, -y1, z2))
			romly_utils.apply_boolean_object(object=obj, boolObject=cutter)
			cutter = romly_utils.create_box_from_corners(corner1=(x1, y1, z1), corner2=(x2, -y1, z2))
			romly_utils.apply_boolean_object(object=obj, boolObject=cutter)



		# 中心に穴を開ける
		hole_obj = romly_utils.create_cylinder(radius=self.val_hole_diameter / 2, length_z_plus=self.val_plate_thickness + self.val_shaft_length_above + 0.5, length_z_minus=self.val_shaft_length_below + 0.5, segments=self.val_segments)
		romly_utils.apply_boolean_object(object=obj, boolObject=hole_obj)



		# ネジ穴を開ける
		screw_hole = romly_utils.create_cylinder(radius=self.val_screw_holes_diameter / 2, length_z_plus=self.val_plate_thickness + 0.5, length_z_minus=0.5, segments=self.val_screw_holes_segments)
		centers = []
		first = Vector([0, -self.val_screw_holes_center_diameter / 2, 0])
		a = self.val_screw_hole_angular_pitch * (self.val_screw_hole_count - 1) / 2
		m = Matrix.Rotation(-a, 4, 'Z')
		v = m @ first
		centers.append(v)
		v = Matrix.Rotation(math.radians(180), 4, 'Z') @ v
		centers.append(v)
		for i in range(self.val_screw_hole_count - 1):
			v = Matrix.Rotation(self.val_screw_hole_angular_pitch, 4, 'Z') @ v
			centers.append(v)
			v = Matrix.Rotation(math.radians(180), 4, 'Z') @ v
			centers.append(v)
		for c in centers:
			screw_hole.location = c
			romly_utils.apply_boolean_object(object=obj, boolObject=screw_hole, unlink=False)
		bpy.context.collection.objects.unlink(screw_hole)



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
	self.layout.operator(ROMLYADDON_OT_add_lead_nut.bl_idname, text=bpy.app.translations.pgettext_iface('Add Lead Nut'), icon='MOD_CLOTH')





classes = [
	ROMLYADDON_OT_add_lead_nut,
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