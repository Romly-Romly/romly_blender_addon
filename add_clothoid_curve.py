import bpy
import math
import mathutils
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import List, Tuple, NamedTuple, Union



from . import romly_utils












def tangent_at(a: float, t: float) -> Tuple[float, float]:
	"""
	クロソイド曲線での指定された位置での接線の角度を求める（接線を斜辺とする三角形の底辺と高さを返す）。

	Parameters
	----------
	a : _type_
		クロソイドパラメーター(A)
	t : _type_
		クロソイド曲線上の位置を示す割合

	Returns
	-------
	Tuple[float, float]
		クロソイド曲線上の位置tを頂点とし、接線を斜辺に取る直角三角形の底辺の長さと高さを返す。
	"""
	angle = 0.5 * a * t * t
	return math.cos(angle), math.sin(angle)





class ClothoidCurveVertices(NamedTuple):
	"""
	make_clothoid_curve_vertices の戻り値を格納する NamedTuple

	Attributes
	----------
	vertices: List[Vector]
		生成したクロソイド曲線の頂点群
	osculating_circle_radius: float
		曲線の終点での接触円の半径
	osculating_circle_center: Vector
		曲線の終点での接触円の中心座標
	angle_radians: float
		曲線の終点での接触角度。X軸プラスベクトルを左回りにこの角度だけ回転すると終点からまっすぐ伸ばした線になり、Y軸プラスベクトルを左回りにこの角度だけ回転すると終点での垂直線（接触円に向かう直線）の向きになる。
	"""
	vertices: List[Vector]
	osculating_circle_radius: float
	osculating_circle_center: Vector
	angle_radians: float





# MARK: create_clothoid_curve_vertices
def create_clothoid_curve_vertices(clothoid_param_A: float, curve_length: float, num_vertices: int, t_max: float = math.inf) -> ClothoidCurveVertices:
	"""

	Parameters
	----------
	clothoid_param_A : float
		クロソイドパラメーター
	curve_length : float
		曲線長
	num_vertices : int
		いくつの頂点を作成するか。少ないと当然粗くなるよ。
	t_max : float, optional
		どこまでクロソイド曲線を描くか。指定しない場合は曲線長から最大値を決定する。
		t_max = curve_length ** 2 / (clothoid_param_A ** 2 * math.pi)

		例えば45度になったら止めたい場合は下記のように指定する。
		t_max = math.sqrt((2 * math.radians(45)) / clothoid_param_A)

	Returns
	-------
	ClothoidCurveVertices
		生成した頂点群と終点での接触円に関する情報を返す。
	"""

	def euler_spiral(a, t):
		"""クロソイド曲線（オイラー螺旋）を描く関数。指定された位置（時間、割合、進み具合）における座標を返す。"""
		x = 0
		y = 0
		dt = 0.01 # 時間の刻み幅。細かいほどスムーズなカーブになる。
		for i in range(int(t / dt)):
			angle = 0.5 * a * dt * dt * (i ** 2)
			dx = math.cos(angle) * dt
			dy = math.sin(angle) * dt
			x += dx
			y += dy
		return x, y

	# Function to calculate radius of osculating circle
	def radius_of_curvature(a, t):
		"""クロソイド曲線の指定された位置における接触円の半径を返す関数。"""

		# ゼロ除算エラー回避。クロソイド曲線の始点では半径は無限大となる。
		if t == 0:
			return math.inf
		return 1 / (a * t)


	if math.isinf(t_max):
		t_max = curve_length ** 2 / (clothoid_param_A ** 2 * math.pi)

	step = t_max / num_vertices
	t_values = [i * step for i in range(num_vertices + 1)]
	vertices = []
	radius = 0
	center_x, center_y = 0, 0
	angle_radians = 0
	for t in t_values:
		x, y = euler_spiral(clothoid_param_A, t)
		vertices.append((x, y, 0))

		if t > 0:
			tangent_x, tangent_y = tangent_at(clothoid_param_A, t)
			radius = radius_of_curvature(clothoid_param_A, t)
			center_x = x - radius * tangent_y
			center_y = y + radius * tangent_x

			angle_radians = math.atan2(tangent_y, tangent_x)

	return ClothoidCurveVertices(vertices=vertices, osculating_circle_radius=radius, osculating_circle_center=Vector((center_x, center_y, 0)), angle_radians=angle_radians)









