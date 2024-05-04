import bpy
import bmesh
from bpy.props import *
import mathutils

from . import romly_utils










def create_cross_extrusion(hLineLength, hLineThickness, vLineLength, vLineThickness, height):
	"""十字を掃引したオブジェクトを生成して返す

	Parameters
	----------
	hLineLength : Float
		横線の長さ
	hLineThickness : Float
		横線の幅
	vLineLength : Float
		縦線の長さ
	vLineThickness : Float
		縦線の幅
	height : Float
		高さ
	"""
	vertices = []
	faces = []

	# 十字の縦線の左上から反時計回り
	if vLineThickness > 0:
		vertices.append(mathutils.Vector([-vLineThickness / 2, vLineLength / 2, 0]))
	vertices.append(mathutils.Vector([-vLineThickness / 2, hLineThickness / 2, 0]))
	if hLineThickness > 0:
		vertices.append(mathutils.Vector([-hLineLength / 2, hLineThickness / 2, 0]))
		vertices.append(mathutils.Vector([-hLineLength / 2, -hLineThickness / 2, 0]))
	vertices.append(mathutils.Vector([-vLineThickness / 2, -hLineThickness / 2, 0]))
	if vLineThickness > 0:
		vertices.append(mathutils.Vector([-vLineThickness / 2, -vLineLength / 2, 0]))

	if vLineThickness > 0:
		vertices.append(mathutils.Vector([vLineThickness / 2, -vLineLength / 2, 0]))
	vertices.append(mathutils.Vector([vLineThickness / 2, -hLineThickness / 2, 0]))
	if hLineThickness > 0:
		vertices.append(mathutils.Vector([hLineLength / 2, -hLineThickness / 2, 0]))
		vertices.append(mathutils.Vector([hLineLength / 2, hLineThickness / 2, 0]))
	vertices.append(mathutils.Vector([vLineThickness / 2, hLineThickness / 2, 0]))
	if vLineThickness > 0:
		vertices.append(mathutils.Vector([vLineThickness / 2, vLineLength / 2, 0]))

	faces.append(list(range(len(vertices))))

	# 掃引
	if height > 0:
		romly_utils.extrude_face(vertices=vertices, faces=faces, extrude_vertex_indices=faces[0], z_offset=height)

	obj = romly_utils.create_object(vertices=vertices, faces=faces, name='Extuded Cross')
	romly_utils.cleanup_mesh(object=obj)
	return obj





class ROMLYADDON_OT_add_cross_extrusion(bpy.types.Operator):
	bl_idname = "romlyaddon.add_cross_extrusion"
	bl_label = "Add Cross Extrusion"
	bl_description = '十字をZ方向に掃引したメッシュを作成します'
	bl_options = {'REGISTER', 'UNDO'}



	MESH_VERTICAL_ALIGNMENT_TOP = 'top'
	MESH_VERTICAL_ALIGNMENT_MIDDLE = 'middle'
	MESH_VERTICAL_ALIGNMENT_BOTTOM = 'bottom'

	MESH_VERTICAL_ALIGNMENT = [
		(MESH_VERTICAL_ALIGNMENT_TOP, 'Top', 'Set origin to top'),
		(MESH_VERTICAL_ALIGNMENT_MIDDLE, 'Middle', 'Set origin to center'),
		(MESH_VERTICAL_ALIGNMENT_BOTTOM, 'Bottom', 'Set origin to bottom')
	]


	# プロパティ
	val_hLineLength: FloatProperty(name='Horizontal Line Length', description='横線の長さ', default=3.0, min=0.0, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_hLineThickness: FloatProperty(name='Horizontal Line Thickness', description='横線の厚み', default=1.0, min=0, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_vLineLength: FloatProperty(name='Vertical Line Length', description='縦線の長さ', default=3.0, min=0.0, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_vLineThickness: FloatProperty(name='Vertical Line Thickness', description='縦線の厚み', default=1.0, min=0, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_height: FloatProperty(name='Height', description='高さ', default=1.0, min=0, max=1000, subtype='DISTANCE', unit='LENGTH')
	val_origin: EnumProperty(name='Origin', description='原点位置', default=MESH_VERTICAL_ALIGNMENT_BOTTOM, items=MESH_VERTICAL_ALIGNMENT)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col.label(text="Horizontal Line")
		row = col.row(align=True)
		row.prop(self, 'val_hLineLength', text='Length')
		row.prop(self, 'val_hLineThickness', text=romly_utils.translate('Thickness', 'IFACE'))	# 'Thickness'はBlender内部の辞書で『幅』に翻訳されてしまうので、自前で翻訳

		col.label(text="Vertical Line")
		row = col.row(align=True)
		row.prop(self, 'val_vLineLength', text='Length')
		row.prop(self, 'val_vLineThickness', text=romly_utils.translate('Thickness', 'IFACE'))	# 'Thickness'はBlender内部の辞書で『幅』に翻訳されてしまうので、自前で翻訳
		col.separator()

		col.prop(self, 'val_height')
		row = col.row(align=True)
		row.label(text='Origin')
		row.prop(self, 'val_origin', expand=True)



	def execute(self, context):
		# 選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# オブジェクトを生成
		extrudedCrossObject = create_cross_extrusion(hLineLength=self.val_hLineLength, hLineThickness=self.val_hLineThickness, vLineLength=self.val_vLineLength, vLineThickness=self.val_vLineThickness, height=self.val_height)
		extrudedCrossObject.name = 'Cross Extrusion'
		bpy.context.collection.objects.link(extrudedCrossObject)

		# 原点位置の設定に従ってずらす
		if self.val_origin == ROMLYADDON_OT_add_cross_extrusion.MESH_VERTICAL_ALIGNMENT_TOP:
			romly_utils.translate_vertices(object=extrudedCrossObject, vector=mathutils.Vector([0, 0, -self.val_height]))
		elif self.val_origin == ROMLYADDON_OT_add_cross_extrusion.MESH_VERTICAL_ALIGNMENT_MIDDLE:
			romly_utils.translate_vertices(object=extrudedCrossObject, vector=mathutils.Vector([0, 0, -self.val_height / 2]))

		# オブジェクトを3Dカーソル位置へ移動
		extrudedCrossObject.location = bpy.context.scene.cursor.location

		# 選択
		extrudedCrossObject.select_set(state=True)
		bpy.context.view_layer.objects.active = extrudedCrossObject

		return {'FINISHED'}





# 親となるメニュー
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_cross_extrusion.bl_idname, icon='ADD')





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_cross_extrusion,
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
