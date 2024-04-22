import bpy
import mathutils
import bmesh
from bpy.props import *



from . import romly_utils










class ROMLYADDON_OT_add_constant_offset_array_modifier(bpy.types.Operator):
	bl_idname = 'romlyaddon.add_constant_offset_array_modifier'
	bl_label = bpy.app.translations.pgettext_iface('Add Constant Offset Array Modifier')
	bl_description = 'Add an array modifier set to a constant offset'
	bl_options = {'REGISTER', 'UNDO'}

	# プロパティ
	val_count: IntProperty(name='Count', description='Number of duplicates to make', default=3, min=2, soft_max=20)
	val_offset: FloatVectorProperty(name='Distance', description='Value for the distance between arrayed items', default=[10, 0, 0], soft_min=-300.0, soft_max=300.0, size=3, subtype='TRANSLATION', unit='LENGTH')



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col.prop(self, 'val_count')
		col.prop(self, 'val_offset')



	def execute(self, context):
		# 選択されているオブジェクトを取得
		active_obj = bpy.context.active_object

		# Arrayモデファイアを追加
		array_modifier = active_obj.modifiers.new(name=bpy.app.translations.pgettext_data('Constant Offset Array'), type='ARRAY')

		# Arrayモデファイアのパラメータを設定
		array_modifier.count = self.val_count
		array_modifier.use_relative_offset = False
		array_modifier.use_constant_offset = True
		array_modifier.constant_offset_displace = self.val_offset

		# 隣接する頂点をマージしない
		array_modifier.use_merge_vertices = False

		# モデファイアを折りたたまれた状態で表示
		array_modifier.show_expanded = False

		return {'FINISHED'}






class ROMLYADDON_MT_object_context_menu_parent(bpy.types.Menu):
	"""親となるメニュー"""
	bl_idname = 'romlyaddon.object_context_menu_parent'
	bl_label = 'Romly Tools'
	bl_description = "Romly Addon Menu"

	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_constant_offset_array_modifier.bl_idname, text=bpy.app.translations.pgettext_iface('Add Constant Offset Array Modifier'), icon='MOD_ARRAY')





def object_context_menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_object_context_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_constant_offset_array_modifier,
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
