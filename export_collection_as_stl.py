import bpy
import os



from . import romly_utils










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











def export_stl_compatible(filepath: str) -> bool:
	"""
	メッシュをSTLでエクスポートする関数。 Blender 4.2 でのAPI変更に対応。

	Parameters
	----------
	filepath : str
		エクスポート先のファイルパス。

	Returns
	-------
	bool
		エクスポートが成功したかどうか。
	"""
	# Blenderのバージョンを取得
	major, minor, _ = bpy.app.version

	# オプション指定
	check_existing = True # 既存ファイルをチェックするかどうか
	use_selection = True # 選択されたオブジェクトのみをエクスポートするかどうか。
	ascii = True	# ASCIIフォーマットで保存するかどうか

	# バージョン4.2以降かどうかをチェック
	if (major, minor) >= (4, 2):
		# 新しいメソッドを使用
		result = bpy.ops.wm.stl_export(filepath=filepath, check_existing=check_existing, export_selected_objects=use_selection, ascii_format=ascii)
	else:
		# 古いメソッドを使用
		result = bpy.ops.export_mesh.stl(filepath=filepath, check_existing=check_existing, use_selection=use_selection, ascii=ascii)

	# OPERATORクラスの戻り値をチェック
	return 'FINISHED' in result










# MARK: Class
class ROMLYADDON_OT_export_collection_as_stl(bpy.types.Operator):
	"""
	コレクション内のメッシュをSTLファイルとして出力するオペレーター。
	"""
	bl_idname = 'romlyaddon.export_collection_as_stl'
	bl_label = bpy.app.translations.pgettext_iface('Export Collection as STL')
	bl_description = 'Export all meshes in this collection as an STL file. The sub collections that were excluded from the layer view will be excluded.'
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
				lambda self, context: self.layout.label(text='Please save the active file first'), title="Error", icon='ERROR')
			return {'CANCELLED'}

		# エクスポートするSTLのファイル名を作る。
		# blendファイル名 + " - " + コレクション名 + ".stl"
		stl_filepath = os.path.splitext(filepath)[0] + " - " + bpy.context.collection.name + ".stl"
		export_stl_compatible(filepath=stl_filepath)

		msg_key = 'The collection {collection} is exported to: {filename}'
		params = {'collection': bpy.context.view_layer.active_layer_collection.name, 'filename': stl_filepath}

		# ポップアップで表示
		msg = bpy.app.translations.pgettext_iface(msg_key).format(**params)
		bpy.context.window_manager.popup_menu(
			lambda self, context: self.layout.label(text=msg), title=bpy.app.translations.pgettext_iface('Export Collection as STL'), icon='INFO')

		# リポートにも表示
		romly_utils.report(self, 'INFO', msg_key=msg_key, params=params)

		return {'FINISHED'}










# MARK: Class
class ROMLYADDON_OT_export_selection_as_stl(bpy.types.Operator):
	"""
	選択されているオブジェクトをSTLファイルとして出力するオペレーター。
	"""
	bl_idname = 'romlyaddon.export_selection_as_stl'
	bl_label = bpy.app.translations.pgettext_iface('Export Selection as STL')
	bl_description = 'Export the selected objects as an STL file'
	bl_options = {'REGISTER', 'UNDO'}



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		# 編集中のファイルに名前がついてないとダメ
		filepath = bpy.data.filepath
		if not filepath:
			bpy.context.window_manager.popup_menu(
				lambda self, context: self.layout.label(text='Please save the active file first'), title='Error', icon='ERROR')
			return {'CANCELLED'}

		# エクスポートするSTLのファイル名を作る。
		# blendファイル名 + " - " + オブジェクト名 + ".stl"
		stl_filepath = os.path.splitext(filepath)[0] + " - " + bpy.context.active_object.name + ".stl"

		# STLとしてエクスポート
		export_stl_compatible(filepath=stl_filepath)

		msg_key = 'The selection is exported to: {filename}'
		params = {'filename': stl_filepath}

		# ポップアップで表示
		msg = bpy.app.translations.pgettext_iface(msg_key).format(**params)
		bpy.context.window_manager.popup_menu(
			lambda self, context: self.layout.label(text=msg), title=self.bl_label, icon='INFO')

		# リポートにも表示
		romly_utils.report(self, 'INFO', msg_key=msg_key, params=params)

		return {'FINISHED'}










class ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent(bpy.types.Menu):
	"""コレクションの右クリックに追加するメニュー"""
	bl_idname = 'ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent'
	bl_label = 'Romly Tools'
	bl_description = 'Romly Addon Menu'

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_export_collection_as_stl.bl_idname, text=bpy.app.translations.pgettext_iface('Export Collection as STL'), icon='EXPORT')





# コレクションメニューに登録
def collection_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent.bl_idname, icon='NONE')










class ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent(bpy.types.Menu):
	"""アウトライナーのオブジェクトの右クリックに追加するメニュー"""
	bl_idname = 'ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent'
	bl_label = 'Romly Tools'
	bl_description = 'Romly Addon Menu'

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_export_selection_as_stl.bl_idname, text=bpy.app.translations.pgettext_iface('Export Selection as STL'), icon='EXPORT')





# オブジェクトの右クリックメニューに登録
def outliner_object_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent.bl_idname, icon='NONE')










classes = [
	ROMLYADDON_OT_export_collection_as_stl,
	ROMLYADDON_OT_export_selection_as_stl,
	ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent,
	ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent,
]



def register():
	# クラスと翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	# コレクションを右クリックしたときに表示されるメニューに追加
	bpy.types.OUTLINER_MT_collection.append(collection_menu_func)

	# アウトライナーでオブジェクトを右クリックしたときに表示されるメニューに追加
	bpy.types.OUTLINER_MT_object.append(outliner_object_menu_func)





def unregister():
	# クラスと翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.OUTLINER_MT_collection.remove(collection_menu_func)
	bpy.types.OUTLINER_MT_object.remove(outliner_object_menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
