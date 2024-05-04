import bpy
import mathutils
import bmesh
from bpy.props import *
from typing import NamedTuple
from mathutils import Vector



from . import romly_utils










PIN_PITCH_127 = '127'
PIN_PITCH_200 = '200'
PIN_PITCH_254 = '254'
PIN_PITCHES = [
	(PIN_PITCH_127, '1.27mm', ''),
	(PIN_PITCH_200, '2.00mm', ''),
	(PIN_PITCH_254, '2.54mm', '')
]

def pin_pitch_to_value(pin_pitch: str):
	if pin_pitch == PIN_PITCH_127:
		return 1.27
	elif pin_pitch == PIN_PITCH_200:
		return 2.00
	else:
		return 2.54










class PinHeaderSpec(NamedTuple):
	pin_thickness: float
	pin_length_above: float
	pin_length_below: float
	block_size: Vector
	block_concave_size: Vector










# MARK: ROMLYADDON_OT_add_pinheader
class ROMLYADDON_OT_add_pinheader(bpy.types.Operator):
	bl_idname = 'romlyaddon.add_pinheader'
	bl_label = bpy.app.translations.pgettext_iface('Add Pin Header')
	bl_description = 'Construct a Pin Header'
	bl_options = {'REGISTER', 'UNDO'}



	def __init__(self):
		self.on_pitch_update(None)



	def on_pitch_update(self, context):
		PIN_SPECS = {
			PIN_PITCH_127: PinHeaderSpec(pin_thickness=0.4, pin_length_above=3, pin_length_below=2.3, block_size=Vector([1.27, 2.1, 1.5]), block_concave_size=Vector([0, 0, 0])),
			PIN_PITCH_200: PinHeaderSpec(pin_thickness=0.5, pin_length_above=4, pin_length_below=2.8, block_size=Vector([2, 2, 2]), block_concave_size=Vector([3, 1.4, 0.3])),
			PIN_PITCH_254: PinHeaderSpec(pin_thickness=0.64, pin_length_above=6.1, pin_length_below=3, block_size=Vector([2.54, 2.5, 2.5]), block_concave_size=Vector([3, 1.6, 0.4])),
		}
		spec = PIN_SPECS.get(self.val_pitch)
		if spec:
			self.val_pin_thickness = spec.pin_thickness
			self.val_pin_length_top = spec.pin_length_above
			self.val_pin_length_bottom = spec.pin_length_below
			self.val_block_size = spec.block_size
			self.val_block_concave_size = spec.block_concave_size



	# プロパティ
	val_pitch: EnumProperty(name='Pitch', description='Pin pitch of the pin header', default=PIN_PITCH_254, items=PIN_PITCHES, update=on_pitch_update)

	val_block_size: FloatVectorProperty(name='Block Size', size=3, min=0.1, soft_max=2.54, description='Size of the pin header housing', subtype='TRANSLATION', unit='LENGTH', precision=3)
	val_pin_thickness: FloatProperty(name='Pin Thickness', min=0.1, soft_max=1, unit='LENGTH')
	val_pin_length_top: FloatProperty(name='Pin Length (Above)', min=0.1, soft_max=10, unit='LENGTH')
	val_pin_length_bottom: FloatProperty(name='Pin Length (Below)', min=0.1, soft_max=10, unit='LENGTH')
	val_block_concave_size: FloatVectorProperty(name='Block Concave Size', size=3, min=0, soft_max=2, description='Size of the housing concave', subtype='TRANSLATION', unit='LENGTH')

	val_num_cols: IntProperty(name='Columns', default=4, min=1, soft_max=20)
	val_num_rows: IntProperty(name='Rows', default=1, min=1, soft_max=3)






	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col.label(text='Pitch')
		row = col.row(align=True)
		row.prop(self, 'val_pitch', expand=True)
		col.separator()

		row = col.row(align=True)
		row.prop(self, 'val_pin_thickness')
		row = col.row(align=True)
		col_pin_length = col.column(align=True)
		col_pin_length.prop(self, 'val_pin_length_top')
		col_pin_length.prop(self, 'val_pin_length_bottom')
		row = col.row(align=True)
		row.alignment = 'RIGHT'
		text = bpy.app.translations.pgettext_iface('Pin Total Length: {value}')
		row.label(text=text.format(value=romly_utils.units_to_string(self.val_pin_length_top + self.val_pin_length_bottom + self.val_block_size[2])))
		col.separator()

		col.label(text='Block Size')
		row = col.row(align=True)
		row.prop(self, 'val_block_size', text='')
		col.label(text='Block Concave Size')
		row = col.row(align=True)
		row.prop(self, 'val_block_concave_size', text='')
		col.separator()

		col.label(text='Number of Pins')
		row = col.row(align=True)
		row.prop(self, 'val_num_cols')
		row.prop(self, 'val_num_rows')



	def execute(self, context):
		# ピンヘッダのプラスチック部分のサイズ
		pin_pitch = pin_pitch_to_value(self.val_pitch)

		# ----------------------------------------
		# プラスチック部分の作成

		# 設定に従った頂点を生成
		obj_plastic = romly_utils.create_box(size=self.val_block_size, offset=mathutils.Vector([0, 0, self.val_block_size[2] / 2]))

		# ベベルモディファイアを追加、適用
		romly_utils.apply_bevel_modifier_to_edges(obj_plastic, self.val_block_size[1] * 0.15, lambda edge: not romly_utils.is_edge_along_z_axis(edge))

		# ----------------------------------------
		# プラスチックの下部を削る

		if self.val_block_concave_size[0] > 0 and self.val_block_concave_size[1] > 0 and self.val_block_concave_size[2] > 0:
			obj_plastic_concave = romly_utils.create_box(size=self.val_block_concave_size, offset=mathutils.Vector([0, 0, self.val_block_concave_size[2] / 2]))
			romly_utils.apply_boolean_object(obj_plastic, obj_plastic_concave)


		bpy.context.collection.objects.unlink(obj_plastic)

		# ----------------------------------------
		# ピン部分の作成

		pin_length = self.val_pin_length_top + self.val_block_size[2] + self.val_pin_length_bottom
		pin_scale = mathutils.Vector([self.val_pin_thickness, self.val_pin_thickness, pin_length])
		obj_pin = romly_utils.create_box(size=pin_scale, offset=mathutils.Vector([0, 0, pin_length / 2 - self.val_pin_length_bottom]))

		# ベベルモディファイアを追加、適用
		romly_utils.apply_bevel_modifier_to_edges(obj_pin, self.val_pin_thickness * 0.3, romly_utils.is_edge_along_z_axis)

		# ----------------------------------------
		# プラスチック部分とピン部分の結合、配列作成

		text = bpy.app.translations.pgettext_iface('Pin Header {pitch}mm {rows}x{cols}')
		obj_name = text.format(pitch=pin_pitch, rows=self.val_num_rows, cols=self.val_num_cols)
		obj = romly_utils.create_combined_object(objects=(obj_plastic, obj_pin), obj_name=obj_name)
		bpy.context.collection.objects.link(obj)
		bpy.context.collection.objects.unlink(obj_pin)

		# 配列を追加

		# Arrayモデファイアを追加
		array_modifier = obj.modifiers.new(name='Pin Header Columns', type='ARRAY')
		array_modifier.count = self.val_num_cols
		array_modifier.use_relative_offset = False
		array_modifier.use_constant_offset = True
		array_modifier.constant_offset_displace = mathutils.Vector([pin_pitch, 0, 0])
		array_modifier.use_merge_vertices = False	# 隣接する頂点をマージしない

		# Arrayモデファイアのパラメータを設定
		array_modifier_rows = obj.modifiers.new(name='Pin Header Rows', type='ARRAY')
		array_modifier_rows.count = self.val_num_rows
		array_modifier_rows.use_relative_offset = False
		array_modifier_rows.use_constant_offset = True
		array_modifier_rows.constant_offset_displace = mathutils.Vector([0, pin_pitch, 0])
		array_modifier_rows.use_merge_vertices = False	# 隣接する頂点をマージしない

		# ----------------------------------------

		# オブジェクトを3Dカーソル位置へ移動
		obj.location = bpy.context.scene.cursor.location

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.operator(ROMLYADDON_OT_add_pinheader.bl_idname, text=bpy.app.translations.pgettext_iface('Add Pin Header'), icon='EMPTY_SINGLE_ARROW')





classes = [
	ROMLYADDON_OT_add_pinheader,
]





def register():
	# クラスと翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.append(menu_func)





def unregister():
	# クラスと翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
