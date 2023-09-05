import bpy
import os




class ROMLYADDON_OT_export_selection_as_stl(bpy.types.Operator):
	"""
	選択されているオブジェクトをSTLファイルとして出力するオペレーター。
	"""
	bl_idname = "romlyaddon.export_selection_as_stl"
	bl_label = "Export Selection as STL"
	bl_description = '選択されているオブジェクトをSTLファイルとして出力する。'
	bl_options = {'REGISTER', 'UNDO'}



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		# 編集中のファイルに名前がついてないとダメ
		filepath = bpy.data.filepath
		if not filepath:
			bpy.context.window_manager.popup_menu(
				lambda self, context: self.layout.label(text='先に編集中のファイルを保存して下さい'), title="エラー", icon='ERROR')
			return {'CANCELLED'}

		# エクスポートするSTLのファイル名を作る。
		# blendファイル名 + " - " + オブジェクト名 + ".stl"
		stl_filepath = os.path.splitext(filepath)[0] + " - " + bpy.context.active_object.name + ".stl"

		# STLとしてエクスポート
		bpy.ops.export_mesh.stl(filepath=stl_filepath, check_existing=True, use_selection=True, ascii=True)

		msg = f"選択されているオブジェクトをファイル {stl_filepath} にエクスポートしました"
		bpy.context.window_manager.popup_menu(
			lambda self, context: self.layout.label(text=msg), title=self.bl_label, icon='INFO')
		return {'FINISHED'}





# アウトライナーのオブジェクトの右クリックに追加するメニュー
class ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent"
	bl_label = "Romly Tools"
	bl_description = "Romly Addon Menu"

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_export_selection_as_stl.bl_idname, icon='EXPORT')





# オブジェクトの右クリックメニューに登録
def outliner_object_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	bpy.utils.register_class(ROMLYADDON_OT_export_selection_as_stl)
	bpy.utils.register_class(ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent)

	# コレクションを右クリックしたときに表示されるメニューに追加
	bpy.types.OUTLINER_MT_object.append(outliner_object_menu_func)





# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLYADDON_OT_export_selection_as_stl)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent)
	bpy.types.OUTLINER_MT_object.remove(outliner_object_menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()

