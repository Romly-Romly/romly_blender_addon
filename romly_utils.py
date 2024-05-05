import bpy
import bmesh
import mathutils
import math
from mathutils import Vector, Matrix
from typing import Literal, NamedTuple
from collections.abc import Callable



import romly_translation

# romly_translationの再読み込み（Blenderを再起動しなくてもよくなる）
import importlib
importlib.reload(romly_translation)










# メッシュを作成する平面を選択するためのアイテム
ALIGN_PLANE_ITEMS = [
	('xy', 'XY Plane', 'Cunstructs a curve on the XY Plane'),
	('xz', 'XZ Plane', 'Cunstructs a curve on the XZ Plane'),
	('yz', 'YZ Plane', 'Cunstructs a curve on the YZ Plane'),
	('view', 'View Plane', 'Cunstructs a curve on the View Plane'),
]

def set_object_rotation_to_plane(obj: bpy.types.Object, plane: Literal['xy', 'xz', 'yz', 'view']) -> None:
	"""
	指定された平面に沿ってオブジェクトの回転を設定する。オブジェクトをディフォルトでxy平面上に展開されている図形として、指定された平面に展開されるよう回転する。

	Parameters
	----------
	obj : bpy.types.Object
		回転を設定するBlenderのオブジェクト。
	plane : Literal['xy', 'xz', 'yz', 'view']
		オブジェクトを回転させる目的の平面。'xy'なら回転を設定しない。'view'は現在のビュー方向に合わせる。
	"""
	match plane:
		case 'yz':
			obj.rotation_euler = Vector((math.radians(-90), math.radians(180), math.radians(-90)))
		case 'xz':
			obj.rotation_euler[0] = math.radians(90)
		case 'view':
			# 現在のコンテキストからビュー行列を取得
			view_matrix = bpy.context.space_data.region_3d.view_matrix
			# オブジェクトの回転をビュー行列の逆行列に設定
			obj.rotation_euler = view_matrix.to_3x3().normalized().transposed().to_euler()










# MARK: ScrewSpec
class ScrewSpec(NamedTuple):
	"""
	ネジ（またはナット）の寸法を格納するタプル

	Attributes
	----------
	nut_height_thin : float
		3種ナットの厚み
	"""
	diameter: float
	pitch: float
	head_diameter: float
	panhead_height: float
	phillips_size: float
	phillips_depth: float
	flathead_diameter: float
	flathead_edge_thickness: float
	bolthead_across_flats: float	# 六角頭またはナットの二面幅
	bolthead_height: float
	nut_height: float	# ナットの厚み（高さ）
	nut_height_thin: float	# 3種ナットの厚み

	def bolthead_diameter(self) -> float:
		"""六角頭またはナットの対角距離を返す。"""
		return self.bolthead_across_flats / math.cos(math.radians(30))

	def thread_depth(self) -> float:
		"""
		ねじ山の高さをピッチから算出する。

		Returns
		-------
		float
			ねじ山の高さ(mm)。
		"""
		return self.pitch * 0.866025 * 2










# M2〜M8のネジの寸法
SCREW_SPECS = {
	'm2': ScrewSpec(diameter=2, pitch=0.4, head_diameter=3.5, panhead_height=1.3, phillips_size=2.2, phillips_depth=1.01, flathead_diameter=4.0, flathead_edge_thickness=0.2, bolthead_across_flats=4, bolthead_height=1.3, nut_height=1.6, nut_height_thin=1.2),
	'm2_5': ScrewSpec(diameter=2.5, pitch=0.45, head_diameter=4.5, panhead_height=1.7, phillips_size=2.6, phillips_depth=1.42, flathead_diameter=5, flathead_edge_thickness=0.2, bolthead_across_flats=5, bolthead_height=1.7, nut_height=2.0, nut_height_thin=1.6),
	'm3': ScrewSpec(diameter=3, pitch=0.5, head_diameter=5.5, panhead_height=2.0, phillips_size=3.6, phillips_depth=1.43, flathead_diameter=6, flathead_edge_thickness=0.25, bolthead_across_flats=5.5, bolthead_height=2.0, nut_height=2.4, nut_height_thin=1.8),
	'm4': ScrewSpec(diameter=4, pitch=0.7, head_diameter=7.0, panhead_height=2.6, phillips_size=4.2, phillips_depth=2.03, flathead_diameter=8, flathead_edge_thickness=0.3, bolthead_across_flats=7, bolthead_height=2.8, nut_height=3.2, nut_height_thin=2.4),
	'm5': ScrewSpec(diameter=5, pitch=0.8, head_diameter=9.0, panhead_height=3.3, phillips_size=4.9, phillips_depth=2.73, flathead_diameter=10, flathead_edge_thickness=0.3, bolthead_across_flats=8, bolthead_height=3.5, nut_height=4.0, nut_height_thin=3.2),
	'm6': ScrewSpec(diameter=6, pitch=1.0, head_diameter=10.5, panhead_height=3.9, phillips_size=6.3, phillips_depth=2.86, flathead_diameter=12, flathead_edge_thickness=0.4, bolthead_across_flats=10, bolthead_height=4.0, nut_height=5.0, nut_height_thin=3.6),
	'm8': ScrewSpec(diameter=8, pitch=1.25, head_diameter=14.0, panhead_height=5.2, phillips_size=7.8, phillips_depth=4.36, flathead_diameter=16, flathead_edge_thickness=0.4, bolthead_across_flats=13, bolthead_height=5.5, nut_height=6.5, nut_height_thin=5.0),
}










def VECTOR_ZERO():
	"""ゼロベクトルを返す。

	Returns
	-------
	mathutils.Vector
		Blenderにおけるゼロベクトル。
	"""
	return mathutils.Vector([0, 0, 0])





def VECTOR_Y_PLUS():
	"""Yプラス方向の単位ベクトルを返す。

	Returns
	-------
	mathutils.Vector
		BlenderにおけるYプラス方向の単位ベクトル。
	"""
	return mathutils.Vector([0, 1, 0])










