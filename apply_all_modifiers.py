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
	bl_idname = "romlyaddon.apply_all_modifiers"
	bl_label = "Apply All Modifiers"
	bl_description = 'すべてのモデファイアを適用します'
	bl_options = {'REGISTER', 'UNDO'}



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		# 選択されているオブジェクトを取得
		obj = bpy.context.active_object

		# すべてのモデファイアを適用
		for modifier in obj.modifiers:
			bpy.ops.object.modifier_apply({"object": obj}, modifier=modifier.name)
		return {'FINISHED'}






# 親となるメニュー
class ROMLYADDON_MT_apply_all_modifiers_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_apply_all_modifiers_menu_parent"
	bl_label = "Romly Tools"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_apply_all_modifiers.bl_idname, icon='CHECKMARK')





# オブジェクトの追加メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_apply_all_modifiers_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	bpy.utils.register_class(ROMLYADDON_OT_apply_all_modifiers)
	bpy.utils.register_class(ROMLYADDON_MT_apply_all_modifiers_menu_parent)
	bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)




# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLYADDON_OT_apply_all_modifiers)
	bpy.utils.unregister_class(ROMLYADDON_MT_apply_all_modifiers_menu_parent)
	bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()
