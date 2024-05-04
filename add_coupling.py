import bpy
import math
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple, Literal



from . import romly_utils










def is_coupling_bevel_edge(edge: bmesh.types.BMEdge, z1: float, z2: float) -> bool:
	"""
	カップリングのオブジェクトの指定された辺がベベルすべき辺ならTrueを返す。
	カップリングの上面または底面にある辺で、90度の角度にある（平面上にある辺ではない）辺。

	Parameters
	----------
	edge : bmesh.types.BMEdge
		判定対象の辺を指定。
	z1, z2 : float
		カップリングの上面Z座標と底面Z座標を指定。この座標にある辺が対象となる。

	Returns
	-------
	bool
		ベベルすべき辺ならTrueを返す。
	"""
	edge_z1 = edge.verts[0].co[2]
	edge_z2 = edge.verts[1].co[2]
	TOL = 0.01
	if ((math.isclose(edge_z1, z1, abs_tol=TOL) and math.isclose(edge_z2, z1, abs_tol=TOL)) or
		(math.isclose(edge_z1, z2, abs_tol=TOL) and math.isclose(edge_z2, z2, abs_tol=TOL))):
		# 閾値値の角度を内積の値に変換
		threshold_radian = math.radians(0.1)
		cos_value = math.cos(threshold_radian)

		# 内積が閾値以下なら、その辺を選択
		dot = romly_utils.calc_linked_face_dot(edge)
		if dot < cos_value:
			return True

	return False










# MARK: create_coupling
def create_coupling(diameter: float, length: float, d1: float, d2: float, d_middle: float, insertion_length: float, bevel: float, segments: int) -> bpy.types.Object:
	"""
	カップリングのベースとなるオブジェクトを作成する。

	Parameters
	----------
	diameter : float
		カップリングの外径。
	length : float
		カップリングの長さ（高さ）。
	d1, d2 : float
		カップリングのそれぞれの内径。d1が上部、d2が下部の内径となる。
	d_middle : float
		中央部分（insertion_lengthより内側）の内径。
	insertion_length : float
		差し込み穴の長さ。d1, d2の内径が続く長さ。
	bevel : float
		カップリングの縁のベベル幅。0の場合はベベル無し。
	segments : int
		カップリングの円周の分割数。

	Returns
	-------
	bpy.types.Object
		生成したカップリングのオブジェクトを返す。
	"""
	# まず円柱を作る
	cylinder = romly_utils.create_cylinder(radius=diameter / 2, length_z_plus=length, segments=segments)

	# D2の穴を下部に開ける
	cutter = romly_utils.create_cylinder(radius=d2 / 2, length_z_plus=insertion_length, length_z_minus=0.5, segments=segments)
	romly_utils.apply_boolean_object(cylinder, cutter)

	# D1の穴を上部に開ける
	cutter = romly_utils.create_cylinder(radius=d1 / 2, length_z_plus=0.5, length_z_minus=insertion_length, segments=segments)
	cutter.location = Vector((0, 0, length))
	romly_utils.apply_boolean_object(cylinder, cutter)

	# ベベルの前にメッシュをクリーンアップする必要がある
	cylinder = romly_utils.cleanup_mesh(cylinder)

	# ベベルを作る
	if bevel > 0:
		romly_utils.apply_bevel_modifier_to_edges(cylinder, bevel, lambda edge: is_coupling_bevel_edge(edge, z1=0, z2=length))

	# D1とD2の中間の穴を作る
	if length - insertion_length * 2 > 0:
		l = (length - insertion_length * 2) / 2
		cutter = romly_utils.create_cylinder(radius=d_middle / 2, length_z_plus=l, length_z_minus=l, segments=segments)
		cutter.location = Vector((0, 0, length / 2))
		romly_utils.apply_boolean_object(cylinder, cutter)

	return cylinder










