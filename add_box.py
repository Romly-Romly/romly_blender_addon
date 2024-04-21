import bpy
import mathutils
import bmesh
from bpy.props import *

from . import romly_utils










class ROMLYADDON_OT_add_box(bpy.types.Operator):
	"""直方体メッシュを作成するオペレーター"""
	bl_idname = 'romlyaddon.add_box'
	bl_label = bpy.app.translations.pgettext_iface('Add Box')
	bl_description = 'Construct a cuboid mesh'
	bl_options = {'REGISTER', 'UNDO'}

	ORIGIN_X_ITEMS = [
		('0.5', 'Left', 'Set the X coordinate of the origin to the left surface'),
		('0', 'Center', 'Set the X coordinate of the origin to the center'),
		('-0.5', 'Right', 'Set the X coordinate of the origin to the right surface')
	]
	ORIGIN_Y_ITEMS = [
		('0.5', 'Front', 'Set the Y coordinate of the origin to the front surface'),
		('0', 'Center', 'Set the Y coordinate of the origin to the center'),
		('-0.5', 'Back', 'Set the Y coordinate of the origin to the back surface')
	]
	ORIGIN_Z_ITEMS = [
		('-0.5', 'Top', 'Set the Z coordinate of the origin to the top surface'),
		('0', 'Center', 'Set the Z coordinate of the origin to the center'),
		('0.5', 'Bottom', 'Set the Z coordinate of the origin to the bottom surface')
	]

	# プロパティ
	val_size: FloatVectorProperty(name='Size', description='Size of the cuboid', default=[10, 10, 10], soft_min=-1000.0, soft_max=1000.0, size=3, subtype='TRANSLATION', unit='LENGTH')
	val_origin_x: EnumProperty(name='X', description='X coordinate of the origin', default='0', items=ORIGIN_X_ITEMS)
	val_origin_y: EnumProperty(name='Y', description='Y coordinate of the origin', default='0', items=ORIGIN_Y_ITEMS)
	val_origin_z: EnumProperty(name='Z', description='Z coordinate of the origin', default='0', items=ORIGIN_Z_ITEMS)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col.prop(self, 'val_size')
		col.separator()

		col.label(text='Origin')
		row = col.row(align=True)
		row.prop(self, 'val_origin_x', expand=True)
		row = col.row(align=True)
		row.prop(self, 'val_origin_y', expand=True)
		row = col.row(align=True)
		row.prop(self, 'val_origin_z', expand=True)



	def execute(self, context):
		vertices = [
			mathutils.Vector([-0.5, -0.5, -0.5]),	# 0 正面 左下
			mathutils.Vector([-0.5, -0.5, 0.5]),	# 1 正面 左上
			mathutils.Vector([-0.5, 0.5, -0.5]),	# 2 奥 左下
			mathutils.Vector([-0.5, 0.5, 0.5]),		# 3 奥 左上
			mathutils.Vector([0.5, -0.5, -0.5]),	# 4 正面 右下
			mathutils.Vector([0.5, -0.5, 0.5]),		# 5 正面 右上
			mathutils.Vector([0.5, 0.5, -0.5]),		# 6 奥 右下
			mathutils.Vector([0.5, 0.5, 0.5])		# 7 奥 右上
		]
		faces = [
			(1, 5, 4, 0),	# 正面
			(3, 7, 6, 2),	# 背面
			(1, 3, 2, 0),	# 左側面
			(5, 7, 6, 4),	# 右側面
			(0, 4, 6, 2),	# 底面
			(1, 5, 7, 3),	# 上面
		]

		# 設定に従った頂点を生成
		offset = mathutils.Vector([float(self.val_origin_x), float(self.val_origin_y), float(self.val_origin_z)])
		box_vertices = [(v + offset) * self.val_size for v in vertices]

		obj_name = 'Cube' if self.val_size[0] == self.val_size[1] and self.val_size[1] == self.val_size[2] else 'Cuboid'
		obj = romly_utils.cleanup_mesh(romly_utils.create_object(box_vertices, faces, name=bpy.app.translations.pgettext_data(obj_name)))
		bpy.context.collection.objects.link(obj)

		# オブジェクトを3Dカーソル位置へ移動
		obj.location = bpy.context.scene.cursor.location

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}





# 親となるメニュー
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_box.bl_idname, text=bpy.app.translations.pgettext_iface('Add Box'), icon='MESH_CUBE')





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_box,
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
