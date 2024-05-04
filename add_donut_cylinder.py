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





def CreatePieCutMesh(amountAngle, rotateAngle, cutSize=10, cutHeight=10):
	"""シリンダーなどをパイ状にカットするためのブーリアン用メッシュを作成する。

	Parameters
	----------
	amountAngle : Float
		シリンダーをこのメッシュでカットした時に残るパイのラジアン単位の角度。
	rotateAngle : Float
		生成されるメッシュのZ軸回りのラジアン単位の回転角度。残ったパイを原点周りに回転させたい時に。
	cutSize : int, optional
		生成されるメッシュの半径的な。カットしたいメッシュのサイズより十分に大きい値を指定してね。
	cutHeight : int, optional
		生成されるメッシュの高さ。カットしたいメッシュの高さより十分に大きい値を指定していね。

	Returns
	-------
	Mesh
		[description]
	"""
	vertices = []
	faces = []

	vertices.append(romly_utils.VECTOR_Y_PLUS() * cutSize)
	vertices.append(romly_utils.VECTOR_ZERO())
	vertices.append(romly_utils.rotated_vector(vector=romly_utils.VECTOR_Y_PLUS() * cutSize, angle_radians=amountAngle, axis='Z'))

	# 180度以下の場合は窪んだ形になるので頂点が増える
	if amountAngle < math.radians(180):
		vertices.append(mathutils.Vector([-cutSize, -cutSize, 0]))
		vertices.append(mathutils.Vector([0, -cutSize, 0]))

	if amountAngle < math.radians(270):
		vertices.append(mathutils.Vector([cutSize, -cutSize, 0]))

	vertices.append(mathutils.Vector([cutSize, cutSize, 0]))

	faces.append(list(reversed(range(len(vertices)))))

	# 掃引
	romly_utils.extrude_face(vertices=vertices, faces=faces, extrude_vertex_indices=faces[0], z_offset=cutHeight)

	# 回転
	romly_utils.rotate_vertices(object=vertices, degrees=math.degrees(rotateAngle), axis='Z')

	mesh = romly_utils.create_object(vertices=vertices, faces=faces, name='Pie Cutter')
	romly_utils.cleanup_mesh(object=mesh)
	mesh.location.z = -cutHeight / 2
	return mesh