def make_arc_vertices(start, center, axis, rotate_degrees: float, segments) -> list[Vector]:
	"""任意の座標を中心とした円または円弧を作る頂点のリストを返す。

	Parameters
	----------
	start : Vertex
		円弧の開始座標
	center : Vertex
		円の中心。円の半径はstartとの差となる。
	axis : ['X', 'Y', 'Z']
	rotate_degrees : float
		[description]
	segments : int
		頂点の数。2以上を指定。
	Returns
	-------
	list[Vertex]
		[description]
	"""
	vertices = []

	for i in range(segments + 1):
		v = rotated_vector(vector=start - center, angle_radians=math.radians(rotate_degrees / segments * i), axis=axis)
		v += center
		vertices.append(v)

	return vertices










def create_object(vertices: list[tuple[float, float, float]], faces: list = [], name: str = '', mesh_name: str = None, edges: list[tuple[int, int]] = []) -> bpy.types.Object:
	"""
	指定された頂点リストと面リストから新しいオブジェクトを生成する。

	Parameters
	----------
	vertices : list[tuple[float, float, float]]
		オブジェクトの頂点座標のリスト。
	faces : list of tuple of int, optional
		オブジェクトの面を構成する頂点のインデックスのリスト。省略すると面は作成されない。
	name : str
		作成されるオブジェクトの名前。
	mesh_name : str, optional
		作成されるメッシュデータの名前。省略した場合、オブジェクト名に '_mesh' を追加されたものになる。
	edges : list[tuple[int, int]], optional
		オブジェクトのエッジを構成する頂点のインデックスのリスト。デフォルトでは辺は作成されない。

	Returns
	-------
	bpy.types.Object
		作成されたオブジェクトのインスタンス。
	"""
	if mesh_name is None:
		mesh_name = name + '_mesh'
	mesh = bpy.data.meshes.new(mesh_name)
	mesh.from_pydata(vertices, edges, faces)
	obj = bpy.data.objects.new(name, mesh)
	return obj





def create_combined_object(objects: list[bpy.types.Object], obj_name: str, mesh_name: str = None) -> bpy.types.Object:
	"""
	複数のオブジェクトを統合して一つのオブジェクトにまとめる。

	Parameters
	----------
	objects : list[bpy.types.Object]
		結合するオブジェクトのリスト。先頭のオブジェクトの位置が維持される。
	obj_name : str
		生成するメッシュにつける名前。
	mesh_name : str
		生成するメッシュにつける名前。
	"""

	# 結合するオブジェクトが1つだけの場合はそのまま返す。ただし名前は変更する。
	if len(objects) == 1:
		objects[0].name = obj_name
		return objects[0]

	vertices = []
	faces = []
	vertex_index_offset = 0
	for obj in objects:
		for v in obj.data.vertices:
			vertices.append(obj.location + v.co - objects[0].location)
		for f in obj.data.polygons:
			faces.append([])
			for v in f.vertices:
				faces[len(faces) - 1].append(v + vertex_index_offset)
		vertex_index_offset += len(obj.data.vertices)

	if mesh_name is None:
		mesh_name = obj_name + '_mesh'
	mesh = bpy.data.meshes.new(mesh_name)
	mesh.from_pydata(vertices, [], faces)

	combined_obj = bpy.data.objects.new(obj_name, mesh)
	combined_obj.location = objects[0].location
	return combined_obj










def create_box(size: Vector, offset: Vector = Vector((0, 0, 0))) -> bpy.types.Object:
	"""
	直方体のオブジェクトを生成する。

	Parameters
	----------
	size : Vector
		直方体の各軸の大きさを表すベクトル。(1.0, 1.0, 1.0)なら大きさ1の立方体を作る。
	offset : Vector, optional
		直方体の中心からのオフセットを表すベクトル。直方体の位置を決める。

	Returns
	-------
	bpy.types.Object
		作成されたオブジェクト。Blenderのシーンには既にリンクされた状態。
	"""
	vertices = [
		mathutils.Vector([-0.5, -0.5, -0.5]),	# 0 正面 左下
		mathutils.Vector([-0.5, -0.5, 0.5]),	# 1 正面 左上
		mathutils.Vector([-0.5, 0.5, -0.5]),	# 2 奥 左下
		mathutils.Vector([-0.5, 0.5, 0.5]),		# 3 奥 左上
		mathutils.Vector([0.5, -0.5, -0.5]),	# 4 正面 右下
		mathutils.Vector([0.5, -0.5, 0.5]),		# 5 正面 右上
		mathutils.Vector([0.5, 0.5, -0.5]),		# 6 奥 右下
		mathutils.Vector([0.5, 0.5, 0.5])		# 7 奥 右上
	]
	faces = [
		(1, 5, 4, 0),	# 正面
		(3, 7, 6, 2),	# 背面
		(1, 3, 2, 0),	# 左側面
		(5, 7, 6, 4),	# 右側面
		(0, 4, 6, 2),	# 底面
		(1, 5, 7, 3),	# 上面
	]

	actual_vertices = [(v * size) + offset for v in vertices]
	obj = cleanup_mesh(create_object(vertices=actual_vertices, faces=faces))
	bpy.context.collection.objects.link(obj)
	return obj










def create_box_from_corners(corner1: tuple[float, float, float], corner2: tuple[float, float, float]) -> bpy.types.Object:
	"""
	corner1、corner2を対角座標とする直方体を生成する。

	Parameters
	----------
	corner1 : tuple[float, float, float]
		直方体の1つ目の角の座標(x, y, z)。
	corner2 : tuple[float, float, float]
		corner1の対角位置の座標(x, y, z)。

	Returns
	-------
	bpy.types.Object
	"""
	# 座標を小さい順と大きい順で整理
	min_c = [min(corner1[i], corner2[i]) for i in range(3)]
	max_c = [max(corner1[i], corner2[i]) for i in range(3)]

	# メッシュデータの作成
	mesh = bpy.data.meshes.new('BoxMesh')
	bm = bmesh.new()

	# 頂点を追加
	verts = [
		bm.verts.new((min_c[0], min_c[1], min_c[2])),
		bm.verts.new((max_c[0], min_c[1], min_c[2])),
		bm.verts.new((max_c[0], max_c[1], min_c[2])),
		bm.verts.new((min_c[0], max_c[1], min_c[2])),
		bm.verts.new((min_c[0], min_c[1], max_c[2])),
		bm.verts.new((max_c[0], min_c[1], max_c[2])),
		bm.verts.new((max_c[0], max_c[1], max_c[2])),
		bm.verts.new((min_c[0], max_c[1], max_c[2])),
	]

	# 面を作成
	faces = [
		(0, 1, 5, 4),  # 下面
		(1, 2, 6, 5),  # 側面1
		(2, 3, 7, 6),  # 上面
		(3, 0, 4, 7),  # 側面2
		(0, 3, 2, 1),  # 前面
		(4, 5, 6, 7)   # 背面
	]

	for face in faces:
		bm.faces.new([verts[i] for i in face])

	# メッシュデータをオブジェクトに変換
	bm.to_mesh(mesh)
	bm.free()

	# オブジェクトを作成し、メッシュを割り当てる
	box_object = bpy.data.objects.new('BoxObject', mesh)

	# シーンにオブジェクトを追加
	bpy.context.collection.objects.link(box_object)

	return box_object










