import bpy
import math
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple, Literal



from . import romly_utils










def create_lead_screw(major_diameter: float, minor_diameter: float, pitch: float, lead: int, thread_angle: float, length: float, segments: int) -> bpy.types.Object:
	# まず major_diameter 径の円柱を作る
	cylinder = romly_utils.create_cylinder(radius=major_diameter / 2, length_z_plus=length, segments=segments)



	# スレッド形状の断面図を作成

	# まず山の部分の幅を求める（谷の部分も同じ）
	d = (major_diameter - minor_diameter) / 2
	t = math.tan(thread_angle / 2) * d
	thread_top_length = ((pitch - t * 2) / 4) * 2

	# ブーリアンで削るので、スレッドの斜めの線を major_diameter より少し伸ばした位置を求めておく
	x = thread_top_length * math.tan(math.pi - math.pi / 2 - thread_angle / 2)

	# 頂点を置いていく
	vertices = []
	faces = []
	# ねじ切りの断面をリードの数分用意する
	z_offset = 0
	for _ in range(lead):
		# この4つの頂点でねじ切りの断面（台形）ひとつ分
		vertices.append(Vector((-major_diameter / 2 - x, 0, z_offset)))
		vertices.append(Vector((-minor_diameter / 2, 0, z_offset + thread_top_length / 2 + t)))
		vertices.append(Vector((-minor_diameter / 2, 0, z_offset + thread_top_length / 2 + t + thread_top_length)))
		vertices.append(Vector((-major_diameter / 2 - x, 0, z_offset + (thread_top_length / 2 + t) * 2 + thread_top_length)))
		faces.append(list(range(len(vertices) - 4, len(vertices))))
		z_offset += pitch

	# 回してスクリューを作る
	pitch_iteration = math.ceil(length / (lead * pitch)) + 2
	n = len(vertices)
	for _ in range(pitch_iteration):
		romly_utils.add_revolved_surface(vertices=vertices, faces=faces, rotation_vertex_count=n, segments=segments, z_offset=lead * pitch, close=True)

	thread_cutter = romly_utils.cleanup_mesh(romly_utils.create_object(vertices, faces))
	bpy.context.collection.objects.link(thread_cutter)

	# 円柱の下まで削れるよう下にずらす
	thread_cutter.location = Vector((0, 0, -lead * pitch))

	# ブーリアンで削る
	romly_utils.apply_boolean_object(cylinder, thread_cutter)

	return cylinder









class ROMLYADDON_OT_add_lead_screw(bpy.types.Operator):
	"""リードスクリューの軸を作成するオペレーター。"""
	bl_idname = 'romlyaddon.add_lead_screw'
	bl_label = bpy.app.translations.pgettext_iface('Add Lead Screw')
	bl_description = 'Construct a Lead Screw'
	bl_options = {'REGISTER', 'UNDO'}

	# 長さ
	val_length: FloatProperty(name='Length', description='The length of the lead screw', default=100.0, min=10, soft_max=500, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	val_major_diameter: FloatProperty(name='Major Dia.', description='The outer diameter of the lead screw', default=8.0, min=0.1, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_minor_diameter: FloatProperty(name='Minor Dia.', description='The thread valley diameter of the lead screw', default=6.2, min=0.1, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	val_pitch: FloatProperty(name='Pitch', description='The pitch of the lead screw', default=2.0, min=1, max=20, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_lead: IntProperty(name='Starts', description='The number of thread starts of the lead screw', default=4, min=1, max=10)
	val_thread_angle: FloatProperty(name='Thread Angle', description='The angle of the thread', default=math.radians(30), min=math.radians(5), soft_max=math.radians(60), max=math.radians(90), subtype='ANGLE')

	val_segments: IntProperty(name='Segments', description='The segments of the screw', default=32, min=3, max=64)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col.prop(self, 'val_length')
		col.separator()

		row = col.row(align=True)
		row.prop(self, 'val_major_diameter')
		row.prop(self, 'val_minor_diameter')
		row = col.row(align=True)
		row.prop(self, 'val_pitch')
		row.prop(self, 'val_lead')
		row = col.row(align=True)
		row.alignment = 'RIGHT'
		s = bpy.app.translations.pgettext_iface('Lead: {value}')
		row.label(text=s.format(value=romly_utils.units_to_string(self.val_pitch * self.val_lead, category=bpy.utils.units.categories.LENGTH)))
		col.prop(self, 'val_thread_angle')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_segments')



	def execute(self, context):
		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')



		obj = create_lead_screw(major_diameter=self.val_major_diameter, minor_diameter=self.val_minor_diameter, pitch=self.val_pitch, lead=self.val_lead, thread_angle=self.val_thread_angle, length=self.val_length, segments=self.val_segments)



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
	self.layout.operator(ROMLYADDON_OT_add_lead_screw.bl_idname, text=bpy.app.translations.pgettext_iface('Add Lead Screw'), icon='MOD_SCREW')





classes = [
	ROMLYADDON_OT_add_lead_screw,
]



def register():
	# 翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	# 翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
