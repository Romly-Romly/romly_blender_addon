import bpy
from bpy.props import *
import bmesh
import math
import mathutils

from . import romly_utils





DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_HOLE = 'diameter/hole'
DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_THICKNESS = 'diameter/thickness'
DONUT_CYLINDER_DIAMETER_METHOD_HOLE_AND_THICKNESS = 'hole/thickness'

MESH_VERTICAL_ALIGNMENT_TOP = 'top'
MESH_VERTICAL_ALIGNMENT_MIDDLE = 'middle'
MESH_VERTICAL_ALIGNMENT_BOTTOM = 'bottom'

MeshVerticalAlignment = [
	(MESH_VERTICAL_ALIGNMENT_TOP, 'Top', 'Set origin to top'),
	(MESH_VERTICAL_ALIGNMENT_MIDDLE, 'Middle', 'Set origin to center'),
	(MESH_VERTICAL_ALIGNMENT_BOTTOM, 'Bottom', 'Set origin to bottom')
]





def ApplyBooleanObject(object, boolObject, unlink):
	"""ブーリアンモデファイア(Difference)を使ってメッシュをもう一方のメッシュの形状で削る。

	Parameters
	----------
	object : Mesh
		元となるメッシュ。
	boolObject : Mesh
		ブーリアンモデファイアに設定されるメッシュ。シーンにリンクされていないとエラーになる。
	unlink : Bool
		処理後にboolObjectをシーンからアンリンクするか。
	"""
	bpy.context.view_layer.objects.active = object
	bpy.context.object.modifiers.new(type='BOOLEAN', name='Boolean')
	bpy.context.object.modifiers["Boolean"].object = boolObject
	bpy.ops.object.modifier_apply(modifier="Boolean")
	if unlink:
		bpy.context.collection.objects.unlink(boolObject)





