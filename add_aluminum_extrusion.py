import bpy
import math
import mathutils
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import List, Tuple, NamedTuple



from . import romly_utils
























def mirror_point(point: Vector, normal: Vector) -> Vector:
	"""
	指定された点を、特定の法線を持つ平面に関してミラーリングします。

	Parameters
	----------
	point : mathutils.Vector
		ミラーリングする点の座標です❤
	normal : mathutils.Vector
		ミラーリング平面の法線ベクトルです❤

	Returns
	-------
	mathutils.Vector
		ミラーリングされた点の座標です❤
	"""
	# 法線を正規化します。
	normal_normalized = normal.normalized()
	# 点と法線の間の距離（内積を使って計算）。
	distance = point.dot(normal_normalized)
	# ミラーリングされた点を計算します。
	mirrored_point = point - 2 * distance * normal_normalized

	return mirrored_point










def find_intersection(line1_start: Vector, line1_end: Vector, line2_start: Vector, line2_end: Vector) -> Vector:
	"""
	二つの線分の交点を求める関数。

	Parameters
	----------
	line1_start : Vector
		線分1の始点。
	line1_end : Vector
		線分1の終点。
	line2_start : Vector
		線分2の始点。
	line2_end : Vector
		線分2の終点。

	Returns
	-------
	Vector or None
		二つの線分の交点。交点がなければNoneを返す。
	"""
	p = line1_start
	q = line2_start
	r = line1_end - line1_start
	s = line2_end - line2_start

	if r.cross(s).length == 0:
		# 線分が平行か重なっている場合
		return None

	t = (q - p).cross(s).length / r.cross(s).length
	u = (q - p).cross(r).length / r.cross(s).length

	if 0 <= t <= 1 and 0 <= u <= 1:
		# 交点が両線分上に存在する
		return p + t * r
	else:
		# 交点が存在しない
		return None








class AluminumExtrusionSpec(NamedTuple):
	size: float
	x_slots: int
	y_slots: int
	slot_width: float
	slot_wide_width: float
	core_width: float
	wall_thickness: float

	# 3つ以上連結する時の中間の壁の厚み。3090とかだと少し厚くて3mmになってる。
	middle_wall_thickness: float

	x_bone_thickness: float



	def make_topmiddle_left_vertices(self, middle: bool = False, core: bool = True) -> List[Vector]:
		"""中間となるフレーム形状の左側の頂点群を生成して返す"""
		diagonal_frame_horizontal_width = self.x_bone_thickness / math.sqrt(2) * 2
		diagonal_frame_root_pos = Vector((self.core_width / 2 - diagonal_frame_horizontal_width / 2, self.core_width / 2, 0))
		diagonal_frame_tip_pos = find_intersection(
			line1_start=diagonal_frame_root_pos,
			line1_end=diagonal_frame_root_pos + Vector((1, 1, 0)) * 1000,
			line2_start=Vector((self.slot_wide_width / 2, 1000, 0)),
			line2_end=Vector((self.slot_wide_width / 2, 0, 0)))

		vertices = []
		if core:
			vertices.append(Vector((0, 0, 0)))
		else:
			vertices.append(Vector((0, self.core_width / 2 - self.x_bone_thickness, 0)))
		vertices.append(Vector((0, self.core_width / 2, 0)))
		vertices.append(diagonal_frame_root_pos)
		vertices.append(diagonal_frame_tip_pos)
		vertices.append(Vector((self.slot_wide_width / 2, self.size / 2 - self.wall_thickness, 0)))
		vertices.append(Vector((self.slot_width / 2, self.size / 2 - self.wall_thickness, 0)))
		vertices.append(Vector((self.slot_width / 2, self.size / 2, 0)))
		vertices.append(Vector((self.size / 2, self.size / 2, 0)))	# 右上
		MIDDLE_WALL_THICKNESS = self.middle_wall_thickness if middle else self.wall_thickness
		vertices.append(Vector((self.size / 2, self.size / 2 - MIDDLE_WALL_THICKNESS, 0)))
		vertices.append(Vector((self.slot_wide_width / 2 + diagonal_frame_horizontal_width, self.size / 2 - MIDDLE_WALL_THICKNESS, 0)))
		diagonal_frame_tip_pos_right = diagonal_frame_tip_pos + Vector((diagonal_frame_horizontal_width, 0, 0))
		vertices.append(diagonal_frame_tip_pos_right)
		if core:
			vertices.append(diagonal_frame_root_pos + Vector((diagonal_frame_horizontal_width / 2, -diagonal_frame_horizontal_width / 2, 0)))
			vertices.append(Vector((self.core_width / 2, 0, 0)))
		else:
			vertices.append(find_intersection(
				line1_start=Vector((0, self.core_width / 2 - self.x_bone_thickness, 0)),
				line1_end=Vector((1000, self.core_width / 2 - self.x_bone_thickness, 0)),
				line2_start=diagonal_frame_tip_pos_right,
				line2_end=diagonal_frame_tip_pos_right + Vector((-1, -1, 0)) * 1000))
		return vertices



	def make_topmiddle_right_vertices(self, middle: bool = False, core: bool = True) -> List[Vector]:
		"""中間となるフレーム形状の右側の頂点群を生成して返す"""
		left_vertices = self.make_topmiddle_left_vertices(middle, core=core)
		mirror_normal = Vector((-1, 0, 0))
		vertices = []
		for i in range(len(left_vertices)):
			vertices.append(mirror_point(left_vertices[i], normal=mirror_normal))
		return vertices