def translate_vertices(vertices: List[Union[Vector, Tuple[float, float, float]]], offset: Vector) -> List[Vector]:
	"""
	頂点リストを平行移動する。頂点はVectorでもタプルでもOKだけど、返り値のリストはVectorに統一される。

	Parameters
	----------
	vertices : List[Union[Vector, Tuple[float, float, float]]]
		頂点リスト。Vectorでもタプル(0, 0, 0)でもOK。
	offset : Vector
		移動する距離。こっちはVectorで指定してちょ。

	Returns
	-------
	List[Vector]
		移動した頂点リスト。
	"""
	result = []
	for v in vertices:
		if isinstance(v, Vector):
			result.append(v + offset)
		else:
			result.append(Vector(v) + offset)
	return result










# MARK: create_clothoid_only_corner_vertices
def create_clothoid_only_corner_vertices(clothoid_param_A: float, curve_length: float, num_curve_vertices: int) -> List[Tuple[float, float, float]]:
	"""
	クロソイド曲線のみを使った角部分の頂点群を作成する。X軸プラス方向からY軸プラス方向へ90度曲がる軌跡の頂点群で、開始座標は(0, 0, 0)、終了座標は第1象限のどこか。
	接線が45度になるまでのクロソイド曲線と、その曲線を反転した曲線で90度曲がる感じ。

	Parameters
	----------
	clothoid_param_A : float
		クロソイドパラメーター
	curve_length : float
		クロソイド曲線の曲線長。クロソイド曲線を決定するのに使われるだけで、この長さになるわけではない。
	num_curve_vertices : int
		いくつの頂点を作成するか。少ないと当然荒い曲線になっちゃうよ。

	Returns
	-------
	List[Tuple[float, float, float]]
		頂点群
	"""

	# 45度になるときのtを求める
	t = math.sqrt((2 * math.radians(45)) / clothoid_param_A)

	# そのtまでのクロソイド曲線を作成
	clothoid_vertices = create_clothoid_curve_vertices(
		clothoid_param_A=clothoid_param_A,
		curve_length=curve_length,
		num_vertices=num_curve_vertices,
		t_max=t)

	# 後半部分を作成
	ending_vertices = []
	for v in reversed(clothoid_vertices.vertices):
		vec = Quaternion(Vector((0, 0, 1)), math.radians(90)) @ Vector(v)
		vec = Vector((vec[0], -vec[1], vec[2]))
		ending_vertices.append(tuple(vec))
	offset = Vector(ending_vertices[0])
	for i, v in enumerate(ending_vertices):
		ending_vertices[i] = tuple(Vector(ending_vertices[i]) - offset + Vector(clothoid_vertices.vertices[-1]))

	return clothoid_vertices.vertices + ending_vertices










