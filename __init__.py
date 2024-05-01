bl_info = {
	'name': 'Romly Blender Add-on',
	'version': (1, 7, 0),
	'blender': (4, 0, 0),
	'category': 'Object',
	'author': 'Romly',
	'doc_url': 'https://github.com/Romly-Romly/romly_blender_addon'
}


import bpy
from .apply_all_modifiers import ROMLYADDON_OT_apply_all_modifiers
from .add_constant_offset_array_modifier import ROMLYADDON_OT_add_constant_offset_array_modifier
from .add_weight_bevel_modifier import ROMLYADDON_OT_add_weight_bevel_modifier
from .toggle_viewport_display_as import ROMLYADDON_OT_toggle_viewport_display_as
from .add_box import ROMLYADDON_OT_add_box
from .add_donut_cylinder import ROMLYADDON_OT_add_donut_cylinder
from .add_cross_extrusion import ROMLYADDON_OT_add_cross_extrusion
from .add_reuleaux_polygon import ROMLYADDON_OT_add_reuleaux_polygon
from .add_reuleaux_tetrahedron import ROMLYADDON_OT_add_reuleaux_tetrahedron
from .add_sphericon import ROMLYADDON_OT_add_sphericon
from .add_oloid import ROMLYADDON_OT_add_oloid
from .add_clothoid_curve import ROMLYADDON_OT_add_clothoid_curve, ROMLYADDON_OT_add_clothoid_corner_plate
from .add_jis_screw import ROMLYADDON_OT_add_jis_screw, ROMLYADDON_OT_add_jis_nut
from .add_aluminum_extrusion import ROMLYADDON_OT_add_aluminum_extrusion
from .add_linear_guide import ROMLYADDON_OT_add_linear_guide_rail, ROMLYADDON_OT_add_linear_guide_block
from .add_pinheader import ROMLYADDON_OT_add_pinheader
from .add_nut_hole import ROMLYADDON_OT_add_nut_hole
from .export_collection_as_stl import ROMLYADDON_OT_export_collection_as_stl, ROMLYADDON_OT_export_selection_as_stl
from .select_edges_on_fair_surface import ROMLYADDON_OT_select_edges_on_fair_surface, ROMLYADDON_OT_select_edges_along_axis
from .language_panel import ROMLYADDON_PT_language_panel, ROMLYADDON_OT_change_language
from .reload_and_run_script import ROMLYADDON_OT_reload_and_run_script
from .romly_translation import TRANSLATION_DICT





# アウトライナーのオブジェクトの右クリックに追加するメニュー
class ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent(bpy.types.Menu):
	bl_idname = 'ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent'
	bl_label = 'Romly Tools'
	bl_description = 'Romly Addon Menu'

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_export_selection_as_stl.bl_idname, text=bpy.app.translations.pgettext_iface('Export Selection as STL'), icon='EXPORT')





def outliner_object_menu_func(self, context):
	"""アウトライナーのオブジェクトの右クリックに追加する関数。"""
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent.bl_idname, icon='NONE')





def view3d_edit_mesh_edges_menu_func(self, context):
	"""編集モードのエッジメニューに追加する関数。平面上にある辺を選択する項目を追加"""
	self.layout.separator()
	self.layout.operator(ROMLYADDON_OT_select_edges_on_fair_surface.bl_idname, text=bpy.app.translations.pgettext_iface('Select Edges on Fair Surface'), icon='EDGESEL')
	self.layout.operator(ROMLYADDON_OT_select_edges_along_axis.bl_idname, text=bpy.app.translations.pgettext_iface('Select Edges along Axis'), icon='EMPTY_ARROWS')