def make_topleft_vertices(spec: AluminumExtrusionSpec) -> List[Vector]:
	frame_width = frame_height = spec.size
	diagonal_frame_horizontal_width = spec.x_bone_thickness / math.sqrt(2) * 2

	vertices = []
	vertices.append(Vector((0, 0, 0)))
	vertices.append(Vector((-spec.core_width / 2, 0, 0)))
	v1 = Vector((-spec.core_width / 2, spec.core_width / 2 - diagonal_frame_horizontal_width / 2, 0))
	vertices.append(v1)
	vertices.append(find_intersection(
		line1_start=v1,
		line1_end=v1 + Vector((-1, 1, 0)) * 1000,
		line2_start=Vector((-1000, spec.slot_wide_width / 2, 0)),
		line2_end=Vector((0, spec.slot_wide_width / 2, 0))))
	vertices.append(Vector((-frame_width / 2 + spec.wall_thickness, spec.slot_wide_width / 2, 0)))
	vertices.append(Vector((-frame_width / 2 + spec.wall_thickness, spec.slot_width / 2, 0)))
	vertices.append(Vector((-frame_width / 2, spec.slot_width / 2, 0)))
	vertices.append(Vector((-frame_width / 2, frame_height / 2, 0)))	# 左上

	vertices.append(Vector((-spec.slot_width / 2, frame_height / 2, 0)))
	vertices.append(Vector((-spec.slot_width / 2, frame_height / 2 - spec.wall_thickness, 0)))
	vertices.append(Vector((-spec.slot_wide_width / 2, frame_height / 2 - spec.wall_thickness, 0)))
	v2 = Vector((-spec.core_width / 2 + diagonal_frame_horizontal_width / 2, spec.core_width / 2, 0))
	vertices.append(find_intersection(
		line1_start=v2,
		line1_end=v2 + Vector((-1, 1, 0)) * 1000,
		line2_start=Vector((-spec.slot_wide_width / 2, 1000, 0)),
		line2_end=Vector((-spec.slot_wide_width / 2, 0, 0))))
	vertices.append(v2)
	vertices.append(Vector((0, spec.core_width / 2, 0)))

	return vertices





def make_topright_vertices(spec: AluminumExtrusionSpec) -> List[Vector]:
	topleft_vertices = make_topleft_vertices(spec)
	vertices = []
	for i in range(len(topleft_vertices)):
		vertices.append(mirror_point(topleft_vertices[i], normal=Vector((-1, 0, 0))))
	return vertices






def make_leftmiddle_top_vertices(spec: AluminumExtrusionSpec) -> List[Vector]:
	topmiddle_left_vertices = spec.make_topmiddle_left_vertices()
	vertices = []
	for v in topmiddle_left_vertices:
		vertices.append(mirror_point(v, normal=Vector((1, 1, 0))))
	return vertices



