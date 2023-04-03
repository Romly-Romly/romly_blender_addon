import bpy
import mathutils
import bmesh
from bpy.props import *





def create_object(vertices, faces, name, mesh_name=None):
	"""
	指定された頂点リストと面リストから新しいオブジェクトを生成する。

	Parameters
	----------
	vertices : list of tuple of float
		オブジェクトの頂点座標のリスト。
	faces : list of tuple of int
		オブジェクトの面を構成する頂点のインデックスのリスト。
	name : str
		作成されるオブジェクトの名前。
	mesh_name : str, optional
		作成されるメッシュデータの名前。デフォルトでは、オブジェクト名に '_mesh' を追加されたものになる。

	Returns
	-------
	bpy.types.Object
		作成されたオブジェクトのインスタンス。
	"""
	if mesh_name is None:
		mesh_name = name + '_mesh'
	mesh = bpy.data.meshes.new(mesh_name)
	mesh.from_pydata(vertices, [], faces)
	obj = bpy.data.objects.new(name, mesh)
	return obj





def cleanup_mesh(object: bpy.types.Object, remove_doubles=True, recalc_normals=True):
	"""
	メッシュオブジェクトの重複する頂点を削除し、法線を再計算することでメッシュをクリーンアップする。

	Parameters
	----------
	object : bpy.types.Object
		クリーンアップするメッシュオブジェクト
	remove_doubles : bool, optional
		True の場合、重複する頂点を削除します。デフォルトは True。
	recalc_normals : bool, optional
		True の場合、法線を再計算します。デフォルトは True。

	Returns
	-------
	bpy.types.Object
	"""
	bm = bmesh.new()
	bm.from_mesh(object.data)
	if remove_doubles:
		bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
	if recalc_normals:
		bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
	bm.to_mesh(object.data)
	bm.clear()
	object.data.update()
	bm.free()
	return object





class ROMLYADDON_OT_add_box(bpy.types.Operator):
	bl_idname = "romlyaddon.add_box"
	bl_label = "Add Box"
	bl_description = '直方体のメッシュを追加します'
	bl_options = {'REGISTER', 'UNDO'}

	ORIGIN_X_ITEMS = [
		('0.5', 'Left', 'X軸原点を左面に設定します'),
		('0', 'Center', 'X軸原点を中心に設定します'),
		('-0.5', 'Right', 'X軸原点を右面に設定します')
	]
	ORIGIN_Y_ITEMS = [
		('0.5', 'Front', 'Y軸原点を正面に設定します'),
		('0', 'Center', 'Y軸原点を中心に設定します'),
		('-0.5', 'Back', 'Y軸原点を背面に設定します')
	]
	ORIGIN_Z_ITEMS = [
		('-0.5', 'Top', 'Z軸原点を上面に設定します'),
		('0', 'center', 'Z軸原点を中心に設定します'),
		('0.5', 'Bottom', 'Z軸原点を底面に設定します')
	]

	# プロパティ
	val_size: FloatVectorProperty(name='Size', description='大きさ', default=[10, 10, 10], min=-100.0, max=100.0, size=3, subtype='TRANSLATION', unit='LENGTH')
	val_origin_x: EnumProperty(name='X', description='X軸原点位置', default='0', items=ORIGIN_X_ITEMS)
	val_origin_y: EnumProperty(name='Y', description='Y軸原点位置', default='0', items=ORIGIN_Y_ITEMS)
	val_origin_z: EnumProperty(name='Z', description='Z軸原点位置', default='0', items=ORIGIN_Z_ITEMS)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col.prop(self, 'val_size')
		col.separator()

		col.label(text="Origin")
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

		bpy.context.scene.cursor.location
		obj = cleanup_mesh(create_object(box_vertices, faces, name='Box'))
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
		layout.operator(ROMLYADDON_OT_add_box.bl_idname, icon='MESH_CUBE')





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	bpy.utils.register_class(ROMLYADDON_OT_add_box)
	bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLYADDON_OT_add_box)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()