def view3d_edit_mesh_context_menu_func(self, context):
	"""
	編集モードのコンテキストメニュー（右クリックメニュー）に追加する関数。
	平面上にある辺を選択する項目を、辺モードの時のみ追加。
	"""
	# 辺モードの時のみメニュー項目を追加（0=頂点, 1=辺, 2=面）
	if bpy.context.tool_settings.mesh_select_mode[1]:
		self.layout.separator()
		self.layout.operator(ROMLYADDON_OT_select_edges_on_fair_surface.bl_idname, text=bpy.app.translations.pgettext_iface('Select Edges on Fair Surface'), icon='EDGESEL')
		self.layout.operator(ROMLYADDON_OT_select_edges_along_axis.bl_idname, text=bpy.app.translations.pgettext_iface('Select Edges along Axis'), icon='EMPTY_ARROWS')





def text_context_menu_func(self, context):
	"""
	テキストエディタのコンテキストメニュー（右クリックメニュー）に追加する関数。
	"""
	self.layout.separator()
	self.layout.operator(ROMLYADDON_OT_reload_and_run_script.bl_idname, text=bpy.app.translations.pgettext_iface('Reload and Run Script'), icon='FILE_SCRIPT')






# オブジェクトの右クリックで表示するメニュー
class ROMLYADDON_MT_romly_tool_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_tool_menu_parent"
	bl_label = "Romly Tools"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_constant_offset_array_modifier.bl_idname, text=bpy.app.translations.pgettext_iface('Add Constant Offset Array Modifier'), icon='MOD_ARRAY')
		layout.operator(ROMLYADDON_OT_add_weight_bevel_modifier.bl_idname, text=bpy.app.translations.pgettext_iface('Add Weight Bevel Modifier'), icon='MOD_BEVEL')
		layout.operator(ROMLYADDON_OT_apply_all_modifiers.bl_idname, text=bpy.app.translations.pgettext_iface('Apply All Modifiers'), icon='CHECKMARK')
		layout.operator(ROMLYADDON_OT_toggle_viewport_display_as.bl_idname, text=bpy.app.translations.pgettext_iface('Toggle Viewport Display As'), icon='SHADING_WIRE')





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
			(ROMLYADDON_OT_add_box, 'Add Box', 'MESH_CUBE'),
			(ROMLYADDON_OT_add_donut_cylinder, 'Add Donut Cylinder', 'MESH_CYLINDER'),
			(ROMLYADDON_OT_add_cross_extrusion, None, 'ADD'),
			(ROMLYADDON_OT_add_reuleaux_polygon, 'Add Reuleaux Polygon', 'MESH_CIRCLE'),
			(ROMLYADDON_OT_add_reuleaux_tetrahedron, 'Add Reuleaux Tetrahedron', 'MESH_CONE'),
			(ROMLYADDON_OT_add_sphericon, 'Add Sphericon', 'MESH_CAPSULE'),
			(ROMLYADDON_OT_add_oloid, 'Add Oloid', 'MESH_CAPSULE'),
			(ROMLYADDON_OT_add_clothoid_curve, 'Add Clothoid Curve', 'FORCE_VORTEX'),
			(ROMLYADDON_OT_add_clothoid_corner_plate, 'Add Clothoid Corner Plate', 'META_PLANE'),
			(None, None, None),
			(ROMLYADDON_OT_add_jis_screw, 'Add JIS Screw', 'MOD_SCREW'),
			(ROMLYADDON_OT_add_jis_nut, 'Add JIS Nut', 'SEQ_CHROMA_SCOPE'),
			(ROMLYADDON_OT_add_aluminum_extrusion, 'Add Aluminium Extrusion', 'FIXED_SIZE'),
			(ROMLYADDON_OT_add_linear_guide_rail, 'Add Linear Guide Rail', 'FIXED_SIZE'),
			(ROMLYADDON_OT_add_linear_guide_block, 'Add Linear Guide Block', 'SNAP_MIDPOINT'),
			(ROMLYADDON_OT_add_pinheader, 'Add Pinheader', 'EMPTY_SINGLE_ARROW'),
			(None, None, None),
			(ROMLYADDON_OT_add_nut_hole, 'Add Nut Hole', 'SEQ_CHROMA_SCOPE'),
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
		layout.operator(ROMLYADDON_OT_export_collection_as_stl.bl_idname, text=bpy.app.translations.pgettext_iface('Export Collection as STL'), icon='EXPORT')





