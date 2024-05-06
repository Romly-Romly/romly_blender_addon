import bpy
import bmesh
import math
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion



from . import romly_utils










# MARK: select_edges_on_fair_surface
class ROMLYADDON_OT_select_edges_on_fair_surface(bpy.types.Operator):
	"""選択されたオブジェクトの平面上にある全ての辺を選択するBlenderオペレータ。"""
	bl_idname = "romlyaddon.select_edges_on_fair_surface"
	bl_label = bpy.app.translations.pgettext_iface('Select Edges on Fair Surface')
	bl_description = 'Select all edges on fair surface plane'
	bl_options = {'REGISTER', 'UNDO'}

	val_threshold: FloatProperty(name='Threshold', description='Select edges when the angle between normals of the two surfaces sharing the edge is less than or equal to this value', default=0.0, min=0.0, soft_max=math.radians(30.0), max=math.radians(180), step=1, precision=3, unit='ROTATION')



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_threshold')



	def execute(self, context):
		romly_utils.select_edges_on_fair_surface(bpy.context.view_layer.objects.active, threshold_degree=math.degrees(self.val_threshold))
		return {'FINISHED'}










# MARK: select_edges_along_axis
class ROMLYADDON_OT_select_edges_along_axis(bpy.types.Operator):
	"""選択されたオブジェクトの軸に沿った辺を選択するBlenderオペレータ。"""
	bl_idname = "romlyaddon.select_edges_along_axis"
	bl_label = bpy.app.translations.pgettext_iface('Select Edges along Axis')
	bl_description = 'Select all edges along the axis'
	bl_options = {'REGISTER', 'UNDO'}

	val_threshold: FloatProperty(name='Threshold', description='Select edges when the angle between normals of the two surfaces sharing the edge is less than or equal to this value', default=0.0, min=0.0, soft_max=math.radians(30.0), max=math.radians(180), step=1, precision=3, unit='ROTATION')
	val_axis: BoolVectorProperty(name='Axis', default=(False, False, True), size=3)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		row = col.row(align=True)
		row.prop(self, 'val_axis')
		col.prop(self, 'val_threshold')



	def execute(self, context):
		romly_utils.select_edges_along_axis(bpy.context.view_layer.objects.active, axis=self.val_axis, threshold_degree=math.degrees(self.val_threshold))
		return {'FINISHED'}










# MARK: toggle_edge_bevel_weight
class ROMLYADDON_OT_toggle_edge_bevel_weight(bpy.types.Operator):
	"""選択されている辺のBevel Weightを0/1切り替えするオペレーター。"""
	bl_idname = 'romlyaddon.toggle_edge_bevel_weight'
	bl_label = bpy.app.translations.pgettext_iface('Toggle Edges Bevel Weight')
	bl_description = "Toggle selected edges' bevel weight to 0 or 1"
	bl_options = {'REGISTER', 'UNDO'}



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		obj = context.view_layer.objects.active
		if obj:
			# 選択されているすべての辺のベベルウェイトが0なら、それらの辺のベベルウェイトを1にする。またはその逆の処理。
			bm = bmesh.from_edit_mesh(obj.data)

			KEY = 'bevel_weight_edge'
			bevel_layer = bm.edges.layers.float.get(KEY, bm.edges.layers.float.new(KEY))

			new_value = 1.0
			for edge in bm.edges:
				if edge.select:
					if not math.isclose(edge[bevel_layer], 0, abs_tol=0.01):
						new_value = 0.0
						break
			for edge in bm.edges:
				if edge.select:
					edge[bevel_layer] = new_value

			# 更新を反映
			bmesh.update_edit_mesh(obj.data)



		return {'FINISHED'}