# MARK: create_cylinder
def create_cylinder(radius: float, length_z_plus: float, length_z_minus: float = 0, segments: int = 32) -> bpy.types.Object:
	"""
	円柱のオブジェクトを生成する。生成される円柱の長さは `length_z_plus` + `length_z_minus` となる。

	Parameters
	----------
	radius : float
		円柱の半径。
	length_z_plus : float
		Z軸プラス方向に伸びる円柱の長さ。
	length_z_minus : float, optional
		Z軸マイナス方向に伸びる円柱の長さ（デフォルトは0）。
	segments : int, optional
		円柱のセグメントの数。ディフォルトは32。

	Returns
	-------
	bpy.types.Object
		生成された円柱のオブジェクト。Blenderのシーンには既にリンクされた状態。
	"""
	vertices = make_circle_vertices(radius=radius, num_vertices=segments, center=(0, 0, -length_z_minus))
	faces = [list(range(len(vertices)))]
	extrude_face(vertices, faces=faces, extrude_vertex_indices=list(range(len(vertices))), z_offset=length_z_plus + length_z_minus)
	cylinder = create_object(vertices=vertices, faces=faces)
	cylinder = cleanup_mesh(cylinder)
	bpy.context.collection.objects.link(cylinder)
	return cylinder










# MARK: create_threaded_cylinder
def create_threaded_cylinder(diameter: float, length: float, pitch: float, lead: int, thread_depth: float, segments: int, bevel_segments: int, edge_flat: bool = False) -> bpy.types.Object:
	"""
	ねじ切りの入った円柱を生成する。

	Parameters
	----------
	diameter : float
		円柱の直径。
	length : float
		円柱の長さ。
	pitch : float
		ねじ山のピッチ（隣接するねじ山の谷の中心間の距離）。
	lead : int
		ねじのリード（一回のねじ山で進む距離）。ピッチの倍数で指定。
	thread_depth : float
		ねじ山の深さ。
	segments : int
		円柱の周りのセグメント数。
	bevel_segments : int
		ねじ山の先端のセグメント数。
	edge_flat : bool, optional
		Trueの場合、上下をまっすぐにカットする。

	Returns
	-------
	bpy.types.Object
		作成されたねじ山付き円柱のオブジェクト。位置は原点からZマイナス方向に配置される。オブジェクトはシーンにリンクされている。
	"""
	# 谷径、山と谷のベベルの半径を決める
	minor_diameter = diameter - thread_depth
	major_radius = diameter / 2
	minor_radius = minor_diameter / 2

	vertices = []
	faces = []

	# --------------------------------------------------------------------------------

	# 蓋のエッジになる頂点のインデックスを保存しておく
	lid_edge_vertex_index = 0

	# bevelSegmentsが0より大きい場合はネジの山と谷にベベルを作る
	if bevel_segments > 0:
		H = major_radius - minor_radius

		z = (lead * pitch) - pitch
		for i in range(lead):
			temp_vertices = []
			rh = math.tan(math.radians(30)) * (H / 4)
			start_point = mathutils.Vector([-minor_radius - H / 4, 0, z + pitch - rh])
			end_point = mathutils.Vector([start_point.x, 0, z + pitch + rh])
			temp_vertices.append(start_point)

			pt = start_point.copy()
			da = 120 / (bevel_segments + 1)
			angle = 30 + da
			dz = abs(end_point.z - start_point.z) / bevel_segments
			for i in range(bevel_segments - 1):
				dx = dz / math.tan(math.radians(angle))
				pt.x += dx if (i < bevel_segments) else -dx
				pt.z += dz
				temp_vertices.append(mathutils.Vector([pt.x, pt.y, pt.z]))
				angle += da

			temp_vertices.append(end_point)

			for i in reversed(range(len(temp_vertices))):
				vertices.append(temp_vertices[i])

			# --------------------------------------------------------------------------------

			# 山の頂点と麓2箇所からなす角を求める
			base1 = mathutils.Vector([-minor_radius, 0, z + pitch])
			peak = mathutils.Vector([-major_radius, 0, z + pitch / 2])
			base2 = mathutils.Vector([-minor_radius, 0, z])
			angle = calc_angle(peak=peak, point1=base1, point2=base2)

			# アールの開始座標
			rh = math.tan(angle / 2) * (H / 8)
			bevel_start = mathutils.Vector([-major_radius + H / 8, 0, z + pitch / 2 + rh])

			# アールの開始位置から適当に伸ばした垂線
			perpendicular_point = rotated_vector(vector=peak - bevel_start, angle_radians=math.radians(-90), axis='Y')
			perpendicular_point += bevel_start

			# アール（ベベル）の中心を求める
			bevel_center = find_intersection(
				line1_start=project_to_xz(bevel_start), line1_end=project_to_xz(perpendicular_point),
				line2_start=project_to_xz(peak), line2_end=Vector((0, 0, z + pitch / 2)))

			# 円弧を構成する頂点郡を返す
			vertices.extend(make_arc_vertices(start=bevel_start, center=bevel_center, axis='Y', rotate_degrees=-(90 - math.degrees(angle) / 2) * 2, segments=bevel_segments))

			# ----------------------------------------------------------------------

			rh = math.tan(math.radians(30)) * (H / 4)
			v = mathutils.Vector([-minor_radius - H / 4, 0, z + rh])
			vertices.append(v)

			z -= pitch

	else:
		# 山と谷のベベルのセグメントが0の場合は鋭利な山と谷になる
		vertices.append(mathutils.Vector([0, 0, lead * pitch]))
		z = (lead * pitch) - pitch
		for i in range(lead):
			vertices.append(mathutils.Vector([-minor_radius, 0, z + pitch]))
			vertices.append(mathutils.Vector([-major_radius, 0, z + pitch / 2]))
			vertices.append(mathutils.Vector([-minor_radius, 0, z]))
			z -= pitch
		vertices.append(mathutils.Vector([0, 0, 0]))

	# 回転体の頂点数を取得しておく
	revolution_vertex_count = len(vertices)

	# ----------------------------------------------------------------------

	# 回してスクリューを作る
	pitch_iteration = math.ceil(length / (lead * pitch)) + 2
	for _ in range(pitch_iteration):
		add_revolved_surface(vertices=vertices, faces=faces, rotation_vertex_count=revolution_vertex_count, segments=segments, z_offset=-lead * pitch)

	# ----------------------------------------------------------------------

	num_last_vertex_index_ecluding_lid_and_bottom = len(vertices) - 1
	bottomZ = vertices[-1].z

	# 蓋を作る
	vertices.append(mathutils.Vector([0, 0, vertices[lid_edge_vertex_index].z]))
	lid_center_vertex_index = len(vertices) - 1
	for i in range(segments):
		faces.append([lid_center_vertex_index, lid_edge_vertex_index + revolution_vertex_count * i, lid_edge_vertex_index + 	revolution_vertex_count * i + revolution_vertex_count])

	# 最初の回転体の側面兼蓋となる面を作る
	lid_face = []
	lid_face.extend(range(0, revolution_vertex_count))
	lid_face.append(lid_center_vertex_index)
	faces.append(lid_face)

	vertices.append(mathutils.Vector([0, 0, bottomZ]))
	bottom_center_vertex_index = len(vertices) - 1
	for i in range(segments):
		faces.append([bottom_center_vertex_index,
			num_last_vertex_index_ecluding_lid_and_bottom - revolution_vertex_count * i,
			num_last_vertex_index_ecluding_lid_and_bottom - revolution_vertex_count * (i + 1)])

	# 最後の回転体の側面兼底となる面を作る
	bottom_face = []
	bottom_face.extend(range(num_last_vertex_index_ecluding_lid_and_bottom - revolution_vertex_count + 1, num_last_vertex_index_ecluding_lid_and_bottom + 1))
	bottom_face.append(bottom_center_vertex_index)
	faces.append(bottom_face)

	# ----------------------------------------------------------------------

	obj = cleanup_mesh(object=create_object(vertices=vertices, faces=faces, name='screw'))
	bpy.context.collection.objects.link(obj)

	# 上下のカット
	if edge_flat:
		cutter = create_box(size=Vector((diameter * 2, diameter * 2, length)), offset=Vector((0, 0, -length - length / 2)))
		apply_boolean_object(obj, cutter)
		cutter = create_box(size=Vector((diameter * 2, diameter * 2, length)), offset=Vector((0, 0, length / 2)))
		apply_boolean_object(obj, cutter)

	return obj










