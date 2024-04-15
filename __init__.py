bl_info = {
	'name': 'Romly Blender Add-on',
	'version': (1, 0, 0),
	'blender': (4, 0, 0),
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
from .add_sphericon import ROMLYADDON_OT_add_sphericon
from .add_oloid import ROMLYADDON_OT_add_oloid
from .add_aluminum_extrusion import ROMLYADDON_OT_add_aluminum_extrusion
from .add_pinheader import ROMLYADDON_OT_add_pinheader
from .export_collection_as_stl import ROMLYADDON_OT_export_collection_as_stl
from .export_selection_as_stl import ROMLYADDON_OT_export_selection_as_stl
from .select_edges_on_fair_surface import ROMLYADDON_OT_select_edges_on_fair_surface
from .language_panel import ROMLYADDON_PT_language_panel, ROMLYADDON_OT_change_language
from .romly_translation import TRANSLATION_DICT





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





def view3d_edit_mesh_edges_menu_func(self, context):
	"""編集モードのエッジメニューに追加する関数。平面上にある辺を選択する項目を追加"""
	self.layout.separator()
	self.layout.operator(ROMLYADDON_OT_select_edges_on_fair_surface.bl_idname, text=bpy.app.translations.pgettext_iface(ROMLYADDON_OT_select_edges_on_fair_surface.bl_label), icon='EDGESEL')





def view3d_edit_mesh_context_menu_func(self, context):
	"""
	編集モードのコンテキストメニュー（右クリックメニュー）に追加する関数。
	平面上にある辺を選択する項目を、辺モードの時のみ追加。
	"""
	# 辺モードの時のみメニュー項目を追加（0=頂点, 1=辺, 2=面）
	if bpy.context.tool_settings.mesh_select_mode[1]:
		self.layout.separator()
		self.layout.operator(ROMLYADDON_OT_select_edges_on_fair_surface.bl_idname, text=bpy.app.translations.pgettext_iface(ROMLYADDON_OT_select_edges_on_fair_surface.bl_label), icon='EDGESEL')





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

		OPERATORS = [
			(ROMLYADDON_OT_add_box, None, 'MESH_CUBE'),
			(ROMLY_OT_add_donut_cylinder, None, 'MESH_CYLINDER'),
			(ROMLYADDON_OT_add_cross_extrusion, None, 'ADD'),
			(ROMLYADDON_OT_add_reuleaux_polygon, None, 'MESH_CIRCLE'),
			(ROMLYADDON_OT_add_reuleaux_tetrahedron, 'Add Reuleaux Tetrahedron', 'MESH_CONE'),
			(ROMLYADDON_OT_add_sphericon, 'Add Sphericon', 'MESH_CAPSULE'),
			(ROMLYADDON_OT_add_oloid, 'Add Oloid', 'MESH_CAPSULE'),
			(None, None, None),
			(ROMLYADDON_OT_add_aluminum_extrusion, 'Add Aluminium Extrusion', 'FIXED_SIZE'),
			(ROMLYADDON_OT_add_pinheader, 'Add Pinheader', 'EMPTY_SINGLE_ARROW'),
		]
		for operator, text, icon in OPERATORS:
			if operator is None:
				layout.separator()
			elif text:
				layout.operator(operator.bl_idname, text=bpy.app.translations.pgettext_iface(text), icon=icon)
			else:
				layout.operator(operator.bl_idname, icon=icon)





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





MY_CLASS_LIST = [
	ROMLYADDON_OT_apply_all_modifiers,
	ROMLYADDON_OT_add_fixed_count_array_modifier,
	ROMLYADDON_MT_romly_tool_menu_parent,
	ROMLYADDON_OT_add_box,
	ROMLY_OT_add_donut_cylinder,
	ROMLYADDON_OT_add_cross_extrusion,
	ROMLYADDON_OT_add_reuleaux_polygon,
	ROMLYADDON_OT_add_reuleaux_tetrahedron,
	ROMLYADDON_OT_add_sphericon,
	ROMLYADDON_OT_add_oloid,
	ROMLYADDON_OT_add_aluminum_extrusion,
	ROMLYADDON_OT_add_pinheader,
	ROMLYADDON_MT_romly_add_mesh_menu_parent,
	ROMLYADDON_OT_export_collection_as_stl,
	ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent,
	ROMLYADDON_OT_export_selection_as_stl,
	ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent,
	ROMLYADDON_OT_select_edges_on_fair_surface,
	ROMLYADDON_PT_language_panel,
	ROMLYADDON_OT_change_language,
]

# blenderへのクラス登録処理
def register():
	# 翻訳辞書の登録
	bpy.app.translations.register(__name__, TRANSLATION_DICT)

	for cls in MY_CLASS_LIST:
		bpy.utils.register_class(cls)

	# それぞれのメニューに独自メニューを登録
	bpy.types.VIEW3D_MT_object_context_menu.append(object_menu_func)
	bpy.types.VIEW3D_MT_add.append(add_menu_func)
	bpy.types.OUTLINER_MT_collection.append(collection_menu_func)
	bpy.types.OUTLINER_MT_object.append(outliner_object_menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_edges.append(view3d_edit_mesh_edges_menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(view3d_edit_mesh_context_menu_func)





# クラスの登録解除
def unregister():
	bpy.types.VIEW3D_MT_object_context_menu.remove(object_menu_func)
	bpy.types.VIEW3D_MT_add.remove(add_menu_func)
	bpy.types.OUTLINER_MT_collection.remove(collection_menu_func)
	bpy.types.OUTLINER_MT_object.remove(outliner_object_menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_edges.remove(view3d_edit_mesh_edges_menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(view3d_edit_mesh_context_menu_func)

	for cls in MY_CLASS_LIST:
		bpy.utils.unregister_class(cls)

	# 翻訳辞書の登録解除
	bpy.app.translations.unregister(__name__)
