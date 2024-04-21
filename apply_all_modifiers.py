import bpy
import mathutils
import bmesh
from bpy.props import *



from . import romly_utils










class ROMLYADDON_OT_apply_all_modifiers(bpy.types.Operator):
	"""
	すべてのモデファイアを一度に適用するためのオペレータクラス。

	Attributes
	----------
	bl_idname : str
		オペレータの内部名。
	bl_label : str
		オペレータの表示名。
	bl_description : str
		オペレータの説明。
	bl_options : set
		オペレータのオプション。
	"""
	bl_idname = 'romlyaddon.apply_all_modifiers'
	bl_label = bpy.app.translations.pgettext_iface('Apply All Modifiers')
	bl_description = 'Apply all modifiers on the active object'
	bl_options = {'REGISTER', 'UNDO'}



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		# 選択されているオブジェクトを取得
		if len(bpy.context.selected_objects) == 0:
			# 選択されているオブジェクトがない
			romly_utils.report(self, 'WARNING', msg_key='Please select the object to which the modifiers are to be applied')
			return {'CANCELLED'}

		obj = obj = bpy.context.active_object
		if len(obj.modifiers) == 0:
			# モデファイアが一つもない
			romly_utils.report(self, 'WARNING', msg_key='The object has no modifiers')
			return {'CANCELLED'}

		# すべてのモデファイアを適用
		count = 0
		for modifier in obj.modifiers:
			bpy.ops.object.modifier_apply(modifier=modifier.name)
			count += 1
		romly_utils.report(self, 'INFO', msg_key='{count} modifiers were applied', params={'count': str(count)})

		return {'FINISHED'}










class ROMLYADDON_MT_object_context_menu_parent(bpy.types.Menu):
	"""親となるメニュー"""
	bl_idname = 'romlyaddon.object_context_menu_parent'
	bl_label = 'Romly Tools'
	bl_description = "Romly Addon Menu"

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_apply_all_modifiers.bl_idname, text=bpy.app.translations.pgettext_iface('Apply All Modifiers'), icon='CHECKMARK')





def object_context_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_object_context_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_apply_all_modifiers,
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

	# 翻訳辞書の登録解除
	bpy.app.translations.unregister(__name__)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