# MARK: create_clothoid_and_arc_corner_vertices
def create_clothoid_and_arc_corner_vertices(clothoid_param_A: float, curve_length: float, num_curve_vertices: int, num_arc_vertices: int) -> Tuple[List[Vector], float]:
	"""
	クロソイド曲線による緩和区間 → 円弧部分 → クロソイド曲線による緩和区間で構成される角部分の頂点群を作成する。
	クロソイド区間のみで接角が45度に到達してしまった場合は円弧部分は省略され、そのまま再びクロソイド区間となる。

	Parameters
	----------
	clothoid_param_A : float
		クロソイドパラメーター
	curve_length : float
		曲線長。クロソイド区間は最大でも接角が45度になるまでしか作られないので、必ずこの長さになるわけではない。
	num_curve_vertices : int
		クロソイド曲線区間それぞれの頂点数。
	num_arc_vertices : int
		円弧部分の頂点数。

	Returns
	-------
	Tuple[List[Vector], float]
		作成した頂点のリストと、円弧部分の角度（ラジアン）を返す。
	"""

	def mirror_vertices_45degree(vertices: List[Vector]) -> List[Vector]:
		result = []
		for v in reversed(vertices):
			v = Quaternion(Vector((0, 0, 1)), math.radians(90)) @ Vector(v)
			v = Vector((v[0], -v[1], v[2]))
			result.append(v)
		return translate_vertices(result, -result[0])



	# 曲線長Lからtの最大値を求める
	t_max = curve_length ** 2 / (clothoid_param_A ** 2 * math.pi)

	# 接角が45度になるときのtを求める
	t_45 = math.sqrt((2 * math.radians(45)) / clothoid_param_A)

	# 接角が45度になるときの t_45 が、t_max 以上の場合はクロソイド曲線の終点で45度未満ということなので普通に作成、そうでない場合はクロソイド区間のみで最後まで曲がるように作成
	corner_vertices = []
	arc_angle = 0
	if t_45 >= t_max:
		# クロソイド区間の頂点群を作成
		clothoid_vertices = create_clothoid_curve_vertices(
			clothoid_param_A=clothoid_param_A,
			curve_length=curve_length,
			num_vertices=num_curve_vertices,
			t_max=t_max)

		# 円弧部の角度を求める（クロソイド区間の終点の接角と45度の差を2倍した値）
		arc_angle = (math.pi / 4 - clothoid_vertices.angle_radians) * 2

		# 後半のクロソイド区間の開始座標を求める
		# Y軸マイナス方向に接触円の半径だけ伸びたベクトルを、［最初のクロソイド区間の終点の接角＋円弧部の角度］だけ回転し、接触円の中心座標を加算すると求まる。
		ending_clothoid_start = Vector((0, -clothoid_vertices.osculating_circle_radius, 0))
		ending_clothoid_start = Quaternion(Vector((0, 0, 1)), clothoid_vertices.angle_radians + arc_angle) @ ending_clothoid_start
		ending_clothoid_start = clothoid_vertices.osculating_circle_center + ending_clothoid_start

		# クロソイド部分、円弧部分、クロソイド部分を含む頂点群を作成
		corner_vertices = []
		corner_vertices.extend(clothoid_vertices.vertices)

		# 円弧部
		# クロソイド区間の終点での角度（X軸と接線との角度、Y軸マイナス方向と垂線の角度）が、45度未満なら円弧部を作成
		if arc_angle > 0:
			arc_vertices = romly_utils.create_circle_vertices(
				radius=clothoid_vertices.osculating_circle_radius,
				num_vertices=num_arc_vertices, center=(0, 0, 0),
				start_angle_degree=270 + math.degrees(clothoid_vertices.angle_radians),
				angle_degree=math.degrees(arc_angle))
			arc_vertices = translate_vertices(arc_vertices, clothoid_vertices.osculating_circle_center)
			corner_vertices.extend(arc_vertices)

		# 後半のクロソイド部分。前半のクロソイド区間の頂点群から作成。
		corner_vertices.extend(translate_vertices(mirror_vertices_45degree(clothoid_vertices.vertices), ending_clothoid_start))

	else:
		# 指定されたクロソイドパラメーターと曲線長でクロソイド区間を作った時に接角が45度以上になったので、クロソイド区間のみで角を作成する処理へ
		corner_vertices = create_clothoid_only_corner_vertices(clothoid_param_A=clothoid_param_A, curve_length=curve_length, num_curve_vertices=num_curve_vertices)
		# この場合、円弧部分は作成されないので、円弧部分の角度は0
		arc_angle = 0

	return corner_vertices, arc_angle