def create_empty_object() -> bpy.types.Object:
	"""
	頂点を持たない空のオブジェクトを生成する。

	Returns
	-------
	bpy.types.Object
		生成されたオブジェクト。Blenderのシーンには既にリンクされた状態。
	"""
	empty = create_object(vertices=[], faces=[])
	bpy.context.collection.objects.link(empty)
	return empty










def cleanup_mesh(object: bpy.types.Object, remove_doubles=True, recalc_normals=True) -> bpy.types.Object:
	"""
	メッシュオブジェクトの重複する頂点を削除し、法線を再計算することでメッシュをクリーンアップする。

	Parameters
	----------
	object : bpy.types.Object
		クリーンアップするメッシュオブジェクト
	remove_doubles : bool, optional
		True の場合、重複する頂点を削除します。デフォルトは True。
	recalc_normals : bool, optional
		True の場合、法線を再計算します。デフォルトは True。

	Returns
	-------
	bpy.types.Object
	"""
	bm = bmesh.new()
	bm.from_mesh(object.data)
	if remove_doubles:
		bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
	if recalc_normals:
		bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
	bm.to_mesh(object.data)
	bm.clear()
	object.data.update()
	bm.free()
	return object





def translate_vertices(object, vector):
	"""
	オブジェクト（またはオブジェクトのリスト）の頂点を移動する。

	Parameters
	----------
	object : bpy.types.Mesh, bpy.types.Object, または list
		頂点を移動するオブジェクト、またはオブジェクトのリスト。
	vector : mathutils.Vector
		移動量を指定するベクトル。

	Raises
	------
	TypeError
		与えられたオブジェクトが bpy.types.Mesh, bpy.types.Object, または list のいずれでもない場合。
	"""
	if isinstance(object, bpy.types.Mesh) or isinstance(object, bpy.types.Object):
		bm = bmesh.new()
		bm.from_mesh(object.data)
		bmesh.ops.translate(bm, vec=vector, verts=bm.verts)
		bm.to_mesh(object.data)
		bm.clear()
		object.data.update()
		bm.free()
	elif isinstance(object, list):
		for i in range(len(object)):
			object[i] = object[i] + vector










