import bpy
from bpy.props import *



from . import romly_utils










class ROMLYADDON_OT_toggle_viewport_display_as(bpy.types.Operator):
	bl_idname = 'romlyaddon.toggle_viewport_display_as'
	bl_label = bpy.app.translations.pgettext_iface('Toggle Viewport Display As')
	bl_description = 'Toggle Viewport Display As Wire/Textured'
	bl_options = {'REGISTER', 'UNDO'}



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		# オブジェクトが選択されてないとだめ
		if len(bpy.context.selected_objects) == 0:
			romly_utils.report(self, 'WARNING', msg_key='Please select an object to operate')
			return {'CANCELLED'}

		# アクティブオブジェクトがワイヤーフレーム表示以外ならワイヤーフレーム表示に、それ以外はテクスチャ表示に切り替える。
		new_display_type = 'TEXTURED'
		if bpy.context.selected_objects[0].display_type != 'WIRE':
			new_display_type = 'WIRE'

		for obj in bpy.context.selected_objects:
			obj.display_type = new_display_type

		return {'FINISHED'}










class ROMLYADDON_MT_object_context_menu_parent(bpy.types.Menu):
	"""親となるメニュー"""
	bl_idname = 'romlyaddon.object_context_menu_parent'
	bl_label = 'Romly Tools'
	bl_description = "Romly Addon Menu"

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_toggle_viewport_display_as.bl_idname, text=bpy.app.translations.pgettext_iface('Toggle Viewport Display As'), icon='SHADING_WIRE')





def object_context_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_object_context_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_toggle_viewport_display_as,
	ROMLYADDON_MT_object_context_menu_parent,
]





def register():
	# クラスと翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	# オブジェクトのコンテキストメニューに追加
	bpy.types.VIEW3D_MT_object_context_menu.append(object_context_menu_func)





def unregister():
	# クラスと翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_object_context_menu.remove(object_context_menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