def make_leftmiddle_bottom_vertices(spec: AluminumExtrusionSpec) -> List[Vector]:
	topmiddle_right_vertices = make_leftmiddle_top_vertices(spec)
	vertices = []
	for v in topmiddle_right_vertices:
		vertices.append(mirror_point(v, normal=Vector((0, 1, 0))))
	return vertices





def make_aluminum_extrusion_bottom(spec: AluminumExtrusionSpec) -> Tuple[List[Vector], List[List[int]]]:
	"""
	アルミフレームの断面図となる形状を作成する。

	Parameters
	----------
	sepc : AluminumExtrusionSpec
		アルミフレームの仕様（大きさ）。

	Returns
	-------
	Tuple[List[Vector], List[List[int]]]
		断面図を構成する頂点リストと面リスト。
	"""
	vertices = []
	faces = []



	def aiueo(new_vertices: List[Vector], offset: Vector, mirror_normal: Vector):
		old_len1 = len(vertices)
		for i in range(len(new_vertices)):
			vertices.append(new_vertices[i] + offset)
		faces.append(list(range(old_len1, len(vertices))))

		# mirror_normalを法線とする平面でミラーリングして反対側を作成
		old_len2 = len(vertices)
		for i in range(old_len1, len(vertices)):
			vertices.append(mirror_point(vertices[i], normal=mirror_normal))
		faces.append(list(range(old_len2, len(vertices))))



	# 上側と下側の構造を作成
	offset = Vector((-spec.size * (spec.x_slots - 1) / 2, spec.size * (spec.y_slots - 1) / 2, 0))
	mirror_normal = Vector((0, -1, 0))
	for i in range(spec.x_slots):
		MIDDLE = spec.x_slots >= 3
		CORE = not (spec.y_slots >= 2 and spec.x_slots >= 3 and 0 < i < spec.x_slots - 1)
		if i == 0:
			aiueo(make_topleft_vertices(spec), offset=offset, mirror_normal=mirror_normal)
		else:
			aiueo(spec.make_topmiddle_right_vertices(MIDDLE, core=CORE), offset=offset, mirror_normal=mirror_normal)
		if i < spec.x_slots - 1:
			aiueo(spec.make_topmiddle_left_vertices(MIDDLE, core=CORE), offset=offset, mirror_normal=mirror_normal)
		else:
			aiueo(make_topright_vertices(spec), offset=offset, mirror_normal=mirror_normal)
		offset += Vector((spec.size, 0, 0))

	# 左側と右側の構造を作成
	offset = Vector((-spec.size * (spec.x_slots - 1) / 2, spec.size * (spec.y_slots - 1) / 2 - spec.size, 0))
	mirror_normal = Vector((-1, 0, 0))
	for i in range(1, spec.y_slots):
		aiueo(make_leftmiddle_top_vertices(spec), offset=offset + Vector((0, spec.size, 0)), mirror_normal=mirror_normal)
		aiueo(make_leftmiddle_bottom_vertices(spec), offset=offset, mirror_normal=mirror_normal)
		offset += Vector((0, -spec.size, 0))

	return vertices, faces




















SIZE_2020 = '2020'
SIZE_2040 = '2040'
SIZE_2060 = '2060'
SIZE_3030 = '3030'
SIZE_3060 = '3060'
SIZE_3090 = '3090'
SIZE_6090 = '6090'










def on_length_presets_update(self, context):
	self.val_length = int(self.val_length_presets)



