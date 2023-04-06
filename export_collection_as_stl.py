import bpy
import os





def selectObjectsInChildren(layerCollection):
	"""
	コレクション内のメッシュを再帰的に選択する。
	"""
	if not layerCollection.exclude:
		for obj in layerCollection.collection.objects:
			# 最初は len(obj.data.polygons) > 0 という条件で面がないメッシュを弾いてたんだけど、モデファイアで作ったメッシュやパーティクルが選択されないので辞めた。
			if obj.type == 'MESH':
				obj.select_set(state=True)
		for child in layerCollection.children:
			selectObjectsInChildren(child)





class ROMLYADDON_OT_export_collection_as_stl(bpy.types.Operator):
	"""
	コレクション内のメッシュをSTLファイルとして出力するオペレーター。
	"""
	bl_idname = "romlyaddon.export_collection_as_stl"
	bl_label = "Export Collection as STL"
	bl_description = 'コレクション内のメッシュをSTLファイルとして出力する。レイヤービューから除外されているコレクションは出力しない'
	bl_options = {'REGISTER', 'UNDO'}



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# アクティブなコレクションの子を選択
		selectObjectsInChildren(bpy.context.view_layer.active_layer_collection)

		# 編集中のファイルに名前がついてないとダメ
		filepath = bpy.data.filepath
		if not filepath:
			bpy.context.window_manager.popup_menu(
				lambda self, context: self.layout.label(text='先に編集中のファイルを保存して下さい'), title="エラー", icon='ERROR')
			return {'CANCELLED'}

		# エクスポートするSTLのファイル名を作る。
		# blendファイル名 + " - " + コレクション名 + ".stl"
		stl_filepath = os.path.splitext(filepath)[0] + " - " + bpy.context.collection.name + ".stl"
		bpy.ops.export_mesh.stl(filepath=stl_filepath, check_existing=True, use_selection=True, ascii=True)

		msg = f"{bpy.context.view_layer.active_layer_collection.name} をファイル {stl_filepath} にエクスポートしました"
		bpy.context.window_manager.popup_menu(
			lambda self, context: self.layout.label(text=msg), title=self.bl_label, icon='INFO')
		return {'FINISHED'}





# コレクションの右クリックに追加するメニュー
class ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent"
	bl_label = "Romly Tools"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_export_collection_as_stl.bl_idname, icon='EXPORT')





# コレクションメニューに登録
def collection_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	bpy.utils.register_class(ROMLYADDON_OT_export_collection_as_stl)
	bpy.utils.register_class(ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent)

	# コレクションを右クリックしたときに表示されるメニューに追加
	bpy.types.OUTLINER_MT_collection.append(collection_menu_func)





# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLYADDON_OT_export_collection_as_stl)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent)
	bpy.types.OUTLINER_MT_collection.remove(collection_menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()