# MARK: create_clothoid_corner_rectangle
def create_clothoid_corner_rectangle(clothoid_param_A: float, curve_length: float, num_curve_vertices: int, num_arc_vertices: int, rectangle_width: float, rectangle_height: float) -> Tuple[List[Vector], float, float]:
	"""
	クロソイド曲線と円弧を使った角丸を持つ矩形の頂点群を作成する。

	Parameters
	----------
	clothoid_param_A : float
		クロソイドパラメーター
	curve_length : float
		曲線長。クロソイド区間は最大でも接角が45度になるまでしか作られないので、必ずこの長さになるわけではない。
	num_curve_vertices : int
		クロソイド曲線区間それぞれの頂点数。
	num_arc_vertices : int
		円弧部分の頂点数。
	rectangle_width : float
		矩形の幅（X軸方向のお大きさ）。角丸部分を含む、全体の幅。
	rectangle_height : float
		矩形の高さ（Y軸方向の大きさ）。角丸部分を含む、全体の高さ。

	Returns
	-------
	Tuple[List[Vector], float, float]
		矩形の頂点群、円弧部分の角度、角丸部分全体の幅（高さ）
	"""

	# 角部分の頂点群を作成
	corner_vertices, arc_angle = create_clothoid_and_arc_corner_vertices(
		clothoid_param_A=clothoid_param_A,
		curve_length=curve_length,
		num_curve_vertices=num_curve_vertices,
		num_arc_vertices=num_arc_vertices)
	corner_width = corner_vertices[-1][0]

	# 角丸部分の大きさが矩形の大きさを越えてしまった場合、矩形サイズに収まるよう縮小する
	corner_scale = 1.0
	if corner_width > min(rectangle_width / 2, rectangle_height / 2):
		corner_scale = min(rectangle_width / 2, rectangle_height / 2) / corner_width
		corner_vertices = [Vector(v) * corner_scale for v in corner_vertices]

	all_vertices = []
	straight_edge_width = rectangle_width - corner_vertices[-1][0] * 2
	straight_edge_height = rectangle_height - corner_vertices[-1][1] * 2
	for v in corner_vertices:
		v = Vector(v) + Vector((straight_edge_width / 2, 0, 0))
		all_vertices.append(tuple(v))
	# 右上の角：右下の角の頂点群を上下反転して右上に移動
	for v in reversed(corner_vertices):
		v = Vector((v[0], -v[1], v[2])) + Vector((straight_edge_width / 2, corner_vertices[-1][1] * 2 + straight_edge_height, 0))
		all_vertices.append(tuple(v))
	# 左上の角：右下の角の頂点群を左右／上下反転して左上に移動
	for v in corner_vertices:
		v = Vector((-v[0], -v[1], v[2])) + Vector((-straight_edge_width / 2, corner_vertices[-1][1] * 2 + straight_edge_height, 0))
		all_vertices.append(tuple(v))
	# 左下の角：右下の角の頂点群を左右反転して左下に移動
	for v in reversed(corner_vertices):
		v = Vector((-v[0], v[1], v[2])) + Vector((-straight_edge_width / 2, 0, 0))
		all_vertices.append(tuple(v))

	# Y方向中央に移動
	all_vertices = translate_vertices(all_vertices, Vector((0, -rectangle_height / 2, 0)))

	return all_vertices, arc_angle, corner_width, corner_scale










CURVE_SPECIFICATION_BY_RL = 'R_and_L'
CURVE_SPECIFICATION_BY_LA = 'L_and_A'
CURVE_SPECIFICATION_BY_RA = 'R_and_A'
CURVE_SPECIFICATION_ITEMS = (
	(CURVE_SPECIFICATION_BY_RL, 'R & L', 'Input Clothoid Parameter and Curve Length to determine the clothoid curve.'),
	(CURVE_SPECIFICATION_BY_LA, 'L & A', 'Input Curve Length and Clothoid Parameter to determine the clothoid curve.'),
	(CURVE_SPECIFICATION_BY_RA, 'R & A', 'Input Curve Radius and Clothoid Parameter to determine the clothoid curve.'),
)










def make_curve_specification_props(self, context, col):
	"""クロソイド曲線の指定方法のUIを作成する。クロソイド曲線を作るオペレーターとクロソイド角丸矩形を作るオペレーターで共通。"""

	col.label(text='Curve Specification Method')
	row = col.row(align=True)
	row.prop(self, 'val_elements', expand=True)
	if self.val_elements == CURVE_SPECIFICATION_BY_RL:
		col.prop(self, 'val_curve_radius')
		col.prop(self, 'val_curve_length')
		row = col.row(align=True)
		row.alignment = 'RIGHT'
		A = math.sqrt(self.val_curve_radius * self.val_curve_length)
		row.label(text=f"A: {bpy.app.translations.pgettext_iface('Clothoid Parameter')}: {A:.3f}")
	elif self.val_elements == CURVE_SPECIFICATION_BY_LA:
		row = col.row(align=True)
		row.alignment = 'RIGHT'
		R = self.val_clothoid_param ** 2 / self.val_curve_length
		row.label(text=f"R: {bpy.app.translations.pgettext_iface('Curve Radius')}: {romly_utils.units_to_string(R)}")
		col.prop(self, 'val_curve_length')
		col.prop(self, 'val_clothoid_param')
	else:
		col.prop(self, 'val_curve_radius')
		row = col.row(align=True)
		row.alignment = 'RIGHT'
		row.label(text=f"L: {bpy.app.translations.pgettext_iface('Curve Length')}: {romly_utils.units_to_string(self.val_curve_length)}")
		col.prop(self, 'val_clothoid_param')