def add_revolved_surface(vertices: list[Vector], faces: list[list[int]], rotation_vertex_count: int, segments: int, close=False, z_offset: float = 0) -> None:
	"""
	頂点群で表される面を360度回転させて回転体を作る。

	Parameters
	----------
	vertices : list[Vector]
		頂点リスト。回転させる頂点も含む。新しく作った頂点もここに追加される。
	faces : list[list[int]]
		面のインデックスリスト。新しい面の追加用で、読み取りはされない。
	rotation_vertex_count : int
		回転させる頂点の数。この数だけの頂点が回転軸周りで回転される。
	segments : int
		回転体を構成するセグメントの数。360度をこの数で割った角度で頂点が回転される。
	close : bool, optional
		回転体の両端を閉じるかどうか。Trueの場合、端の面が作成される。
	z_offset : float, optional
		頂点のZ座標に加算されるオフセット。このオフセットは全セグメントに渡って線形に加算される。ねじ切りはこの値を使うことで軸方向にずらしている。

	Notes
	-----
	この関数は`vertices`と`faces`を直接変更します。メッシュデータは呼び出し元で管理する必要があります。
	"""
	rot = mathutils.Matrix.Rotation(-math.radians(360.0 / segments), 4, 'Z')
	for i in range(segments):
		temp_vertices = []
		for j in range(rotation_vertex_count):
			v = vertices[len(vertices) - rotation_vertex_count + j].copy()
			v.z += z_offset / segments
			v.rotate(rot)
			temp_vertices.append(v)
		for j in range(len(temp_vertices)):
			vertices.append(temp_vertices[j])

		# 面を貼る
		n = len(vertices)
		for j in range(rotation_vertex_count - 1):
			faces.append([
				n - rotation_vertex_count * 2 + j,
				n - rotation_vertex_count * 2 + 1 + j,
				n - rotation_vertex_count + 1 + j,
				n - rotation_vertex_count + j])
		if close:
			faces.append([
				n - rotation_vertex_count * 2 + rotation_vertex_count - 1,
				n - rotation_vertex_count * 2,
				n - rotation_vertex_count,
				n - rotation_vertex_count + rotation_vertex_count - 1])










def cleanup_mesh(object: bpy.types.Object, remove_doubles=True, recalc_normals=True):
	"""
	メッシュオブジェクトの重複する頂点を削除し、法線を再計算することでメッシュをクリーンアップする。

	Parameters
	----------
	object : bpy.types.Object
		クリーンアップするメッシュオブジェクト
	remove_doubles : bool, optional
		True の場合、重複する頂点を削除します。デフォルトは True。
	recalc_normals : bool, optional
		True の場合、法線を再計算します。デフォルトは True。

	Returns
	-------
	bpy.types.Object
	"""
	bm = bmesh.new()
	bm.from_mesh(object.data)
	if remove_doubles:
		bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
	if recalc_normals:
		bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
	bm.to_mesh(object.data)
	bm.clear()
	object.data.update()
	bm.free()
	return object










def extrude_face(vertices: list[Vector | tuple[float, float, float]], faces: list[list[int]], extrude_vertex_indices: list[int], z_offset: float = 1, offset: Vector = None, cap=True):
	"""
	指定された面を掃引して、新しくできた頂点と面を追加する。

	Parameters
	----------
	vertices : list[Vector | tuple[float, float, float]]
		頂点のリスト
	faces : list[list[int]]
		面を構成する頂点インデックスのリスト
	extrude_vertex_indices : list[int]
		掃引する頂点のインデックスのリスト。頂点(Vector)のリストじゃないので注意してね。
	z_offset : float
		掃引する距離
	cap : bool, optional
		掃引したすべての頂点を結ぶ面を作るか。つまり、面をキャップ（閉じる）するかどうか。
	"""
	# 各頂点を掃引した位置に複製する
	for i in extrude_vertex_indices:
		if isinstance(vertices[i], Vector):
			v = vertices[i].copy()
		else:
			v = Vector((vertices[i][0], vertices[i][1], vertices[i][2]))
		if offset:
			v += offset
		else:
			v.z += z_offset
		vertices.append(v)

	l = len(vertices)
	numExtrudeFaceVertices = len(extrude_vertex_indices)
	for i in range(numExtrudeFaceVertices):
		if i == numExtrudeFaceVertices - 1:
			faces.append([
				extrude_vertex_indices[i],
				extrude_vertex_indices[0],
				l - numExtrudeFaceVertices,
				l - numExtrudeFaceVertices + i])
		else:
			faces.append([
				extrude_vertex_indices[i],
				extrude_vertex_indices[i + 1],
				l - numExtrudeFaceVertices + i + 1,
				l - numExtrudeFaceVertices + i])

	if cap:
		faces.append(list(reversed(range(l - numExtrudeFaceVertices, l))))










def remove_decimal_trailing_zeros(value: float) -> str:
	"""数値を文字列に変換し、小数点以下の右端に0があれば削除する。"""
	s = f'{value:.3f}'
	if '.' in s:
		s = s.rstrip('0')
		if s[-1] == '.':
			s = s[0:-1]
	return s










def units_to_string(value, category=bpy.utils.units.categories.LENGTH, removeSpace=False):
	"""
	Blender内の単位を文字列に変換する。

	Parameters
	----------
	value : float
		変換する単位の値。
	category : str, optional
		変換する単位のカテログリ。bpy.utils.units.categoriesの定数。デフォルトは 'LENGTH'。
	removeSpace : bool, optional
		結果の文字列からスペースを削除するかどうか。デフォルトはFalse。

	Returns
	-------
	str
		変換された単位の文字列。

	Examples
	--------
	>>> units_to_string(2)
	'2 m'
	>>> units_to_string(2, True)
	'2m'
	"""
	if category == bpy.utils.units.categories.LENGTH:
		s = bpy.utils.units.to_string(unit_system=bpy.context.scene.unit_settings.system, unit_category=category, value=value * bpy.context.scene.unit_settings.scale_length)
	else:
		s = bpy.utils.units.to_string(unit_system=bpy.context.scene.unit_settings.system, unit_category=category, value=value)

	# スペースの削除
	if removeSpace:
		s = s.replace(' ', '')

	return s





def rotated_vector(vector: Vector, angle_radians: float, axis: Literal['X', 'Y', 'Z']) -> Vector:
	"""原点周りで回転したベクトルを生成して返す。

	Parameters
	----------
	vector : Vector
		元になるベクトル。
	angle_radians : float
		ラジアン単位の回転角度。
	axis : Literal['X', 'Y', 'Z']
		回転軸。Matrix.Rotationメソッドにそのまま渡される。

	Returns
	-------
	Vector
		回転したベクトル。新しいベクトルが生成されて返される。
	"""
	v = vector.copy()
	v.rotate(mathutils.Matrix.Rotation(angle_radians, 4, axis))
	return v





