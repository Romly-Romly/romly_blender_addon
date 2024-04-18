import bpy
import mathutils
import bmesh
from bpy.props import *














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
			self.report({'WARNING'}, 'Please select the object to which the modifiers are to be applied')
			return {'CANCELLED'}
		else:
			obj = obj = bpy.context.active_object
			if len(obj.modifiers) == 0:
				# モデファイアが一つもない
				self.report({'WARNING'}, 'The object has no modifiers')
				return {'CANCELLED'}

			# すべてのモデファイアを適用
			for modifier in obj.modifiers:
				bpy.ops.object.modifier_apply(modifier=modifier.name)
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
	# 翻訳辞書の登録
	try:
		bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)
	except ValueError:
		bpy.app.translations.unregister(__name__)
		bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)

	# blenderへのクラス登録処理
	for cls in classes:
		bpy.utils.register_class(cls)

	# オブジェクトのコンテキストメニューに追加
	bpy.types.VIEW3D_MT_object_context_menu.append(object_context_menu_func)




# クラスの登録解除
def unregister():
	bpy.types.VIEW3D_MT_object_context_menu.remove(object_context_menu_func)

	# クラスの登録解除
	for cls in classes:
		bpy.utils.unregister_class(cls)

	# 翻訳辞書の登録解除
	bpy.app.translations.unregister(__name__)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()
