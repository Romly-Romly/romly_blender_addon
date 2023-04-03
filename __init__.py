bl_info = {
	'name': 'Romly Blender Add-on',
	'blender': (3, 5, 0),
	'category': 'Object',
	'author': 'Romly'
}


import bpy
from .apply_all_modifiers import ROMLYADDON_OT_apply_all_modifiers
from .add_fixed_count_array_modifier import ROMLYADDON_OT_add_fixed_count_array_modifier
from .add_box import ROMLYADDON_OT_add_box





# オブジェクトの右クリックで表示するメニュー
class ROMLYADDON_MT_romly_tool_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_tool_menu_parent"
	bl_label = "Romly Tools"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_fixed_count_array_modifier.bl_idname, icon='MOD_ARRAY')
		layout.operator(ROMLYADDON_OT_apply_all_modifiers.bl_idname, icon='CHECKMARK')





# オブジェクトの右クリックメニューに登録
def object_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_tool_menu_parent.bl_idname, icon='NONE')





# Addメニューに追加するメニュー
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_box.bl_idname, icon='MESH_CUBE')





# Addメニューに登録
def add_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	bpy.utils.register_class(ROMLYADDON_OT_apply_all_modifiers)
	bpy.utils.register_class(ROMLYADDON_OT_add_fixed_count_array_modifier)
	bpy.utils.register_class(ROMLYADDON_MT_romly_tool_menu_parent)

	bpy.utils.register_class(ROMLYADDON_OT_add_box)
	bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)

	bpy.types.VIEW3D_MT_object_context_menu.append(object_menu_func)
	bpy.types.VIEW3D_MT_add.append(add_menu_func)





# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLYADDON_OT_apply_all_modifiers)
	bpy.utils.unregister_class(ROMLYADDON_OT_add_fixed_count_array_modifier)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_tool_menu_parent)

	bpy.utils.unregister_class(ROMLYADDON_OT_add_box)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)

	bpy.types.VIEW3D_MT_object_context_menu.remove(object_menu_func)
	bpy.types.VIEW3D_MT_add.remove(add_menu_func)