# MARK: Class
class ROMLYADDON_OT_add_clothoid_curve(bpy.types.Operator):
	"""クロソイド曲線を作成するオペレーター"""
	bl_idname = 'romlyaddon.add_clothoid_curve'
	bl_label = bpy.app.translations.pgettext_iface('Add Clothoid Curve')
	bl_description = 'Construct a Clothoid Curve'
	bl_options = {'REGISTER', 'UNDO'}

	val_elements: EnumProperty(name='Curve Specification Method', items=CURVE_SPECIFICATION_ITEMS, default=CURVE_SPECIFICATION_BY_RL)
	val_curve_radius: FloatProperty(name='R: ' + bpy.app.translations.pgettext_iface('Curve Radius'), default=1.0, min=0.1, max=100.0, step=10, precision=3, unit='LENGTH')
	val_curve_length: FloatProperty(name='L: ' + bpy.app.translations.pgettext_iface('Curve Length'), default=10.0, min=0.1, soft_max=100.0, step=1, precision=3, unit='LENGTH')
	val_clothoid_param: FloatProperty(name='A: ' + bpy.app.translations.pgettext_iface('Clothoid Parameter'), default=1.0, min=0.1, max=100.0, step=1, precision=3)

	val_num_vertices: IntProperty(name='Curve Vertices', default=64, min=3, soft_max=128, max=1024, step=1)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		make_curve_specification_props(self, context, col)
		col.separator()

		col.prop(self, 'val_num_vertices')



	def execute(self, context):
		if self.val_elements == CURVE_SPECIFICATION_BY_LA:
			# 曲線長とクロソイドパラメータで指定する場合
			self.val_curve_radius = self.val_clothoid_param ** 2 / self.val_curve_length
		elif self.val_elements == CURVE_SPECIFICATION_BY_RA:
			# 曲線半径とクロソイドパラメータで指定する場合
			self.val_curve_length = self.val_clothoid_param ** 2 / self.val_curve_radius
		else:
			# 曲線半径と曲線長で指定する場合
			self.val_clothoid_param = math.sqrt(self.val_curve_radius * self.val_curve_length)

		curve_length = self.val_curve_length
		clothoid_param_A = math.sqrt(self.val_curve_radius * curve_length)

		clothoid_vertices = create_clothoid_curve_vertices(clothoid_param_A=clothoid_param_A, curve_length=curve_length, num_vertices=self.val_num_vertices)
		obj = romly_utils.create_object(clothoid_vertices.vertices,
			name=bpy.app.translations.pgettext_data('Clothoid Curve'),
			edges=[(i, i + 1) for i in range(len(clothoid_vertices.vertices) - 1)])
		bpy.context.collection.objects.link(obj)

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		# オブジェクトの原点を3Dカーソル位置に設定
		obj.location = bpy.context.scene.cursor.location

		return {'FINISHED'}










