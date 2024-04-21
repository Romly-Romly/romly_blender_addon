import bpy
from bpy.props import *



from . import romly_utils










class ROMLYADDON_OT_reload_and_run_script(bpy.types.Operator):
	bl_idname = 'romlyaddon.reload_and_run_script'
	bl_label = bpy.app.translations.pgettext_iface('Reload and Run Script')
	bl_description = 'Reload active script from disk and run'
	bl_options = {'REGISTER', 'UNDO'}



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
#		bpy.ops.script.reload()
		bpy.ops.text.resolve_conflict(resolution='RELOAD')
		bpy.ops.text.run_script()
		return {'FINISHED'}










def text_context_menu_func(self, context):
	self.layout.separator()
	self.layout.operator(ROMLYADDON_OT_reload_and_run_script.bl_idname, text=bpy.app.translations.pgettext_iface('Reload and Run Script'), icon='FILE_SCRIPT')





classes = [
	ROMLYADDON_OT_reload_and_run_script,
]





def register():
	# クラスと翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	# テキストエディタのコンテキストメニューに追加
	bpy.types.TEXT_MT_context_menu.append(text_context_menu_func)





def unregister():
	# クラスと翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.TEXT_MT_context_menu.remove(text_context_menu_func)






# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