# MARK: make_setscrew_holes
def make_setscrew_holes(obj: bpy.types.Object, coupling_diameter: float, coupling_length: float, diameter: float, position: float, angle: float, segments: int, threaded: bool = True, thread_pitch: float = 1, thread_depth: float = 1) -> None:
	"""
	カップリングに止めネジ穴を開ける。

	Parameters
	----------
	obj : bpy.types.Object
		カップリングのオブジェクトを渡す。
	coupling_diameter : float
		カップリングの外径。止めネジ穴を開けるのに十分な長さをこの値から決める。
	coupling_length : float
		カップリングの長さ。
	diameter : float
		止めネジ穴の直径。
	position : float
		止めネジ穴の位置。カップリングの上面と底面それぞれからの穴の中心までの距離。
	angle : float
		カップリングを上から見た時の、止めネジ穴の角度。0の場合は同じ高さには1つしか穴を開けない（合計で2つ）。
	segments : int
		止めネジ穴のメッシュの分割数。
	threaded : bool, optional
		_description_, by default True
	thread_pitch : float, optional
		_description_, by default 1
	thread_depth : float, optional
		_description_, by default 1
	"""
	cutter = None
	x_rotation = 90
	if threaded:
		cutter = romly_utils.create_threaded_cylinder(diameter=diameter, length=coupling_diameter * 2, pitch=thread_pitch, lead=1, thread_depth=thread_depth, segments=segments, bevel_segments=5, edge_flat=True)
		x_rotation = -90
	else:
		cutter = romly_utils.create_cylinder(radius=diameter / 2, length_z_plus=coupling_diameter * 2, length_z_minus=0, segments=segments)

	cutter.rotation_euler = Vector((math.radians(x_rotation), 0, 0))
	cutter.location = Vector((0, 0, position))
	romly_utils.apply_boolean_object(obj, cutter, unlink=False)

	if not math.isclose(angle, 0, abs_tol=0.01):
		cutter.rotation_euler = Vector((math.radians(x_rotation), 0, angle))
		romly_utils.apply_boolean_object(obj, cutter, unlink=False)

	cutter.rotation_euler = Vector((math.radians(x_rotation), 0, 0))
	cutter.location = Vector((0, 0, coupling_length - position))
	romly_utils.apply_boolean_object(obj, cutter, unlink=False)

	if not math.isclose(angle, 0, abs_tol=0.01):
		cutter.rotation_euler = Vector((math.radians(x_rotation), 0, angle))
		romly_utils.apply_boolean_object(obj, cutter, unlink=False)

	bpy.context.collection.objects.unlink(cutter)









def make_slit(obj: bpy.types.Object, coupling_diameter: float, coupling_length: float, width: float, distance: float, rotation_count: int, segments: int) -> None:
	if width > 0 and rotation_count > 0:
		# 回転体の元になる四角形
		z = coupling_length / 2 - (distance * rotation_count) / 2
		vertices = [
			Vector((-coupling_diameter, 0, z + width / 2)),
			Vector((-coupling_diameter, 0, z - width / 2)),
			Vector((-0.1, 0, z - width / 2)),
			Vector((-0.1, 0, z + width / 2)),
		]
		faces = []
		for _ in range(rotation_count):
			romly_utils.add_revolved_surface(vertices, faces=faces, rotation_vertex_count=4, segments=segments, close=True, z_offset=distance)

		# 回転体の断面の蓋
		faces.append([0, 1, 2, 3])
		faces.append(list(range(len(vertices) - 4, len(vertices))))

		cutter = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=vertices, faces=faces))
		bpy.context.collection.objects.link(cutter)
		romly_utils.apply_boolean_object(obj, cutter)










def update_setscrew_sizes(self: bpy.types.OperatorProperties, context) -> None:
	# 指定されたスクリューサイズに基づいて直径とピッチを設定
	spec = romly_utils.SCREW_SPECS.get(self.val_setscrew_sizes)
	if spec:
		self.val_setscrew_diameter = spec.diameter
		self.val_setscrew_thread_pitch = spec.pitch
		self.val_setscrew_thread_depth = spec.thread_depth()