# MARK: transform_object_aligning_edge_to_axis
class ROMLYADDON_OT_transform_object_aligning_edge_to_axis(bpy.types.Operator):
	"""選択されている辺が軸に沿うようにオブジェクトを回転させるオペレーター。"""
	bl_idname = 'romlyaddon.transform_object_aligning_edge_to_axis'
	bl_label = bpy.app.translations.pgettext_iface('Rotate object aligning edge to axis')
	bl_description = 'Rotate and translate the object to align the selected edge to the axis'
	bl_options = {'REGISTER', 'UNDO'}

	val_axis: EnumProperty(name='Axis', items=[('X', 'X', 'Rotate object to align selected edges to X-axis'), ('Y', 'Y', 'Rotate object to align selected edges to Y-axis'), ('Z', 'Z', 'Rotate object to align selected edges to Z-axis')], default='Z')



	def draw(self, context):
		col = self.layout.column()
		row = col.row(align=True)
		row.prop(self, 'val_axis', expand=True)



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		obj = context.view_layer.objects.active

		if not obj:
			romly_utils.report(self, 'WARNING', msg_key='Please select the object')
			return {'CANCELLED'}

		# 最低でも1つ以上辺を選択していること
		selected = False
		bm = bmesh.from_edit_mesh(obj.data)
		for edge in bm.edges:
			if edge.select:
				selected = True
				break
		if not selected:
			romly_utils.report(self, 'WARNING', msg_key='Please select the edge')



		def get_selected_v1_v2(obj: bpy.types.Object) -> tuple[Vector, Vector]:
			"""
			選択されているすべての辺の始点と終点をそれぞれ平均化した位置をワールド座標で返す。辺が一つも選択されていない場合はゼロベクトルを返す。

			Parameters
			----------
			obj : Object

			Returns
			-------
			tuple[Vector, Vector]
				算出された始点の平均位置のワールド座標と終点の平均位置のワールド座標のタプル。
			"""
			v1 = Vector([0, 0, 0])
			v2 = Vector([0, 0, 0])
			count = 0
			bm = bmesh.from_edit_mesh(obj.data)
			for edge in bm.edges:
				if edge.select:
					v1 += obj.matrix_world @ edge.verts[0].co
					v2 += obj.matrix_world @ edge.verts[1].co
					count += 1
			if count > 0:
				return v1 / count, v2 / count
			else:
				return v1, v2

		def get_mid_point(v1: Vector, v2: Vector) -> Vector:
			"""二つのベクトルの中間点を求める。"""
			return v1 + (v2 - v1) * 0.5



		# 選択されているすべての辺の始点終点の平均を計算
		selected_v1, selected_v2 = get_selected_v1_v2(obj)

		# どの軸に合わせるか
		align_target_vector = Vector([0, 0, 1])
		match self.val_axis:
			case 'X':
				align_target_vector = Vector([1, 0, 0])
			case 'Y':
				align_target_vector = Vector([0, 1, 0])

		# その軸に合わせるためのクォータニオンを求め、オイラー角に変換
		quat = (selected_v2 - selected_v1).normalized().rotation_difference(align_target_vector)
		eular_angles = quat.to_euler()

		# オブジェクトにすでに設定されているオイラー角と合成し、新しいオイラー角として設定
		combined = obj.rotation_euler.copy()
		combined.rotate(eular_angles)
		obj.rotation_euler = combined



		# 位置を再設定する前に、これを呼ばないとオブジェクトの変換座標が更新されない
		bpy.context.view_layer.update()



		# 再び選択されているすべての辺の始点終点の平均を計算し、以前の中間点から新しい中間点へのオフセットを求め、以前の中間点の位置が維持されるようにオブジェクトを移動
		new_selected_v1, new_selected_v2 = get_selected_v1_v2(obj)
		obj.location += get_mid_point(selected_v1, selected_v2) - get_mid_point(new_selected_v1, new_selected_v2)



		return {'FINISHED'}










class ROMLYADDON_MT_romly_select_edges_on_fair_surface_menu_parent(bpy.types.Menu):
	bl_idname = "romlyaddon.select_edges_on_fair_surface_menu_parent"
	bl_label = "Romly Tools"
	bl_description = "Romly Addon Menu"

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_select_edges_on_fair_surface.bl_idname, text=bpy.app.translations.pgettext_iface('Select Edges on Fair Surface'), icon='EDGESEL')
		layout.operator(ROMLYADDON_OT_select_edges_along_axis.bl_idname, text=bpy.app.translations.pgettext_iface('Select Edges along Axis'), icon='EMPTY_ARROWS')
		layout.operator(ROMLYADDON_OT_toggle_edge_bevel_weight.bl_idname, text=bpy.app.translations.pgettext_iface('Toggle Edges Bevel Weight'), icon='MOD_BEVEL')
		layout.operator(ROMLYADDON_OT_transform_object_aligning_edge_to_axis.bl_idname, text=bpy.app.translations.pgettext_iface('Rotate object aligning edge to axis'), icon='MOD_BEVEL')





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
	ROMLYADDON_OT_select_edges_along_axis,
	ROMLYADDON_OT_toggle_edge_bevel_weight,
	ROMLYADDON_OT_transform_object_aligning_edge_to_axis,
	ROMLYADDON_MT_romly_select_edges_on_fair_surface_menu_parent,
]





def register():
	# クラスと翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	# 編集モードのエッジメニューに追加
	bpy.types.VIEW3D_MT_edit_mesh_edges.append(view3d_edit_mesh_edges_menu_func)
	# 編集モードの右クリックメニューにも追加。こちらは選択モード無関係なのでエッジ選択モードか判定する必要がある。
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(view3d_edit_mesh_context_menu_func)





def unregister():
	# クラスと翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_edit_mesh_edges.remove(view3d_edit_mesh_edges_menu_func)





if __name__ == '__main__':
	register()