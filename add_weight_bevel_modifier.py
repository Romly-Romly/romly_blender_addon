import bpy
import mathutils
import bmesh
from bpy.props import *



from . import romly_utils










# MARK: add_weight_bevel_modifier
class ROMLYADDON_OT_add_weight_bevel_modifier(bpy.types.Operator):
	"""制限方法(Limit Method)をウェイト(Weight)に設定済みのベベルモデファイアを追加するオペレーター。"""
	bl_idname = 'romlyaddon.add_weight_bevel_modifier'
	bl_label = bpy.app.translations.pgettext_iface('Add Weight Bevel Modifier')
	bl_description = 'Add a bevel modifier with its Limit Method set to Weight'
	bl_options = {'REGISTER', 'UNDO'}

	# プロパティ
	val_width: FloatProperty(name='Amount', description='Bevel amount', default=2.0, min=0.01, max=100.0, step=1, precision=2, unit='LENGTH')
	val_segments: IntProperty(name='Segments', description='Number of segments for round edges/verts', default=8, min=1, soft_max=32)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_width')
		col.prop(self, 'val_segments')



	def execute(self, context):
		# 選択されているオブジェクトを取得
		active_obj = bpy.context.active_object

		# Bevelモデファイアを追加
		bevel_modifier = active_obj.modifiers.new(name=bpy.app.translations.pgettext_data('Weight Bevel'), type='BEVEL')

		# モデファイアのパラメータを設定
		bevel_modifier.limit_method = 'WEIGHT'
		bevel_modifier.width = self.val_width
		bevel_modifier.segments = self.val_segments

		# モデファイアを折りたたまれた状態で表示
		bevel_modifier.show_expanded = False

		return {'FINISHED'}










# MARK: clear_bevel_weight
class ROMLYADDON_OT_clear_bevel_weight(bpy.types.Operator):
	"""オブジェクトのすべての辺のベベルウェイトをクリア（0にする）オペレーター。"""
	bl_idname = 'romlyaddon.clear_bevel_weight'
	bl_label = bpy.app.translations.pgettext_iface('Clear Bevel Weight')
	bl_description = 'Set the Bevel Weight of the all edges and vertices to zero'
	bl_options = {'REGISTER', 'UNDO'}

	# プロパティ
	val_edges: BoolProperty(name='Edges', description='Set the Bevel Weight of all edges to zero', default=True)
	val_verts: BoolProperty(name='Vertices', description='Set the Bevel Weight of all vertices to zero', default=False)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_edges')
		col.prop(self, 'val_verts')



	def execute(self, context):
		# 選択されているオブジェクトを取得
		active_obj = bpy.context.active_object

		if self.val_edges:
			romly_utils.clear_bevel_weight(active_obj)
		if self.val_verts:
			romly_utils.clear_verts_bevel_weight(active_obj)

		return {'FINISHED'}






class ROMLYADDON_MT_object_context_menu_parent(bpy.types.Menu):
	"""親となるメニュー"""
	bl_idname = 'romlyaddon.object_context_menu_parent'
	bl_label = 'Romly Tools'
	bl_description = "Romly Addon Menu"

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_weight_bevel_modifier.bl_idname, text=bpy.app.translations.pgettext_iface('Add Weight Bevel Modifier'), icon='MOD_BEVEL')
		layout.operator(ROMLYADDON_OT_clear_bevel_weight.bl_idname, text=bpy.app.translations.pgettext_iface('Clear Bevel Weight'), icon='REMOVE')





def object_context_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_object_context_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_weight_bevel_modifier,
	ROMLYADDON_OT_clear_bevel_weight,
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