# MARK: Class
class ROMLYADDON_OT_add_clothoid_corner_plate(bpy.types.Operator):
	"""クロソイド角丸矩形を作成するオペレーター"""
	bl_idname = "romlyaddon.add_clothoid_corner_plate"
	bl_label = bpy.app.translations.pgettext_iface('Add Clothoid Corner Plate')
	bl_description = 'Construct a Clothoid Corner Plate'
	bl_options = {'REGISTER', 'UNDO'}

	val_elements: EnumProperty(name='Curve Specification Method', items=CURVE_SPECIFICATION_ITEMS, default=CURVE_SPECIFICATION_BY_RL)
	val_curve_radius: FloatProperty(name='R: ' + bpy.app.translations.pgettext_iface('Curve Radius'), default=2.0, min=0.1, max=100.0, step=10, precision=3, unit='LENGTH')
	val_curve_length: FloatProperty(name='L: ' + bpy.app.translations.pgettext_iface('Curve Length'), default=3.4, min=0.1, max=100.0, step=10, precision=3, unit='LENGTH')
	val_clothoid_param: FloatProperty(name='A: ' + bpy.app.translations.pgettext_iface('Clothoid Parameter'), default=1.0, min=0.1, max=100.0, step=1, precision=3)

	val_size: FloatVectorProperty(name='Rectangle Size', size=2, default=(2.0, 2.0), unit='LENGTH')
	val_thickness: FloatProperty(name='Thickness', default=0.1, min=0.0, soft_max=10.0, step=1, precision=3, unit='LENGTH')

	val_num_vertices: IntProperty(name='Curve Vertices', default=12, min=2, soft_max=32, max=128, step=1)
	val_num_arc_vertices: IntProperty(name='Arc Vertices', default=16, min=3, soft_max=32, max=128, step=1)
	arc_angle: float = 0
	corner_width: float = 0
	corner_scale: float = 1



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		make_curve_specification_props(self, context, col)

		row = col.row(align=True)
		row.alignment = 'RIGHT'
		row.label(text=f"{bpy.app.translations.pgettext_iface('Angle of Circular Arc')}: {romly_utils.units_to_string(self.arc_angle, category=bpy.utils.units.categories.ROTATION)}")

		c = col.column(align=True)
		c.label(text=f"{bpy.app.translations.pgettext_iface('Total width(height) of rounded corner')}:")
		row = c.row(align=True)
		row.alignment = 'RIGHT'
		if self.corner_scale != 1:
			row.label(text=f"{romly_utils.units_to_string(self.corner_width)} -> {romly_utils.units_to_string(self.corner_width * self.corner_scale)}")
		else:
			row.label(text=f"{romly_utils.units_to_string(self.corner_width)}")
		col.separator()

		row = col.row(align=True)
		row.prop(self, 'val_size')
		col.prop(self, 'val_thickness')
		col.separator()

		col.prop(self, 'val_num_vertices')
		col.prop(self, 'val_num_arc_vertices')



	def execute(self, context):
		if self.val_elements == CURVE_SPECIFICATION_BY_LA:
			# 曲線長とクロソイドパラメータで指定する場合
			self.val_curve_radius = self.val_clothoid_param ** 2 / self.val_curve_length
		elif self.val_elements == CURVE_SPECIFICATION_BY_RA:
			# 曲線半径とクロソイドパラメータで指定する場合
			self.val_curve_length = self.val_clothoid_param ** 2 / self.val_curve_radius
		else:
			# 曲線半径と曲線長で指定する場合
			self.val_clothoid_param = math.sqrt(self.val_curve_radius * self.val_curve_length)

		all_vertices, self.arc_angle, self.corner_width, self.corner_scale = create_clothoid_corner_rectangle(
			clothoid_param_A=self.val_clothoid_param,
			curve_length=self.val_curve_length,
			num_curve_vertices=self.val_num_vertices,
			num_arc_vertices=self.val_num_arc_vertices,
			rectangle_width=self.val_size[0],
			rectangle_height=self.val_size[1])

		# 掃引
		faces = [list(range(len(all_vertices)))]
		if self.val_thickness > 0:
			romly_utils.extrude_face(all_vertices, faces=faces, extrude_vertex_indices=range(len(all_vertices)), z_offset=self.val_thickness)

		obj = romly_utils.create_object(all_vertices, faces=faces, name=bpy.app.translations.pgettext_data('Clothoid Corner Rectangle'))
		obj = romly_utils.cleanup_mesh(obj)
		bpy.context.collection.objects.link(obj)



		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		# オブジェクトの原点を3Dカーソル位置に設定
		obj.location = bpy.context.scene.cursor.location

		return {'FINISHED'}










# MARK: Menu
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_clothoid_curve.bl_idname, text=bpy.app.translations.pgettext_iface('Add Clothoid Curve'), icon='FORCE_VORTEX')
		layout.operator(ROMLYADDON_OT_add_clothoid_corner_plate.bl_idname, text=bpy.app.translations.pgettext_iface('Add Clothoid Corner Plate'), icon='META_PLANE')









# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_clothoid_curve,
	ROMLYADDON_OT_add_clothoid_corner_plate,
	ROMLYADDON_MT_romly_add_mesh_menu_parent,
]





def register():
	# 翻訳辞書の登録
	try:
		bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)
	except ValueError:
		bpy.app.translations.unregister(__name__)
		bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)

	# blenderへのクラス登録処理
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.VIEW3D_MT_add.append(menu_func)





def unregister():
	# クラスの登録解除
	for cls in classes:
		bpy.utils.unregister_class(cls)

	bpy.types.VIEW3D_MT_add.remove(menu_func)

	# 翻訳辞書の登録解除
	bpy.app.translations.unregister(__name__)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()