def rotate_vertices(object: bpy.types.Mesh | list[Vector], degrees: float, axis: Literal['X', 'Y', 'Z']):
	"""MeshまたはVectorの配列のすべての頂点を原点周りで回転する

	Parameters
	----------
	object : bpy.types.Mesh | list[Vector]
		回転する頂点を含むMeshオブジェクトか、Vectorの配列。
	axis : Literal['X', 'Y', 'Z']
		回転軸。Matrix.Rotationメソッドにそのまま渡される。

	"""
	if isinstance(object, bpy.types.Mesh) or isinstance(object, bpy.types.Object):
		bm = bmesh.new()
		bm.from_mesh(object.data)
		bmesh.ops.rotate(bm, verts=bm.verts, cent=(0.0, 0.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(degrees), 4, axis))
		bm.to_mesh(object.data)
		bm.clear()
		object.data.update()
		bm.free()
	elif isinstance(object, list):
		for i in range(len(object)):
			v = object[i]
			if isinstance(v, mathutils.Vector):
				v.rotate(mathutils.Matrix.Rotation(math.radians(degrees), 4, axis))
				object[i] = v
			else:
				vec = Vector(v)
				vec.rotate(mathutils.Matrix.Rotation(math.radians(degrees), 4, axis))
				object[i] = vec.to_tuple()










def project_to_xy(v: Vector) -> Vector:
	"""ベクトルのZ成分を0にしてXY平面に投影する。"""
	return Vector((v.x, v.y, 0))










def project_to_xz(v: Vector) -> Vector:
	"""ベクトルのY成分を0にしてXZ平面に投影する。"""
	return Vector((v.x, 0, v.z))










def calc_angle(peak: Vector, point1: Vector, point2: Vector) -> float:
	"""peakからpoint1へのベクトルと、peakからpoint2へのベクトルのなす角度を計算する。"""
	v1 = point1 - peak
	v2 = point2 - peak
	return math.acos(v1.dot(v2) / (v1.magnitude * v2.magnitude))










def apply_boolean_object(object, boolObject, operation='DIFFERENCE', use_self=False, unlink=True, apply=True, fast_solver=False):
	"""
	ブーリアンモデファイア(Difference)を使ってメッシュをもう一方のメッシュの形状で削る。

	Parameters
	----------
	object : Mesh
		元となるメッシュ。
	boolObject : Mesh
		ブーリアンモデファイアに設定されるメッシュ。シーンにリンクされていないとエラーになる。
	unlink : Bool
		処理後にboolObjectをシーンからアンリンクするか。
	apply : Bool, optional
		ブーリアンモデファイアを適用するかどうか。デフォルトはTrue。
	"""
	bpy.context.view_layer.objects.active = object
	mod = bpy.context.object.modifiers.new(type='BOOLEAN', name='Boolean')
	mod.operation = operation
	mod.object = boolObject
	mod.use_self = use_self
	if fast_solver:
		mod.solver = 'FAST'
	if apply:
		bpy.ops.object.modifier_apply(modifier=mod.name)
	if unlink:
		bpy.context.collection.objects.unlink(boolObject)










def apply_bevel_modifier(obj: bpy.types.Object, width: float) -> None:
	bevel_modifier = obj.modifiers.new(name='Bevel', type='BEVEL')
	bevel_modifier.offset_type = 'OFFSET'
	bevel_modifier.use_clamp_overlap = True
	bevel_modifier.limit_method = 'WEIGHT'
	bevel_modifier.width = width
	bevel_modifier.segments = 1
	bevel_modifier.profile = 0.5
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=bevel_modifier.name)










def apply_bevel_modifier_to_edges(obj: bpy.types.Object, width: float, edge_select_func: Callable[[bmesh.types.BMEdge], bool]) -> None:
	select_edges_by_condition(obj, lambda edge: edge_select_func(edge))
	set_bevel_weight(obj)

	# ベベルモディファイアを追加、適用
	apply_bevel_modifier(obj, width)










def calc_linked_face_dot(edge: bmesh.types.BMEdge) -> float | None:
	"""
	辺を共有する2つの面の法線の内積を計算する。辺に対する面が2つでなかった場合はNoneを返す。

	Parameters
	----------
	edge : bmesh.types.BMEdge
		内積を計算する辺。

	Returns
	-------
	float
		法線の内積。
	"""
	linked_faces = edge.link_faces
	if len(linked_faces) == 2:
		# 両面の法線を取得
		n1 = linked_faces[0].normal
		n2 = linked_faces[1].normal

		# 法線の内積を計算
		return n1.dot(n2)
	else:
		return None










def select_edges_on_fair_surface(obj: bpy.types.Object, threshold_degree: float = 0) -> None:
	"""
	平面上にある辺（隣接する面の法線が同じ辺）を選択します。

	Parameters
	----------
	obj : bpy.types.Object
		法線を比較して辺を選択する対象のBlenderオブジェクト。
	"""
	bpy.ops.mesh.select_mode(type='EDGE')
	bm = bmesh.from_edit_mesh(obj.data)

	# まず選択を解除
	bpy.ops.mesh.select_all(action='DESELECT')

	# 閾値値の角度を内積の値に変換
	threshold_radian = math.radians(threshold_degree)
	cos_value = math.cos(threshold_radian)

	for edge in bm.edges:
		dot = calc_linked_face_dot(edge)
		if dot is not None and dot >= cos_value:
			edge.select = True

	# 更新を反映
	bmesh.update_edit_mesh(obj.data)










def select_edges_along_axis(obj: bpy.types.Object, axis: tuple[bool, bool, bool], threshold_degree: float = 0) -> None:
	"""
	軸に沿った辺（指定の軸との内積が0）を選択します。

	Parameters
	----------
	obj : bpy.types.Object
		法線を比較して辺を選択する対象のBlenderオブジェクト。
	axis : tuple[bool, bool, bool]
		軸を指定するタプル(X, Y, Z)。同時に複数の軸を指定可。
	"""
	bpy.ops.mesh.select_mode(type='EDGE')
	bm = bmesh.from_edit_mesh(obj.data)

	# まず選択を解除
	bpy.ops.mesh.select_all(action='DESELECT')

	# 閾値値の角度を内積の値に変換
	threshold_radian = math.radians(threshold_degree)
	cos_value = math.cos(threshold_radian)

	VECTORS = [Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))]
	for edge in bm.edges:
		edge_vector = (edge.verts[1].co - edge.verts[0].co).normalized()

		for i in range(3):
			if axis[i]:
				dot_abs = abs(edge_vector.dot(VECTORS[i]))
				if dot_abs >= cos_value:
					edge.select = True

	# 更新を反映
	bmesh.update_edit_mesh(obj.data)