def on_size_update(self, context):
	""" アルミフレームのサイズ（種類）変更時の処理。各プロパティをサイズごとの規定値に戻す。 """
	if self.val_size == SIZE_2020 or self.val_size == SIZE_2040 or self.val_size == SIZE_2060:
		self.val_base_size = 20
		if self.val_size == SIZE_2040:
			self.val_x_slots = 2
		elif self.val_size == SIZE_2060:
			self.val_x_slots = 3
		else:
			self.val_x_slots = 1
		self.val_y_slots = 1
		self.val_slot_width = 6
		self.val_slot_wide_width = 12
		self.val_core_width = 8
		self.val_thickness = 2
		self.val_middle_wall_thickness = 2
		self.val_x_bone_thickness = 1.5
		self.val_center_hole_diameter = 4.2
		self.val_corner_hole_diameter = 0
		self.val_bevel_width = 1

	elif self.val_size == SIZE_3030 or self.val_size == SIZE_3060 or self.val_size == SIZE_3090 or self.val_size == SIZE_6090:
		self.val_base_size = 30
		if self.val_size == SIZE_3060:
			self.val_x_slots = 2
			self.val_y_slots = 1
			self.val_middle_wall_thickness = 3
		elif self.val_size == SIZE_3090:
			self.val_x_slots = 3
			self.val_y_slots = 1
			self.val_middle_wall_thickness = 3
		elif self.val_size == SIZE_6090:
			self.val_x_slots = 3
			self.val_y_slots = 2
			self.val_middle_wall_thickness = 3
		else:
			self.val_x_slots = 1
			self.val_y_slots = 1
			self.val_middle_wall_thickness = 2
		self.val_slot_width = 8
		self.val_slot_wide_width = 16.5
		self.val_core_width = 12
		self.val_thickness = 2
		self.val_x_bone_thickness = 2
		self.val_center_hole_diameter = 6.8
		self.val_corner_hole_diameter = 4.2
		self.val_bevel_width = 2










def make_corner_holes(object, spec: AluminumExtrusionSpec, diameter: float, space: float, keep_modifiers = False, vertices: int = 32):
	HOLE_X = space / 2 + spec.size / 2 * (spec.x_slots - 1)
	HOLE_Y = space / 2 + spec.size / 2 * (spec.y_slots - 1)
	locations = [
		(-HOLE_X, HOLE_Y, 0),
		(HOLE_X, HOLE_Y, 0),
		(-HOLE_X, -HOLE_Y, 0),
		(HOLE_X, -HOLE_Y, 0)
	]

	# 全体を貫くのに十分な長さ
	depth = object.dimensions[2] * 2.1

	for l in locations:
		bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=diameter / 2, depth=depth, enter_editmode=False, align='WORLD', location=l, scale=(1, 1, 1))
		toolObj = bpy.data.objects[bpy.context.active_object.name]
		romly_utils.apply_boolean_object(object=object, boolObject=toolObj, unlink=not keep_modifiers, apply=not keep_modifiers)










def make_corner_bevels(object: bpy.types.Object, frame_size: float, x_slots: int, y_slots: int):
	"""アルミフレームの四隅の辺にベベルウェイトを設定する。

	Parameters
	----------
	object : bpy.types.Object
		アルミフレームのオブジェクト
	frame_size : float
		アルミフレームの基本サイズ。四隅の座標の計算に使う。
	x_slots : int
		アルミフレームの横の連結数。四隅の座標の計算に使う。
	y_slots : int
		アルミフレームの縦の連結数。四隅の座標の計算に使う。
	"""
	# アルミフレームの四隅の座標
	CORNER_POINTS = [
		Vector((-frame_size * x_slots / 2, frame_size * y_slots / 2, 0)),
		Vector((frame_size * x_slots / 2, frame_size * y_slots / 2, 0)),
		Vector((-frame_size * x_slots / 2, -frame_size * y_slots / 2, 0)),
		Vector((frame_size * x_slots / 2, -frame_size * y_slots / 2, 0))
	]

	def is_near_xy(a: Vector, b: Vector) -> bool:
		"""2つの座標が同じ座標にあるか調べる。Z座標は無視する。"""
		EPSILON = 0.001
		return abs(a[0] - b[0]) < EPSILON and abs(a[1] - b[1]) < EPSILON

	def is_near_to_corners_xy(point: Vector) -> bool:
		"""指定された座標がアルミフレームの四隅の座標と一致するか調べる。Z座標は無視する。"""
		for corner_point in CORNER_POINTS:
			if is_near_xy(corner_point, point):
				return True
		return False

	bpy.context.view_layer.objects.active = object
	bpy.ops.object.mode_set(mode='EDIT')

	# Bevel Weightを設定
	mesh = bmesh.from_edit_mesh(object.data)

	# Bevel Weightのレイヤーを取得（存在しない場合は新しく作成）
	bevel_layer = mesh.edges.layers.float.get('bevel_weight_edge', mesh.edges.layers.float.new('bevel_weight_edge'))

	# 四隅の座標とXYが一致し、Z軸に伸びる辺にBevel Weightを設定
	for edge in mesh.edges:
		if is_near_to_corners_xy(edge.verts[0].co) and is_near_xy(edge.verts[0].co, edge.verts[1].co):
			edge[bevel_layer] = 1.0

	# オブジェクトモードに戻す
	bpy.ops.object.mode_set(mode='OBJECT')