# 中央に穴の空いたシリンダーを生成する
class ROMLY_OT_add_donut_cylinder(bpy.types.Operator):
	bl_idname = "romly.add_donut_cylinder"
	bl_label = "Add Donut Cylinder"
	bl_description = '中央に穴の空いたシリンダーのメッシュを作成します'
	bl_options = {'REGISTER', 'UNDO'}

	DiameterMethod = [
		(DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_HOLE, '直径と穴径', '直径と穴径で指定します'),
		(DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_THICKNESS, '直径と厚み', '直径と厚みで指定します'),
		(DONUT_CYLINDER_DIAMETER_METHOD_HOLE_AND_THICKNESS, '穴径と厚み', '穴径と厚みで指定します')
	]

	#--- properties ---#
	val_diameterMethod: EnumProperty(name='Method', description='径の指定方法', default=DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_HOLE, items=DiameterMethod)
	val_majorDiameter: FloatProperty(name='Diameter', description='シリンダーの直径', default=1.0, min=0.001, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_holeDiameter: FloatProperty(name='Hole Diameter', description='穴の直径', default=0.5, min=0.0, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_thickness: FloatProperty(name='Thickness', description='厚み', min=0.01, max=1000, default=0.25, subtype='DISTANCE', unit='LENGTH')

	val_height: FloatProperty(name='Height', description='シリンダーの高さ', default=1, min=0.0001, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_origin: EnumProperty(name='Origin', description='シリンダーの原点位置', default=MESH_VERTICAL_ALIGNMENT_BOTTOM, items=MeshVerticalAlignment)

	val_amount: FloatProperty(name='Amount', description='作成する立方体の分量', default=math.radians(360), min=math.radians(0.1), max=math.radians(360), subtype='ANGLE', unit='ROTATION')
	val_rotation: FloatProperty(name='Rotation', description='回転', default=math.radians(0), min=math.radians(0.1), max=math.radians(360), subtype='ANGLE', unit='ROTATION')

	val_majorSegments: IntProperty(name='Segments', description='セグメント数', default=32, min=3, max=128, subtype='NONE')
	val_holeSegments: IntProperty(name='Hole Segments', description='穴のセグメント数', default=32, min=3, max=128, subtype='NONE')
	val_smooth: BoolProperty(name='Auto Smooth', description='チェックするとメッシュのスムーズシェーディングとAuto Smoothを有効にします', default=True)

	def draw(self, context):
		col = self.layout.column()

		col.label(text="Diameters")
		col.row(align=True).prop(self, 'val_diameterMethod', expand=True)
		if self.val_diameterMethod == DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_HOLE:
			col.prop(self, 'val_majorDiameter')
			col.prop(self, 'val_holeDiameter')
			row = col.row()
			row.alignment = 'RIGHT'
			row.label(text='Thickness: {value}'.format(value=romly_utils.units_to_string(value=(self.val_majorDiameter - self.val_holeDiameter) / 2)))
		elif self.val_diameterMethod == DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_THICKNESS:
			col.prop(self, 'val_majorDiameter')
			row = col.row()
			row.alignment = 'RIGHT'
			row.label(text='Hole Diameter: {value}'.format(value=romly_utils.units_to_string(value=(self.val_majorDiameter - self.val_thickness * 2))))
			col.prop(self, 'val_thickness')
		elif self.val_diameterMethod == DONUT_CYLINDER_DIAMETER_METHOD_HOLE_AND_THICKNESS:
			row = col.row()
			row.alignment = 'RIGHT'
			row.label(text='Diameter: {value}'.format(value=romly_utils.units_to_string(value=(self.val_holeDiameter + self.val_thickness * 2))))
			col.prop(self, 'val_holeDiameter')
			col.prop(self, 'val_thickness')
		col.separator()

		col.label(text='Height')
		col.prop(self, 'val_height')
		row = col.row(align=True)
		row.label(text='Origin')
		row.prop(self, 'val_origin', expand=True)
		col.separator()

		col.label(text='Amount')
		col.prop(self, 'val_amount')
		if self.val_amount < math.pi * 2:
			col.prop(self, 'val_rotation')
		col.separator()

		col.label(text="Mesh Settings")
		col.prop(self, 'val_majorSegments')
		col.prop(self, 'val_holeSegments')
		col.prop(self, 'val_smooth')

	#--- invoke ---#
	def invoke(self, context, event):
		return self.execute(context)

	#--- execute ---#
	def execute(self, context):
		if self.val_diameterMethod == DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_HOLE:
			majorRadius = self.val_majorDiameter / 2
			holeRadius = self.val_holeDiameter / 2
		elif self.val_diameterMethod == DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_THICKNESS:
			majorRadius = self.val_majorDiameter / 2
			holeRadius = majorRadius - self.val_thickness
		elif self.val_diameterMethod == DONUT_CYLINDER_DIAMETER_METHOD_HOLE_AND_THICKNESS:
			holeRadius = self.val_holeDiameter / 2
			majorRadius = holeRadius + self.val_thickness

		# 穴の直径の方が大きい場合は警告
		if holeRadius >= majorRadius:
			self.report({'WARNING'}, '穴の直径を外径より大きくすることはできません')
			return {'CANCELLED'}
		elif holeRadius < 0:
			self.report({'WARNING'}, '穴の直径をマイナスにすることはできません')
			return {'CANCELLED'}
		else:
			# 選択を解除
			bpy.ops.object.select_all(action='DESELECT')

			# シリンダーを生成
			bpy.ops.mesh.primitive_cylinder_add(vertices=self.val_majorSegments, radius=majorRadius, depth=self.val_height, end_fill_type='NGON', enter_editmode=False, location=bpy.context.scene.cursor.location)
			cylinderObject = bpy.data.objects[bpy.context.active_object.name]

			# 穴となるシリンダーを生成してブーリアン
			if holeRadius > 0:
				bpy.ops.mesh.primitive_cylinder_add(vertices=self.val_holeSegments, radius=holeRadius, depth=self.val_height * 2, end_fill_type='NGON', enter_editmode=False, location=bpy.context.scene.cursor.location)
				holeCylinderObject = bpy.data.objects[bpy.context.active_object.name]
				ApplyBooleanObject(object=cylinderObject, boolObject=holeCylinderObject, unlink=True)

			# 作成する分量が360度以下の場合
			if self.val_amount < math.radians(360):
				# ブーリアン用のメッシュを作成
				subtructMesh = CreatePieCutMesh(amountAngle=self.val_amount, rotateAngle=self.val_rotation)
				bpy.context.collection.objects.link(subtructMesh)
				ApplyBooleanObject(object=cylinderObject, boolObject=subtructMesh, unlink=True)


			# 原点位置の設定に従ってずらす
			if self.val_origin == MESH_VERTICAL_ALIGNMENT_TOP:
				romly_utils.translate_vertices(object=cylinderObject, vector=mathutils.Vector([0, 0, -self.val_height / 2]))
			elif self.val_origin == MESH_VERTICAL_ALIGNMENT_BOTTOM:
				romly_utils.translate_vertices(object=cylinderObject, vector=mathutils.Vector([0, 0, self.val_height / 2]))

			# 選択
			cylinderObject.select_set(state=True)

			# スムーズシェーディング
			if self.val_smooth:
				bpy.ops.object.shade_smooth()
				cylinderObject.data.use_auto_smooth = True

			cylinderObject.name = 'Donut Cylinder {majorDiameter}/{holeDiameter}'.format(majorDiameter=romly_utils.units_to_string(value=majorRadius * 2, removeSpace=True), holeDiameter=romly_utils.units_to_string(value=holeRadius * 2, removeSpace=True))

			return {'FINISHED'}





# 親となるメニュー
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLY_OT_add_donut_cylinder.bl_idname, icon='MESH_CYLINDER')





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	bpy.utils.register_class(ROMLY_OT_add_donut_cylinder)
	bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLY_OT_add_donut_cylinder)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()