# MARK: clear_bevel_weight
def clear_bevel_weight(obj: bpy.types.Object) -> None:
	"""
	指定されたオブジェクトのすべての辺の Bevel Weight を 0 に設定する。

	Parameters
	----------
	obj : bpy.types.Object
		_description_
	"""
	select_edges_by_condition(obj, lambda edge: True)
	set_bevel_weight(obj, bevel_weight=0.0)










def clear_verts_bevel_weight(obj: bpy.types.Object) -> None:
	"""
	指定されたオブジェクトのすべての頂点の Bevel Weight を 0 に設定する。

	Parameters
	----------
	obj : bpy.types.Object
		_description_
	"""
	select_verts_by_condition(obj, lambda vert: True)
	set_verts_bevel_weight(obj, bevel_weight=0.0)










def set_bevel_weight(obj: bpy.types.Object, bevel_weight: float = 1.0) -> None:
	"""
	アクティブオブジェクトを対象に、選択されている辺に Bevel Weight を設定する。
	オブジェクトモードじゃないと使えないので注意。

	Parameters
	----------
	bevel_weight : float, optional
		設定するベベルウェイトの値。省略した場合は1.0。
	"""
	bm = bmesh.new()
	bm.from_mesh(obj.data)

	# Bevel Weightのレイヤーを取得（存在しない場合は新しく作成）
	KEY = 'bevel_weight_edge'
	bevel_layer = bm.edges.layers.float.get(KEY, bm.edges.layers.float.new(KEY))
	for edge in bm.edges:
		if edge.select:
			edge[bevel_layer] = bevel_weight

	# 更新
	bm.to_mesh(obj.data)
	bm.free()

	# これも忘れないように実行しないと即時反映されない
	obj.data.update()










def set_verts_bevel_weight(obj: bpy.types.Object, bevel_weight: float = 1.0) -> None:
	"""
	アクティブオブジェクトを対象に、選択されている頂点に Bevel Weight を設定する。
	オブジェクトモードじゃないと使えないので注意。

	Parameters
	----------
	bevel_weight : float, optional
		設定するベベルウェイトの値。省略した場合は1.0。
	"""
	bm = bmesh.new()
	bm.from_mesh(obj.data)

	# Bevel Weightのレイヤーを取得（存在しない場合は新しく作成）
	KEY = 'bevel_weight_vert'
	bevel_layer = bm.verts.layers.float.get(KEY, bm.verts.layers.float.new(KEY))
	for vert in bm.verts:
		if vert.select:
			vert[bevel_layer] = bevel_weight

	# 更新
	bm.to_mesh(obj.data)
	bm.free()

	# これも忘れないように実行しないと即時反映されない
	obj.data.update()










def select_edges_by_condition(obj: bpy.types.Object, condition_func: Callable[[bmesh.types.BMEdge], bool]) -> None:
	"""
	指定された条件に合った全ての辺を選択する。

	Parameters
	----------
	condition_func : Callable[[bmesh.types.BMEdge], bool]
		選択の条件となるboolを返す関数。
	"""
	bm = bmesh.new()
	bm.from_mesh(obj.data)
	bm.select_flush(True)
	for edge in bm.edges:
		edge.select = condition_func(edge)

	# これがキモで呼ばないと選択状態が変わらない
	bm.select_flush(False)

	# 更新
	bm.to_mesh(obj.data)
	bm.free()










def select_verts_by_condition(obj: bpy.types.Object, condition_func: Callable[[bmesh.types.BMVert], bool]) -> None:
	"""
	指定された条件に合った全ての頂点を選択する。

	Parameters
	----------
	condition_func : Callable[[bmesh.types.BMVert], bool]
		選択の条件となるboolを返す関数。
	"""
	bm = bmesh.new()
	bm.from_mesh(obj.data)
	bm.select_flush(True)
	for vert in bm.verts:
		vert.select = condition_func(vert)

	# これがキモで呼ばないと選択状態が変わらない
	bm.select_flush(False)

	# 更新
	bm.to_mesh(obj.data)
	bm.free()










def is_edge_along_z_axis(edge: bmesh.types.BMEdge) -> bool:
	"""
	エッジがZ軸に沿っている（Z軸に平行）かどうかを判定する、`select_edges_by_condition`用の関数。

	Parameters:
		edge : bmesh.types.BMEdge

	Returns:
		bool
			エッジの始点と終点のZ座標が同じならTrue。
	"""
	return edge.verts[0].co[2] == edge.verts[1].co[2]










def make_circle_vertices(radius: float, num_vertices: int, center: tuple[float, float, float] = (0, 0, 0), start_angle_degree: float = 0, angle_degree: float = 360, normal_vector: tuple[float, float, float] = (0, 0, 1)) -> list[tuple[float, float, float]]:
	"""
	円周上の頂点群を生成する。指定された半径を持つ円を外接円とする多角形の作成にも使えるよ。頂点はディフォルトではXY平面上に配置され、Z座標はすべて0だけど、法線ベクトルを指定することで任意の平面に配置できるよ。

	Parameters
	----------
	radius : float
		円（外接円）の半径。
	num_vertices : int
		生成する頂点の数、または多角形の辺の数。
	center : tuple[float, float, float], optional
		円の中心座標 (x, y, z)
	start_angle_degree : float, optional
		開始角度（度単位）。デフォルトは0（右、X軸プラス）。90で上、180で左、270で下からになる。
	normal_vector : tuple[float, float, float], optional
		円を配置する平面の法線ベクトル。デフォルトは(0, 0, 1)、つまりZ軸で、XY平面に配置される。

	Returns
	-------
	list[tuple[float, float, float]]
		生成された頂点の座標リスト。(x, y, z)のリスト。
	"""
	vertices = []

	# 法線ベクトルを正規化
	normal = Vector(normal_vector).normalized()

	# Z軸（(0, 0, 1)）と法線ベクトルとの間の回転を表す行列を作成
	if normal != Vector((0, 0, 1)):
		rot_axis = normal.cross(Vector((0, 0, 1)))
		if rot_axis.length != 0:
			rot_axis.normalize()
			angle = math.acos(normal.dot(Vector((0, 0, 1))))
			rot_matrix = Matrix.Rotation(angle, 4, rot_axis)
		else:
			# 法線ベクトルがZ軸と一致または逆向きの場合
			rot_matrix = Matrix.Rotation(math.pi, 4, Vector((1, 0, 0))) if normal.z < 0 else Matrix.Identity(4)
	else:
		rot_matrix = Matrix.Identity(4)

	# 円の頂点を計算
	start_angle = math.radians(start_angle_degree)
	for i in range(num_vertices):
		angle = math.radians(angle_degree) * i / num_vertices + start_angle
		x = radius * math.cos(angle)
		y = radius * math.sin(angle)
		vertex = Vector((x, y, 0))
		vertex = rot_matrix @ vertex # 回転
		vertex += Vector(center) # 中心へ移動
		vertices.append(tuple(vertex))

	return vertices