def cleanup_interior_faces(object: bpy.types.Object) -> None:
	bpy.context.view_layer.objects.active = object
	bpy.ops.object.mode_set(mode='EDIT')

	# 内部の面を選択
	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.mesh.select_interior_faces()

	# 選択した面を削除
	bpy.ops.mesh.delete(type='FACE')
	bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
	bpy.ops.object.mode_set(mode='OBJECT')


	# 平面上にある辺（融解すべきもの）を選択
	# いちいち編集モードを切り替えてるのはなぜかこうしないと選択されないため。たぶんモード切替時に内部で必要な処理が走ってるっぽい。
	bpy.ops.object.mode_set(mode='EDIT')
	romly_utils.select_edges_on_fair_surface(object)
	bpy.ops.object.mode_set(mode='OBJECT')


	# 辺を融解
	# こちらも同様にいちいち編集モードを切り替える必要がある
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.dissolve_edges()
	bpy.ops.object.mode_set(mode='OBJECT')










def make_holes(object: bpy.types.Object, spec: AluminumExtrusionSpec, center_hole_diameter: float, corner_hole_diameter: float, corner_hole_space: float, vertices: int) -> None:
	# 穴を開ける時のブーリアンモデファイアとシリンダーを残すか。デバッグ用。
	DEBUG_KEEP_HOLE_MODS = False

	# 中心に穴を開ける
	for x in range(spec.x_slots):
		for y in range(spec.y_slots):
			center = [0, 0, 0]
			center[0] = spec.size * x - 0.5 * spec.size * (spec.x_slots - 1)
			center[1] = -spec.size * y + 0.5 * spec.size * (spec.y_slots - 1)
			bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=center_hole_diameter / 2, depth=object.dimensions[2] * 2.1, enter_editmode=False, align='WORLD', location=center, scale=(1, 1, 1))
			toolObj = bpy.data.objects[bpy.context.active_object.name]
			romly_utils.apply_boolean_object(object=object, boolObject=toolObj, unlink=not DEBUG_KEEP_HOLE_MODS, apply=not DEBUG_KEEP_HOLE_MODS)

	# 四隅に穴を開ける
	if corner_hole_diameter > 0:
		make_corner_holes(object, spec=spec, diameter=corner_hole_diameter, space=corner_hole_space, keep_modifiers=DEBUG_KEEP_HOLE_MODS, vertices=vertices)

	# 四隅のベベルを作成
	make_corner_bevels(object, frame_size=spec.size, x_slots=spec.x_slots, y_slots=spec.y_slots)










