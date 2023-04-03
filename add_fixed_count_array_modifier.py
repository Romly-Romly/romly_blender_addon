import bpy
import mathutils
import bmesh
from bpy.props import *




class ROMLYADDON_OT_add_fixed_count_array_modifier(bpy.types.Operator):
	bl_idname = "romlyaddon.add_fixed_count_array_modifier"
	bl_label = "Add Fixed Count Array Modifier"
	bl_description = '距離指定で一定回数複製設定のArrayモデファイアを追加します'
	bl_options = {'REGISTER', 'UNDO'}

	# プロパティ
	val_count: IntProperty(name='Count', description='複製する数を指定します', default=3, min=2, soft_max=20)
	val_offset: FloatVectorProperty(name='Distance', description='オフセット距離', default=[10, 0, 0], soft_min=-100.0, soft_max=100.0, size=3, subtype='TRANSLATION', unit='LENGTH')



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
		array_modifier = active_obj.modifiers.new(name="Constant Offset Array", type="ARRAY")

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






# 親となるメニュー
class ROMLYADDON_MT_apply_all_modifiers_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_apply_all_modifiers_menu_parent"
	bl_label = "Romly Tools"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_fixed_count_array_modifier.bl_idname, icon='MOD_ARRAY')





# オブジェクトの追加メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_apply_all_modifiers_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	bpy.utils.register_class(ROMLYADDON_OT_add_fixed_count_array_modifier)
	bpy.utils.register_class(ROMLYADDON_MT_apply_all_modifiers_menu_parent)
	bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)





# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLYADDON_OT_add_fixed_count_array_modifier)
	bpy.utils.unregister_class(ROMLYADDON_MT_apply_all_modifiers_menu_parent)
	bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()