# MARK: ROMLYADDON_OT_add_coupling
class ROMLYADDON_OT_add_coupling(bpy.types.Operator):
	"""カップリングのメッシュを作成するオペレーター。"""
	bl_idname = 'romlyaddon.add_coupling'
	bl_label = bpy.app.translations.pgettext_iface('Add Coupling')
	bl_description = 'Construct a Coupling'
	bl_options = {'REGISTER', 'UNDO'}

	# 外径
	val_diameter: FloatProperty(name='Diameter', description='[D] The outer diameter of the Coupling', default=19, min=1, soft_max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	# 長さ
	val_length: FloatProperty(name='Length', description='[L] The length (height) of the Coupling', default=25, min=2, soft_max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# D1, D2
	val_d1: FloatProperty(name='D1', description='The inner diameter 1 of the Coupling', default=5, min=1, soft_max=30, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_d2: FloatProperty(name='D2', description='The inner diameter 2 of the Coupling', default=8, min=1, soft_max=30, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	val_hole_length: FloatProperty(name='Hole Length', description='The length of the Coupling', default=7, min=1, soft_max=30, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_middle_part_clearance: FloatProperty(name='Clearance', description='The length of the Coupling', default=0.5, min=1, soft_max=5, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# セットスクリュー
	val_setscrew: BoolProperty(name='Set Screw Holes', description='Make set screw holes on the Coupling.', default=True)
	val_setscrew_position: FloatProperty(name='Position', description='The distance to the center of the set screw holes from both ends of the coupling', default=3, min=1, soft_max=10, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_setscrew_angle: FloatProperty(name='Angle', description='Angle on the Z-axis between each pair of opposing set screws', default=math.radians(90), min=math.radians(-180), soft_max=math.radians(180), max=math.radians(360), subtype='ANGLE')
	SETSCREW_SIZE_DEFAULT = 'm3'
	val_setscrew_sizes: EnumProperty(name='Set Screw Sizes', items=[
		('m2', 'M2', 'Set specs to M2 size'),
		('m2_5', 'M2.5', 'Set specs to M2.5 size'),
		('m3', 'M3', 'Set specs to M3 size'),
		('m4', 'M4', 'Set specs to M4 size'),
		], default=SETSCREW_SIZE_DEFAULT, update=update_setscrew_sizes)
	val_setscrew_diameter: FloatProperty(name='Diameter', description='Diameter of the set screw holes', default=romly_utils.SCREW_SPECS[SETSCREW_SIZE_DEFAULT].diameter, min=1, soft_max=10, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_setscrew_thread: BoolProperty(name='Threading', description="Thread screw holes if it's checked", default=False)
	val_setscrew_thread_pitch: FloatProperty(name='Pitch', description='Pitch of the set screw hole threads', default=romly_utils.SCREW_SPECS[SETSCREW_SIZE_DEFAULT].pitch, min=0.1, soft_max=10, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_setscrew_thread_depth: FloatProperty(name='Depth', description='Depth of the set screw hole threads', default=romly_utils.SCREW_SPECS[SETSCREW_SIZE_DEFAULT].thread_depth(), min=0.1, soft_max=10, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# スリット
	val_slit: BoolProperty(name='Helical Slit', description='Make helical slit on the coupling', default=True)
	val_slit_thickness: FloatProperty(name='Width', description='The width of the helical slit', default=0.3, min=0.1, soft_max=1, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_slit_count: IntProperty(name='Count', description='The rotation count of the slit', default=5, min=1, soft_max=20)
	val_slit_interval: FloatProperty(name='Distance', description='Distance traveled per rotation of the slit', default=2, min=1, soft_max=4, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# 縁のベベル幅
	val_bevel: FloatProperty(name='Bevel', description='The bevel offset width of the edge of the coupling', default=0.5, min=0, soft_max=5, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# セグメント数
	val_segments: IntProperty(name='Coupling Segments', description='The number of segments of the coupling', default=48, min=6, soft_max=64, max=128)
	val_setscrew_segments: IntProperty(name='Set Screw Segments', description='The number of segments of the set screw holes', default=16, min=4, soft_max=32, max=64)
	val_slit_segments: IntProperty(name='Slit Segments', description='The number of segments of the slit', default=48, min=6, soft_max=64, max=128)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		row = col.row(align=True)
		row.prop(self, 'val_diameter')
		row.prop(self, 'val_length')
		row = col.row(align=True)
		row.prop(self, 'val_d1')
		row.prop(self, 'val_d2')
		col.prop(self, 'val_hole_length')
		col.prop(self, 'val_middle_part_clearance')
		col.separator()

		col.prop(self, 'val_setscrew')
		box = col.box()
		box.enabled = self.val_setscrew
		box_col = box.column()
		row = box_col.row(align=True)
		row.prop(self, 'val_setscrew_position')
		row.prop(self, 'val_setscrew_angle')
		box_col.separator()

		row = box_col.row(align=True)
		row.prop(self, 'val_setscrew_sizes', expand=True)
		size_box = box_col.box()
		split = size_box.split(factor=0.5, align=True)
		c = split.column(align=False)
		c.prop(self, 'val_setscrew_diameter')
		c.prop(self, 'val_setscrew_thread')
		c = split.column(align=True)
		c.enabled = self.val_setscrew_thread
		c.alignment = 'RIGHT'
		c.prop(self, 'val_setscrew_thread_pitch')
		c.prop(self, 'val_setscrew_thread_depth')
		col.separator()

		col.prop(self, 'val_slit')
		box = col.box()
		box.enabled = self.val_slit
		box_col = box.column()
		box_col.prop(self, 'val_slit_thickness')
		row = box_col.row(align=True)
		row.prop(self, 'val_slit_count')
		row.prop(self, 'val_slit_interval')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_bevel')
		col.prop(self, 'val_segments')
		col.prop(self, 'val_setscrew_segments')
		col.prop(self, 'val_slit_segments')



	def execute(self, context):
		middle_diameter = max(self.val_d1, self.val_d2) + self.val_middle_part_clearance
		obj = create_coupling(diameter=self.val_diameter, length=self.val_length, d1=self.val_d1, d2=self.val_d2, d_middle=middle_diameter, insertion_length=self.val_hole_length, bevel=self.val_bevel, segments=self.val_segments)

		# 止めネジ穴を作る
		if self.val_setscrew:
			make_setscrew_holes(obj, coupling_diameter=self.val_diameter, coupling_length=self.val_length, diameter=self.val_setscrew_diameter, position=self.val_setscrew_position, angle=self.val_setscrew_angle, segments=self.val_setscrew_segments, threaded=self.val_setscrew_thread, thread_pitch=self.val_setscrew_thread_pitch, thread_depth=self.val_setscrew_thread_depth)

		# スリットを作成
		if self.val_slit:
			make_slit(obj, coupling_diameter=self.val_diameter, coupling_length=self.val_length, width=self.val_slit_thickness, distance=self.val_slit_interval, rotation_count=self.val_slit_count, segments=self.val_slit_segments)

		# オブジェクト名を設定
		obj.name = bpy.app.translations.pgettext_data('Coupling') + f'D{romly_utils.remove_decimal_trailing_zeros(self.val_diameter)}L{romly_utils.remove_decimal_trailing_zeros(self.val_length)}'



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
	self.layout.operator(ROMLYADDON_OT_add_coupling.bl_idname, text=bpy.app.translations.pgettext_iface('Add Coupling'), icon='MESH_CYLINDER')





classes = [
	ROMLYADDON_OT_add_coupling,
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
