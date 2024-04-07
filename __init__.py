bl_info = {
	'name': 'Romly Blender Add-on',
	'version': (0, 7, 0),
	'blender': (3, 5, 0),
	'category': 'Object',
	'author': 'Romly',
	'doc_url': 'https://github.com/Romly-Romly/romly_blender_addon'
}


import bpy
from .apply_all_modifiers import ROMLYADDON_OT_apply_all_modifiers
from .add_fixed_count_array_modifier import ROMLYADDON_OT_add_fixed_count_array_modifier
from .add_box import ROMLYADDON_OT_add_box
from .add_donut_cylinder import ROMLY_OT_add_donut_cylinder
from .add_cross_extrusion import ROMLYADDON_OT_add_cross_extrusion
from .add_reuleaux_polygon import ROMLYADDON_OT_add_reuleaux_polygon
from .add_reuleaux_tetrahedron import ROMLYADDON_OT_add_reuleaux_tetrahedron
from .add_pinheader import ROMLYADDON_OT_add_pinheader
from .export_collection_as_stl import ROMLYADDON_OT_export_collection_as_stl
from .export_selection_as_stl import ROMLYADDON_OT_export_selection_as_stl





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
		layout.operator(ROMLY_OT_add_donut_cylinder.bl_idname, icon='MESH_CYLINDER')
		layout.operator(ROMLYADDON_OT_add_cross_extrusion.bl_idname, icon='ADD')
		layout.operator(ROMLYADDON_OT_add_reuleaux_polygon.bl_idname, icon='MESH_CIRCLE')
		layout.operator(ROMLYADDON_OT_add_reuleaux_tetrahedron.bl_idname, icon='MESH_CONE')
		layout.operator(ROMLYADDON_OT_add_pinheader.bl_idname, icon='EMPTY_SINGLE_ARROW')





# Addメニューに登録
def add_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





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
	bpy.utils.register_class(ROMLYADDON_OT_apply_all_modifiers)
	bpy.utils.register_class(ROMLYADDON_OT_add_fixed_count_array_modifier)
	bpy.utils.register_class(ROMLYADDON_MT_romly_tool_menu_parent)

	bpy.utils.register_class(ROMLYADDON_OT_add_box)
	bpy.utils.register_class(ROMLY_OT_add_donut_cylinder)
	bpy.utils.register_class(ROMLYADDON_OT_add_cross_extrusion)
	bpy.utils.register_class(ROMLYADDON_OT_add_reuleaux_polygon)
	bpy.utils.register_class(ROMLYADDON_OT_add_reuleaux_tetrahedron)
	bpy.utils.register_class(ROMLYADDON_OT_add_pinheader)
	bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)

	bpy.utils.register_class(ROMLYADDON_OT_export_collection_as_stl)
	bpy.utils.register_class(ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent)

	bpy.utils.register_class(ROMLYADDON_OT_export_selection_as_stl)
	bpy.utils.register_class(ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent)

	# それぞれのメニューに独自メニューを登録
	bpy.types.VIEW3D_MT_object_context_menu.append(object_menu_func)
	bpy.types.VIEW3D_MT_add.append(add_menu_func)
	bpy.types.OUTLINER_MT_collection.append(collection_menu_func)
	bpy.types.OUTLINER_MT_object.append(outliner_object_menu_func)





# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLYADDON_OT_apply_all_modifiers)
	bpy.utils.unregister_class(ROMLYADDON_OT_add_fixed_count_array_modifier)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_tool_menu_parent)

	bpy.utils.unregister_class(ROMLYADDON_OT_add_box)
	bpy.utils.unregister_class(ROMLY_OT_add_donut_cylinder)
	bpy.utils.unregister_class(ROMLYADDON_OT_add_cross_extrusion)
	bpy.utils.unregister_class(ROMLYADDON_OT_add_reuleaux_polygon)
	bpy.utils.unregister_class(ROMLYADDON_OT_add_reuleaux_tetrahedron)
	bpy.utils.unregister_class(ROMLYADDON_OT_add_pinheader)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)

	bpy.utils.unregister_class(ROMLYADDON_OT_export_collection_as_stl)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent)

	bpy.utils.unregister_class(ROMLYADDON_OT_export_selection_as_stl)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent)

	bpy.types.VIEW3D_MT_object_context_menu.remove(object_menu_func)
	bpy.types.VIEW3D_MT_add.remove(add_menu_func)
	bpy.types.OUTLINER_MT_collection.remove(collection_menu_func)
	bpy.types.OUTLINER_MT_object.remove(outliner_object_menu_func)
