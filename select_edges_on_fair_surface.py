import bpy



from . import romly_utils














class ROMLYADDON_OT_select_edges_on_fair_surface(bpy.types.Operator):
	"""選択されたオブジェクトの平面上にある全ての辺を選択するBlenderオペレータ。"""
	bl_idname = "romlyaddon.select_edges_on_fair_surface"
	bl_label = 'Select Edges on Fair Surface'
	bl_description = 'Select all edges on fair surface plane'
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		romly_utils.select_edges_on_fair_surface(bpy.context.view_layer.objects.active)
		return {'FINISHED'}










class ROMLYADDON_MT_romly_select_edges_on_fair_surface_menu_parent(bpy.types.Menu):
	bl_idname = "romlyaddon.select_edges_on_fair_surface_menu_parent"
	bl_label = "Romly Tools"
	bl_description = "Romly Addon Menu"

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_select_edges_on_fair_surface.bl_idname, icon='EDGESEL')





def view3d_edit_mesh_edges_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_select_edges_on_fair_surface_menu_parent.bl_idname, icon='NONE')



def view3d_edit_mesh_context_menu_func(self, context):
	# 辺モードの時のみメニュー項目を追加（0=頂点, 1=辺, 2=面）
	if bpy.context.tool_settings.mesh_select_mode[1]:
		self.layout.separator()
		self.layout.menu(ROMLYADDON_MT_romly_select_edges_on_fair_surface_menu_parent.bl_idname, icon='NONE')









classes = [
	ROMLYADDON_OT_select_edges_on_fair_surface,
	ROMLYADDON_MT_romly_select_edges_on_fair_surface_menu_parent,
]





def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	# 編集モードのエッジメニューに追加
	bpy.types.VIEW3D_MT_edit_mesh_edges.append(view3d_edit_mesh_edges_menu_func)
	# 編集モードの右クリックメニューにも追加。こちらは選択モード無関係なのでエッジ選択モードか判定する必要がある。
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(view3d_edit_mesh_context_menu_func)





def unregister():
	bpy.types.VIEW3D_MT_edit_mesh_edges.remove(view3d_edit_mesh_edges_menu_func)
	for cls in classes:
		bpy.utils.unregister_class(cls)





if __name__ == "__main__":
	register()