class ROMLYADDON_OT_add_aluminum_extrusion(bpy.types.Operator):
	bl_idname = "romlyaddon.add_aluminum_extrusion"
	bl_label = bpy.app.translations.pgettext_iface('Add Aluminium Extrusion')
	bl_description = 'Construct an aluminum extrusion'
	bl_options = {'REGISTER', 'UNDO'}

	LENGTH_PRESET_ITEMS = [
		('100', '100', 'Set length to 100 mm'),
		('150', '150', 'Set length to 150 mm'),
		('200', '200', 'Set length to 200 mm'),
		('250', '250', 'Set length to 250 mm'),
		('300', '300', 'Set length to 300 mm'),
		('400', '400', 'Set length to 400 mm'),
		('500', '500', 'Set length to 500 mm'),
	]

	# 長さ
	val_length: FloatProperty(name='Length', description='The length of the extrusion', default=100.0, min=1.0, soft_max=1000.0, step=1, precision=2, unit='LENGTH')
	val_length_presets: EnumProperty(name='Length Presets', description='The length of the extrusion', default='100', items=LENGTH_PRESET_ITEMS, update=on_length_presets_update)

	# アルミフレームの種類（大きさ）
	SIZE_ITEMS = [
		(SIZE_2020, '2020', 'Set specs as the 2020 size'),
		(SIZE_2040, '2040', 'Set specs as the 2040 size'),
		(SIZE_2060, '2060', 'Set specs as the 2060 size'),
		(SIZE_3030, '3030', 'Set specs as the 3030 size'),
		(SIZE_3060, '3060', 'Set specs as the 3060 size'),
		(SIZE_3090, '3090', 'Set specs as the 3090 size'),
		(SIZE_6090, '6090', 'Set specs as the 6090 size'),
	]
	val_size: EnumProperty(name='Size', description='The size (type) of the aluminum extrusion', default=SIZE_2020, items=SIZE_ITEMS, update=on_size_update)

	# 基本サイズ（角サイズ）
	val_base_size: FloatProperty(name='Frame Size', description='The basic frame size', default=20.0, min=1.0, soft_min=10, soft_max=80.0, step=1, precision=2, unit='LENGTH')

	# フレームの溝の数（列数）
	val_x_slots: IntProperty(name='X Slots', description='The number of slots in the X direction', default=1, min=1, soft_max=4, max=10)
	val_y_slots: IntProperty(name='Y Slots', description='The number of slots in the Y direction', default=1, min=1, soft_max=4, max=10)

	# 溝の幅
	val_slot_width: FloatProperty(name='Slot Width', description='The width of the slot', default=6.0, min=1.0, soft_max=20.0, step=1, precision=2, unit='LENGTH')
	val_slot_wide_width: FloatProperty(name='Inner Slot Width', description='The inner width of the slot', default=12.0, min=1.0, soft_max=20.0, step=1, precision=2, unit='LENGTH')

	# 芯の幅
	val_core_width: FloatProperty(name='Core Width', description='The width of the core part', default=8.0, min=1.0, soft_max=20.0, step=1, precision=2, unit='LENGTH')

	# 厚み
	val_thickness: FloatProperty(name='Wall Thickness', description='The thickness of the walls sandwiching the slot', default=2.0, min=1.0, soft_max=4.0, step=1, precision=4, unit='LENGTH')
	val_middle_wall_thickness: FloatProperty(name='Middle Wall Thickness', description='The thickness of the walls in the middle column', default=2.0, min=1.0, soft_max=4.0, step=1, precision=4, unit='LENGTH')

	# 中心の穴の直径
	val_center_hole_diameter: FloatProperty(name='Center Hole Diameter', description='The diameter of the center hole', default=4.0, min=0.0, soft_max=10.0, step=1, precision=4, unit='LENGTH')

	# X構造の厚み
	val_x_bone_thickness: FloatProperty(name='X Bone Thickness', description='The thickness of the X bone', default=1.5, min=1.0, soft_max=3.0, step=1, precision=2, unit='LENGTH')

	# 四隅の穴の直径と位置
	val_corner_hole_diameter: FloatProperty(name='Diameter', description='The diameter of the center hole', default=0.0, min=0.0, soft_max=10.0, step=1, precision=2, unit='LENGTH')
	val_corner_hole_space: FloatProperty(name='Distance', description='The distance between corner holes', default=23.2, min=0.0, soft_max=30.0, step=1, precision=4, unit='LENGTH')
	val_hole_segments: IntProperty(name='Hole Segments', description='The number of segments in the holes', default=16, min=6, soft_max=64, max=128, step=1)

	# 四隅のベベル
	val_bevel_width: FloatProperty(name='Width', description='The bevel width of the corner bevels', default=1.0, min=0.0, soft_max=4.0, step=1, precision=2, unit='LENGTH')
	val_bevel_segments: IntProperty(name='Bevel Segments', description='The number of segments in the corner bevels', default=5, min=1, soft_max=10, max=32, step=1)
	val_keep_modifiers: BoolProperty(name='Keep Modifiers', description="Keep modifiers if it's checked", default=False)


	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_length')
		row = col.row(align=True)
		row.prop(self, 'val_length_presets', expand=True)
		col.separator()

		col.label(text='Template')
		row = col.row(align=True)
		row.prop(self, 'val_size', expand=True)
		col.separator()

		col.label(text='Specs')
		col.prop(self, 'val_base_size')
		row = col.row(align=True)
		row.prop(self, 'val_x_slots')
		row.prop(self, 'val_y_slots')
		col.separator()

		col.prop(self, 'val_slot_width')
		col.prop(self, 'val_slot_wide_width')
		col.prop(self, 'val_core_width')
		col.prop(self, 'val_thickness')
		col.prop(self, 'val_middle_wall_thickness')
		col.prop(self, 'val_x_bone_thickness')
		col.prop(self, 'val_center_hole_diameter')
		col.separator()

		col.label(text='Corner Holes')
		row = col.row(align=True)
		row.prop(self, 'val_corner_hole_diameter')
		row.prop(self, 'val_corner_hole_space')
		col.separator()

		col.label(text='Corner Bevel')
		col.prop(self, 'val_bevel_width')
		col.prop(self, 'val_keep_modifiers')
		col.separator()

		col.label(text='Mesh')
		col.prop(self, 'val_hole_segments')
		col.prop(self, 'val_bevel_segments')




	def execute(self, context):
		# パラメータを取得
		length = self.val_length
		bevel_width = self.val_bevel_width
		bevel_segments = self.val_bevel_segments
		hole_segments = self.val_hole_segments

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 掃引のもとになる形状を作成
		aluminum_extrusion_spec = AluminumExtrusionSpec(
			size=self.val_base_size,
			x_slots=self.val_x_slots,
			y_slots=self.val_y_slots,
			slot_width=self.val_slot_width,
			slot_wide_width=self.val_slot_wide_width,
			core_width=self.val_core_width,
			wall_thickness=self.val_thickness,
			middle_wall_thickness=self.val_middle_wall_thickness,
			x_bone_thickness=self.val_x_bone_thickness)
		vertices, faces = make_aluminum_extrusion_bottom(aluminum_extrusion_spec)

		# 掃引
		extrude_faces = []
		for face in faces:
			romly_utils.extrude_face(vertices, extrude_faces, extrude_vertex_indices=face, z_offset=length)
		faces.extend(extrude_faces)

		obj = romly_utils.cleanup_mesh(romly_utils.create_object(vertices, faces=faces, name='Aluminum Extrusion'))
		bpy.context.collection.objects.link(obj)



		# 連結部に残ってしまった面（立体の内部にある面）を削除する
		cleanup_interior_faces(obj)


		bpy.context.view_layer.objects.active = obj

		make_holes(obj, aluminum_extrusion_spec, center_hole_diameter=self.val_center_hole_diameter, corner_hole_diameter=self.val_corner_hole_diameter, corner_hole_space=self.val_corner_hole_space, vertices=hole_segments)



		obj = romly_utils.cleanup_mesh(obj)

		# ベベルを追加。ベベルは幅が0だと適用するとエラーになるので、0より大きい場合にのみ追加する
		if bevel_width > 0:
			mod = bpy.context.object.modifiers.new(type='BEVEL', name='Bevel')
			mod.width = bevel_width
			mod.segments = bevel_segments
			mod.limit_method = 'WEIGHT'



		# オブジェクトを3Dカーソル位置へ移動
		obj.location = bpy.context.scene.cursor.location

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}










class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_aluminum_extrusion.bl_idname, text=bpy.app.translations.pgettext_iface('Add Aluminium Extrusion'), icon='FIXED_SIZE')









# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	# 翻訳辞書の登録
	bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)

	bpy.utils.register_class(ROMLYADDON_OT_add_aluminum_extrusion)
	bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	try:
		bpy.utils.unregister_class(ROMLYADDON_OT_add_aluminum_extrusion)
	except RuntimeError:
		pass
	try:
		bpy.utils.unregister_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	except RuntimeError:
		pass
	bpy.types.VIEW3D_MT_add.remove(menu_func)

	# 翻訳辞書の登録解除
	bpy.app.translations.unregister(__name__)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	# 既に登録されていないかのチェック。テキストエディタから直接実行する時に必要
	if 'bpy' in locals():
		unregister()
	register()