# MARK: Class
class ROMLYADDON_OT_add_donut_cylinder(bpy.types.Operator):
	"""中空構造の円柱を作成するオペレーター"""
	bl_idname = 'romlyaddon.add_donut_cylinder'
	bl_label = bpy.app.translations.pgettext_iface('Add Donut Cylinder')
	bl_description = 'Construct a donut cylinder mesh'
	bl_options = {'REGISTER', 'UNDO'}



	val_diameterMethod: EnumProperty(name='Method', description='How to specify its size', default=DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_HOLE, items=[
		(DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_HOLE, 'Diameter & Hole Diameter', 'Specify its size by the diameter and the hole diameter'),
		(DONUT_CYLINDER_DIAMETER_METHOD_DIAMETER_AND_THICKNESS, 'Diameter & Thickness', 'Specify its size by the diameter and the thickness'),
		(DONUT_CYLINDER_DIAMETER_METHOD_HOLE_AND_THICKNESS, 'Hole Diameter & Thickness', 'Specify its size by the hole diameter and the thickness')
	])
	val_majorDiameter: FloatProperty(name='Diameter', description='The outer diameter of the cylinder', default=1.0, min=0.001, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_holeDiameter: FloatProperty(name='Hole Diameter', description='Diameter of the hole', default=0.5, min=0.0, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_thickness: FloatProperty(name='Thickness', min=0.01, max=1000, default=0.25, subtype='DISTANCE', unit='LENGTH')

	val_height: FloatProperty(name='Height', description='Height of the cylinder', default=1, min=0.0001, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_origin: EnumProperty(name='Origin', description='The origin point of the cylinder mesh', default=MESH_VERTICAL_ALIGNMENT_BOTTOM, items=MeshVerticalAlignment)

	val_amount: FloatProperty(name='Amount', default=math.radians(360), min=math.radians(0.1), max=math.radians(360), subtype='ANGLE', unit='ROTATION')
	val_rotation: FloatProperty(name='Rotation', default=math.radians(0), min=math.radians(0.1), max=math.radians(360), subtype='ANGLE', unit='ROTATION')

	val_majorSegments: IntProperty(name='Segments', default=32, min=3, max=128, subtype='NONE')
	val_holeSegments: IntProperty(name='Hole Segments', default=32, min=3, max=128, subtype='NONE')



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
			col.prop(self, 'val_thickness', text=romly_utils.translate('Thickness', 'IFACE'))	# 'Thickness'はBlender内部の辞書で『幅』に翻訳されてしまうので、自前で翻訳
		elif self.val_diameterMethod == DONUT_CYLINDER_DIAMETER_METHOD_HOLE_AND_THICKNESS:
			row = col.row()
			row.alignment = 'RIGHT'
			row.label(text='Diameter: {value}'.format(value=romly_utils.units_to_string(value=(self.val_holeDiameter + self.val_thickness * 2))))
			col.prop(self, 'val_holeDiameter')
			col.prop(self, 'val_thickness', text=romly_utils.translate('Thickness', 'IFACE'))	# 'Thickness'はBlender内部の辞書で『幅』に翻訳されてしまうので、自前で翻訳
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



	def invoke(self, context, event):
		return self.execute(context)



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
			romly_utils.report(self, 'WARNING', msg_key='The hole diameter must be smaller than the outer diameter')
			return {'CANCELLED'}
		elif holeRadius < 0:
			romly_utils.report(self, 'WARNING', msg_key='The hole diameter must be larger than zero')
			return {'CANCELLED'}


		# 選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# シリンダーを生成
		bpy.ops.mesh.primitive_cylinder_add(vertices=self.val_majorSegments, radius=majorRadius, depth=self.val_height, end_fill_type='NGON', enter_editmode=False, location=bpy.context.scene.cursor.location)
		cylinderObject = bpy.data.objects[bpy.context.active_object.name]

		# 穴となるシリンダーを生成してブーリアン
		if holeRadius > 0:
			bpy.ops.mesh.primitive_cylinder_add(vertices=self.val_holeSegments, radius=holeRadius, depth=self.val_height * 2, end_fill_type='NGON', enter_editmode=False, location=bpy.context.scene.cursor.location)
			holeCylinderObject = bpy.data.objects[bpy.context.active_object.name]
			romly_utils.apply_boolean_object(object=cylinderObject, boolObject=holeCylinderObject, unlink=True)

		# 作成する分量が360度以下の場合
		if self.val_amount < math.radians(360):
			# ブーリアン用のメッシュを作成
			subtructMesh = CreatePieCutMesh(amountAngle=self.val_amount, rotateAngle=self.val_rotation)
			bpy.context.collection.objects.link(subtructMesh)
			romly_utils.apply_boolean_object(object=cylinderObject, boolObject=subtructMesh, unlink=True)


		# 原点位置の設定に従ってずらす
		if self.val_origin == MESH_VERTICAL_ALIGNMENT_TOP:
			romly_utils.translate_vertices(object=cylinderObject, vector=mathutils.Vector([0, 0, -self.val_height / 2]))
		elif self.val_origin == MESH_VERTICAL_ALIGNMENT_BOTTOM:
			romly_utils.translate_vertices(object=cylinderObject, vector=mathutils.Vector([0, 0, self.val_height / 2]))

		# 選択
		cylinderObject.select_set(state=True)

		cylinderObject.name = f"{bpy.app.translations.pgettext_data('Donut Cylinder')} {romly_utils.units_to_string(value=majorRadius * 2, removeSpace=True)}/{romly_utils.units_to_string(value=holeRadius * 2, removeSpace=True)}"

		return {'FINISHED'}





# 親となるメニュー
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_donut_cylinder.bl_idname, text=bpy.app.translations.pgettext_iface('Add Donut Cylinder'), icon='MESH_CYLINDER')





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')




classes = [
	ROMLYADDON_OT_add_donut_cylinder,
	ROMLYADDON_MT_romly_add_mesh_menu_parent,
]





def register():
	# クラスと翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.append(menu_func)





def unregister():
	# クラスと翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