def find_intersection(line1_start: Vector, line1_end: Vector, line2_start: Vector, line2_end: Vector, return_intersection_point_ratio: bool = False) -> Vector:
	"""
	二つの線分の交点を求める関数。

	Parameters
	----------
	line1_start : Vector | Tuple[float, float, float]
		線分1の始点。
	line1_end : Vector
		線分1の終点。
	line2_start : Vector
		線分2の始点。
	line2_end : Vector
		線分2の終点。
	return_intersection_point_ratio : bool, optional, default: False
		交点の座標をline1の始点からの相対的な割合で返すかどうか。これがTrueの場合、返り値はタプルとなる。

	Returns
	-------
	Vector or None or Tuple[Vector, float]
		二つの線分の交点。交点がなければNoneを返す。
		return_intersection_point_ratioにTrueを指定した場合、返り値は交点と、交点のline1の始点からの相対的な割合の値が含まれるタプルとなる。
	"""
	p = line1_start if isinstance(line1_start, Vector) else Vector(line1_start)
	q = line2_start if isinstance(line2_start, Vector) else Vector(line2_start)
	r = (line1_end if isinstance(line1_end, Vector) else Vector(line1_end)) - p
	s = (line2_end if isinstance(line2_end, Vector) else Vector(line2_end)) - q

	if r.cross(s).length == 0:
		# 線分が平行か重なっている場合
		return None

	t = (q - p).cross(s).length / r.cross(s).length
	u = (q - p).cross(r).length / r.cross(s).length

	result = None
	# 交点が両線分上に存在する
	if 0 <= t <= 1 and 0 <= u <= 1:
		result = p + t * r

	if return_intersection_point_ratio:
		return result, t
	else:
		return result










def is_blender_version_at_least(major: int, minor: int) -> bool:
	"""
	Blenderのバージョンが、指定されたバージョン以上かどうか判定

	Parameters
	----------
	major : int
		比較対象のメジャーバージョン番号。
	minor : int
		比較対象のマイナーバージョン番号。

	Returns
	-------
	bool
		指定されたバージョン以上の場合はTrue、そうでない場合はFalse。

	Notes
	-----
	"""
	# blenderのバージョンは bpy.app.version に[メジャー, マイナー, リビジョン]で格納されている
	return bpy.app.version[0] >= major and bpy.app.version[1] >= minor










def translate(s: str, category: Literal['IFACE', 'TIP', 'DATA', 'RPT']) -> str:
	"""
	指定された文字列をBlenderのシステムに頼らず自前で翻訳する処理。'Thickness'という単語が内部辞書で『幅』に翻訳されてしまうので、回避して正しく『厚み』に翻訳できるよう作った。

	Parameters
	----------
	s : str
		翻訳する文字列。
	category : Literal['IFACE', 'TIP', 'DATA', 'RPT']
		翻訳のカテゴリ。`RPT`はBlender 4.1以上で対応。

	Returns
	-------
	str
		翻訳後の文字列。`romly_translation.TRANSLATION_DICT`に見つからなかった場合は s をそのまま返す。
	"""

	# カテゴリがマッチするかのチェック。RPTは4.1以上のみ
	category_match = ((category == 'IFACE' and bpy.context.preferences.view.use_translate_interface) or
		(category == 'TIP' and bpy.context.preferences.view.use_translate_tooltips) or
		(category == 'DATA' and bpy.context.preferences.view.use_translate_new_dataname) or
		(is_blender_version_at_least(4, 1) and category == 'RPT' and bpy.context.preferences.view.use_translate_reports))

	if category_match:
		loc = bpy.app.translations.locale
		dict = romly_translation.TRANSLATION_DICT.get(loc)
		if dict:
			for key in dict:
				if key[1] == s:
					return dict[key]

	return s










def report(self: bpy.types.Operator, type: str, msg_key: str, params: dict[str, str] = None):
	"""
	BlenderのOperatorを使ったリポートを表示する。paramsに辞書を指定すると、文字列のformatに展開されて渡される。

	Parameters
	----------
	self : bpy.types.Operator
		オペレータークラスのインスタンスを指定
	type : str
		'INFO', 'WARNING', 'ERROR', 'DEBUG'
	msg_key : str
		表示するメッセージの辞書ファイルのキー
	params : Dict[str, str], optional
		指定されている場合、翻訳されたメッセージのformatに展開されて渡される。省略した場合はNoneでプレースホルダーの置き換えは行われない。
	"""
	if is_blender_version_at_least(4, 1):
		msg = bpy.app.translations.pgettext_rpt(msg_key)
	else:
		msg = bpy.app.translations.pgettext_iface(msg_key)

	if params:
		msg = msg.format(**params)

	self.report({type}, msg)










def register_classes_and_translations(classes: list[type]):
	"""翻訳辞書とクラスの登録。"""
	try:
		bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)
	except ValueError:
		bpy.app.translations.unregister(__name__)
		bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)

	# blenderへのクラス登録処理
	for cls in classes:
		bpy.utils.register_class(cls)










def unregister_classes_and_translations(classes: list[type]):
	"""翻訳辞書の登録解除。"""
	bpy.app.translations.unregister(__name__)

	# クラスの登録解除
	for cls in classes:
		bpy.utils.unregister_class(cls)