# コレクションメニューに登録
def outliner_collection_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent.bl_idname, icon='NONE')





MY_CLASS_LIST = [
	ROMLYADDON_OT_apply_all_modifiers,
	ROMLYADDON_OT_add_constant_offset_array_modifier,
	ROMLYADDON_OT_add_weight_bevel_modifier,
	ROMLYADDON_OT_toggle_viewport_display_as,
	ROMLYADDON_MT_romly_tool_menu_parent,
	ROMLYADDON_OT_add_box,
	ROMLYADDON_OT_add_donut_cylinder,
	ROMLYADDON_OT_add_cross_extrusion,
	ROMLYADDON_OT_add_reuleaux_polygon,
	ROMLYADDON_OT_add_reuleaux_tetrahedron,
	ROMLYADDON_OT_add_sphericon,
	ROMLYADDON_OT_add_oloid,
	ROMLYADDON_OT_add_clothoid_curve,
	ROMLYADDON_OT_add_clothoid_corner_plate,
	ROMLYADDON_OT_add_jis_screw,
	ROMLYADDON_OT_add_jis_nut,
	ROMLYADDON_OT_add_aluminum_extrusion,
	ROMLYADDON_OT_add_linear_guide_rail,
	ROMLYADDON_OT_add_linear_guide_block,
	ROMLYADDON_OT_add_pinheader,
	ROMLYADDON_OT_add_nut_hole,
	ROMLYADDON_MT_romly_add_mesh_menu_parent,
	ROMLYADDON_OT_export_collection_as_stl,
	ROMLYADDON_OT_export_selection_as_stl,
	ROMLYADDON_MT_romly_export_collection_as_stl_menu_parent,
	ROMLYADDON_MT_romly_export_selection_as_stl_menu_parent,
	ROMLYADDON_OT_select_edges_on_fair_surface,
	ROMLYADDON_OT_select_edges_along_axis,
	ROMLYADDON_PT_language_panel,
	ROMLYADDON_OT_change_language,
	ROMLYADDON_OT_reload_and_run_script,
]



# MARK: register
def register():
	# 翻訳辞書の登録
	try:
		bpy.app.translations.register(__name__, TRANSLATION_DICT)
	except ValueError:
		bpy.app.translations.unregister(__name__)
		bpy.app.translations.register(__name__, TRANSLATION_DICT)

	# blenderへのクラス登録処理
	for cls in MY_CLASS_LIST:
		bpy.utils.register_class(cls)

	# それぞれのメニューに独自メニューを登録
	bpy.types.VIEW3D_MT_object_context_menu.append(object_menu_func)
	bpy.types.VIEW3D_MT_add.append(add_menu_func)
	bpy.types.OUTLINER_MT_collection.append(outliner_collection_menu_func)
	bpy.types.OUTLINER_MT_object.append(outliner_object_menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_edges.append(view3d_edit_mesh_edges_menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(view3d_edit_mesh_context_menu_func)
	bpy.types.TEXT_MT_context_menu.append(text_context_menu_func)





def unregister():
	bpy.types.VIEW3D_MT_object_context_menu.remove(object_menu_func)
	bpy.types.VIEW3D_MT_add.remove(add_menu_func)
	bpy.types.OUTLINER_MT_collection.remove(outliner_collection_menu_func)
	bpy.types.OUTLINER_MT_object.remove(outliner_object_menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_edges.remove(view3d_edit_mesh_edges_menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(view3d_edit_mesh_context_menu_func)
	bpy.types.TEXT_MT_context_menu.remove(text_context_menu_func)

	# クラスの登録解除
	for cls in MY_CLASS_LIST:
		bpy.utils.unregister_class(cls)

	# 翻訳辞書の登録解除
	bpy.app.translations.unregister(__name__)
