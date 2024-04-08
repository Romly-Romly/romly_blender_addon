import bpy
import math
import mathutils
import bmesh
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import List, Tuple, NamedTuple



from . import romly_utils














class TetrahedronIndices(NamedTuple):
	"""
	正四面体の頂点と各要素のインデックスを格納するためのNamedTuple。create_regular_tetrahedronメソッドが返す。

	Parameters
	----------
	vertices : List[Vector]
		正四面体の頂点のリスト。各頂点はVectorオブジェクト。
	faces : List[List[int]]
		正四面体の面を構成する頂点のインデックスのリストのリスト。
	opposite_vertex_indices : List[int]
		各面の反対側にある球の中心となる頂点のインデックス。
	sphere_center_vertex_index_pairs : List[List[int]]
		交差部を取り、エッジとする球のペアの中心となる座標の（インデックスの）リスト。
	edge_arc_start_end_vertex_indices : List[List[int]]
		エッジの始点と終点のインデックスのリスト。
	adjoin_face_index_pairs : List[List[int]]
		shpere_pairsから生成されるエッジが接する2つの面のインデックスのリスト。
	"""
	vertices: List[Vector]
	faces: List[List[int]]
	opposite_vertex_indices: List[int]
	sphere_center_vertex_index_pairs: List[List[int]]
	edge_arc_start_end_vertex_indices: List[List[int]]
	adjoin_face_index_pairs: List[List[int]]








class ROMLYADDON_OT_add_reuleaux_tetrahedron(bpy.types.Operator):
	bl_idname = "romlyaddon.add_reuleaux_tetrahedron"
	bl_label = bpy.app.translations.pgettext_iface('Add Reuleaux Tetrahedron')
	bl_description = 'Construct a Reuleaux Tetrahedron mesh'
	bl_options = {'REGISTER', 'UNDO'}

	# UV球のリング数の最小値。設定できるのは8までで、-1の7にすると正四面体になる。
	RING_COUNT_MIN = 8 - 1

	# メッシュの生成方法
	BUILD_METHOD_UV_SPHERES = 'uv_shperes'
	BUILD_METHOD_ICO_SPHERES = 'ico_spheres'
	BUILD_METHOD_VERTICES = 'vertices'
	BUILD_METHOD_ITEMS = [
		(BUILD_METHOD_UV_SPHERES, 'UV Sphere', 'Use UV spheres intersection part. It collapses when the number of segments/ring count is few'),
		(BUILD_METHOD_ICO_SPHERES, 'Ico Sphere', 'Use Ico spheres intersection part. It collapses when the number of subdivisions is few'),
		(BUILD_METHOD_VERTICES, 'Calc Vertices', "Calculate vertex positions without using spheres. It won't collapse even if the number of subdivisions is few")
	]

	# 原点の位置
	ORIGIN_ITEMS = [
		('center', 'Center', 'Set mesh origin to its center.'),
		('bottom', 'Bottom Face', 'Set mesh origin to its bottom face center.'),
		('apex', 'Apex', 'Set mesh origin to its apex.')
	]


	# プロパティ

	# 外接円の半径
	val_radius: FloatProperty(name='Radius', description='The radius of spheres that construct Reuleaux Tetrahedron (Edge length of Regular Tetrahedron)', default=1.0, soft_min=0.01, soft_max=100.0, step=1, precision=2, unit='LENGTH')

	# 構築方法
	val_build_method: EnumProperty(name='Build Method', description='How to construct Reuleaux Tetrahedron mesh', default=BUILD_METHOD_VERTICES, items=BUILD_METHOD_ITEMS)

	# メッシュのセグメント数
	val_segments: IntProperty(name='Segments', description='The number of UV spheres segments', default=48, min=4, max=128, step=1)
	val_ring_count: IntProperty(name='Ring Count', description='The number of UV spheres ring counts', default=48, min=RING_COUNT_MIN, max=128, step=1)
	val_ico_subdivisions: IntProperty(name='Subdivisions', description='The number of ICO spheres subdivisions / Mesh subdivisions', default=3, min=0, max=6, step=1)

	val_triangulate: BoolProperty(name='Triangulate', description='Triangulate quad faces', default=True)

	# 原点をどこにするか
	val_origin: EnumProperty(name='Origin', description='原点位置', default='center', items=ORIGIN_ITEMS)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_radius')
		col.separator()

		col.label(text="Build Method")
		row = col.row(align=True)
		row.prop(self, 'val_build_method', expand=True)
		if (self.val_build_method == self.BUILD_METHOD_UV_SPHERES):
			col.prop(self, 'val_segments')
			col.prop(self, 'val_ring_count')
		else:
			col.prop(self, 'val_ico_subdivisions')
		col.prop(self, 'val_triangulate')
		col.separator()

		col.label(text="Origin")
		row = col.row(align=True)
		row.prop(self, 'val_origin', expand=True)



	def execute(self, context):
		# パラメータを取得
		radius = self.val_radius
		build_method = self.val_build_method
		segments = self.val_segments
		ring_count = self.val_ring_count
		ico_subdivisions = self.val_ico_subdivisions
		triangulate = self.val_triangulate
		origin = self.val_origin

		if ((build_method == self.BUILD_METHOD_ICO_SPHERES and ico_subdivisions == 0) or
			(build_method == self.BUILD_METHOD_UV_SPHERES and (segments == 4 or ring_count == self.RING_COUNT_MIN)) or
			(build_method == self.BUILD_METHOD_VERTICES and ico_subdivisions == 0)):
			# ICO球かつ分割数が0の場合、またはUV球かつsegmentsが4またはring_countが self.RING_COUNT_MIN の場合、
			# または頂点計算かつ分割数が0の場合、普通の正四面体を追加
			tetrahedron = create_regular_tetrahedron(radius, origin=origin)
			obj = romly_utils.create_object(tetrahedron.vertices, tetrahedron.faces, name=bpy.app.translations.pgettext_data('Regular Tetrahedron'))
			bpy.context.collection.objects.link(obj)

		elif build_method == self.BUILD_METHOD_VERTICES:
			# 頂点計算かつ、分割数が0でない場合
			vertices, faces = create_reuleaux_tetrahedron(radius=radius, origin=origin, subdivisions=ico_subdivisions)
			obj = romly_utils.create_object(vertices=vertices, faces=faces, name=bpy.app.translations.pgettext_data('Regular Tetrahedron'))
			bpy.context.collection.objects.link(obj)

		else:
			tetrahedron = create_regular_tetrahedron(radius, origin=origin)

			# 各頂点の位置に球を生成
			location = bpy.context.scene.cursor.location + tetrahedron.vertices[0]
			if build_method == self.BUILD_METHOD_UV_SPHERES:
				bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, segments=segments, ring_count=ring_count)
			else:
				bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, location=location, subdivisions=ico_subdivisions)
			sphere = bpy.context.active_object
			sphere.name = bpy.app.translations.pgettext_data('Reuleaux Tetrahedron')
			for i in range(1, 4):
				location = bpy.context.scene.cursor.location + tetrahedron.vertices[i]
				if build_method == self.BUILD_METHOD_UV_SPHERES:
					bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, segments=segments, ring_count=ring_count)
				else:
					bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, location=location, subdivisions=ico_subdivisions)
				bool_object = bpy.context.active_object
				bpy.context.view_layer.objects.active = sphere
				mod = bpy.context.object.modifiers.new(type='BOOLEAN', name='bool')
				mod.object = bool_object
				mod.operation = 'INTERSECT'
				bpy.ops.object.modifier_apply(modifier=mod.name)
				bpy.context.collection.objects.unlink(bool_object)

			bpy.context.view_layer.objects.active = sphere
			obj = bpy.context.active_object

		# 重複する頂点を削除
		obj = romly_utils.cleanup_mesh(obj)

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		# 三角形に分割
		if triangulate:
			bpy.ops.object.mode_set(mode='EDIT')
			bpy.ops.mesh.select_all(action='SELECT')
			bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
			bpy.ops.object.mode_set(mode='OBJECT')

		# オブジェクトの原点を3Dカーソル位置に設定
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

		return {'FINISHED'}











def subdivide_triangle(vertices: List[Vector], face: Tuple[int, int, int]) -> Tuple[List[int], List[Tuple[int, int, int]]]:
	"""
	三角形を分割して新しい頂点と面を生成します。

	Parameters
	----------
	vertices : List[Vector]
		三角形を含む頂点リスト。分割時にできた新しい頂点はこのリストに追加されます。
	face : Tuple[int, int, int]
		分割元の三角形を形成する頂点のインデックス。

	Returns
	-------
	tuple : Tuple[List[int], List[Tuple[int, int, int]]]
		新しい頂点のインデックスのリストと新しい面のリストを含むタプル。
	"""
	new_vertex_indices = []
	new_faces = []

	# 三角形の各頂点を取得
	v0 = vertices[face[0]]
	v1 = vertices[face[1]]
	v2 = vertices[face[2]]
	new_vertex_indices.append(face[0])
	new_vertex_indices.append(face[1])
	new_vertex_indices.append(face[2])

	# 三角形の各辺の中点を計算
	v3 = (v0 + v1) / 2
	v4 = (v1 + v2) / 2
	v5 = (v2 + v0) / 2

	# 新しい頂点を追加
	vertices.append(v3)
	new_vertex_indices.append(len(vertices) - 1)
	vertices.append(v4)
	new_vertex_indices.append(len(vertices) - 1)
	vertices.append(v5)
	new_vertex_indices.append(len(vertices) - 1)

	# 新しい面を追加
	i0 = len(vertices) - 3
	i1 = len(vertices) - 2
	i2 = len(vertices) - 1
	new_faces.append((i0, i1, i2))
	new_faces.append((face[0], i0, i2))
	new_faces.append((i0, face[1], i1))
	new_faces.append((i2, i1, face[2]))

	return new_vertex_indices, new_faces








def create_regular_tetrahedron(radius: float, origin: str) -> int:
	"""
	指定された半径と原点の位置に基づいて、正四面体の頂点、面、その他の情報を計算する。

	Parameters
	----------
	radius : float
		正四面体の半径。
	origin : str
		四面体の原点の位置を指定する文字列。'center'、'bottom'、または 'apex' のいずれか。

	Returns
	-------
	TetrahedronIndices
		頂点、面、球の中心、球のペア、弧の始点終点、隣接面インデックスのタプル。

	Raises
	------
	ValueError
		`origin` が 'center'、'bottom'、'apex' のいずれでもない場合に発生。
	"""
	if origin not in ['center', 'bottom', 'apex']:
		raise ValueError("`origin` は 'center'、'bottom'、または 'apex' のいずれかである必要があります。")

	# 四面体の頂点を計算する
	# 0: 底面（XY平面上の正三角形）の左下
	# 1: 底面の右下
	# 2: 底面の三角形の頂点
	# 3: 他の頂点とはZ軸が異なる、四面体の頂点
	vertices = [
		Vector((0, 0, 0)),
		Vector((radius, 0, 0)),
		Vector((radius / 2, math.sqrt(3) / 2 * radius, 0)),
		Vector((radius / 2, math.sqrt(3) / 6 * radius, math.sqrt(6) / 3 * radius))
	]

	# 原点の設定に従ってオフセットを計算
	offset = Vector((0, 0, 0))
	if origin == 'center':
		offset = (Vector(vertices[0]) + Vector(vertices[1]) + Vector(vertices[2]) + Vector(vertices[3])) / 4
	elif origin == 'bottom':
		offset = (Vector(vertices[0]) + Vector(vertices[1]) + Vector(vertices[2])) / 3
	elif origin == 'apex':
		offset = Vector(vertices[3])
	for i in range(len(vertices)):
		vertices[i] -= offset

	# 四面体の面を定義する
	faces = [(0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0)]

	return TetrahedronIndices(vertices=vertices, faces=faces,
		opposite_vertex_indices=[3, 2, 0, 1],
		sphere_center_vertex_index_pairs=[(2, 1), (2, 0), (3, 2), (3, 1), (0, 1), (3, 0)],
		edge_arc_start_end_vertex_indices=[(3, 0), (1, 3), (1, 0), (0, 2), (2, 3), (2, 1)],
		adjoin_face_index_pairs=[(1, 3), (1, 2), (0, 1), (3, 0), (2, 3), (0, 2)]
	)









def create_reuleaux_tetrahedron(radius, origin, subdivisions):
	# 四面体の頂点を計算する
	tetrahedron = create_regular_tetrahedron(radius, origin=origin)

	total_faces = []

	tetrahedron_each_face_vertex_indices = []

	# 四面体の各面について…
	for i in range(4):
		spherical_surface_vertex_indices = []

		current_faces = [tetrahedron.faces[i]]
		for j in range(subdivisions):
			temp_faces = []
			for face in current_faces:
				new_vertex_indices, new_faces = subdivide_triangle(tetrahedron.vertices, face)
				spherical_surface_vertex_indices.extend(new_vertex_indices)
				temp_faces.extend(new_faces)
			current_faces = temp_faces.copy()

		# 各頂点を球の表面上に移動
		sphere_center = tetrahedron.vertices[tetrahedron.opposite_vertex_indices[i]]
		for index in spherical_surface_vertex_indices:
			v = tetrahedron.vertices[index] - sphere_center
			tetrahedron.vertices[index] = sphere_center + v.normalized() * radius

		face_vertices = []
		for index in spherical_surface_vertex_indices:
			face_vertices.append(index)
		tetrahedron_each_face_vertex_indices.append(face_vertices)

		total_faces.extend(current_faces)



	# 稜線となる頂点を追加していく
	for i in range(len(tetrahedron.sphere_center_vertex_index_pairs)):
		sphere_center1 = tetrahedron.vertices[tetrahedron.sphere_center_vertex_index_pairs[i][0]]
		sphere_center2 = tetrahedron.vertices[tetrahedron.sphere_center_vertex_index_pairs[i][1]]
		start = tetrahedron.vertices[tetrahedron.edge_arc_start_end_vertex_indices[i][0]]
		end = tetrahedron.vertices[tetrahedron.edge_arc_start_end_vertex_indices[i][1]]
		segments = calculate_subdivided_edge_vertex_count(subdivisions - 1) - 1
		vertices_on_arc = sphere_intersection(sphere_center1, radius, sphere_center2, radius, start=start, end=end, segments=segments)

		old_vertices = tetrahedron.vertices.copy()
		for v in vertices_on_arc:
			tetrahedron.vertices.append(v)

		# 稜線と三角形部分を繋ぐ面を追加する
		for face_index in tetrahedron.adjoin_face_index_pairs[i]:
			single_face_vertex_indices = tetrahedron_each_face_vertex_indices[face_index]

			index = find_nearest_vertex(old_vertices, single_face_vertex_indices, vertices_on_arc[1])
			face = (len(old_vertices), len(old_vertices) + 1, index)
			total_faces.append(face)

			for j in range(1, len(vertices_on_arc) - 1, 1):
				index1 = find_nearest_vertex(old_vertices, single_face_vertex_indices, vertices_on_arc[j])
				index2 = find_nearest_vertex(old_vertices, single_face_vertex_indices, vertices_on_arc[j + 1])
				face = (len(old_vertices) + j, index1, index2, len(old_vertices) + j + 1)
				total_faces.append(face)

			index = find_nearest_vertex(old_vertices, single_face_vertex_indices, vertices_on_arc[-1])
			face = (len(old_vertices) + len(vertices_on_arc) - 2, len(old_vertices) + len(vertices_on_arc) - 1, index)
			total_faces.append(face)

	return tetrahedron.vertices, total_faces






def calculate_subdivided_edge_vertex_count(n: int):
	"""
	三角形の辺を分割した時の頂点数を返す関数。

	分割回数nに応じて、三角形の辺上に新たに追加される頂点の数を計算します。
	各分割で辺は中点で分割され、新しい頂点が追加されます。
	この関数は分割後の三角形の辺にある頂点の総数を返します。

	Parameters
	----------
	n : int
		分割する回数。n >= 0 である必要があります。

	Returns
	-------
	int
		分割後の三角形の辺にある頂点の総数。

	Examples
	--------
	>>> calculate_subdivided_edge_vertex_count(0)
	3
	>>> calculate_subdivided_edge_vertex_count(2)
	9
	"""
	if n < 0:
		raise ValueError("nは非負の整数である必要があります。")
	return 3 + (2 * (1 - 2 ** n) // (1 - 2))







def find_nearest_vertex(vertices: List[Vector], indices: List[int], target: Vector):
	"""
	指定された頂点リストから、ターゲット位置に最も近い頂点のインデックスを見つける。

	Parameters
	----------
	vertices : List[Vector]
		検索される頂点のリスト。
	indices : List[int]
		検索する頂点のインデックスのリスト。このリストにないverticesの頂点は無視される。
	target : Vector
		元になる頂点座標。この座標に近い頂点を見つける。

	Returns
	-------
	int
		ターゲットに最も近い頂点のインデックス。見つからない場合は-1。
	"""
	min_distance = float('inf')
	index = -1
	for i in indices:
		distance = (vertices[i] - target).length
		if distance < min_distance:
			min_distance = distance
			index = i
	return index








def sphere_intersection(sphere_center1, radius1, sphere_center2, radius2, start, end, segments):
	# 中心間の距離
	d = (sphere_center2 - sphere_center1).length

	# 交差円の中心と半径を計算
	d1 = (radius1**2 - radius2**2 + d**2) / (2 * d)
	r = math.sqrt(radius1**2 - d1**2)

	# 交差円の中心座標
	circle_center = sphere_center1 + (sphere_center2 - sphere_center1).normalized() * d1

	# 交差円が配置されるべき平面の法線ベクトルを計算
	normal_vector = (sphere_center2 - sphere_center1).normalized()

	# Z軸と法線ベクトルとの間の角度を計算
	angle = math.acos(normal_vector.dot(Vector((0, 0, 1))))

	# 回転軸（Z軸と法線ベクトルの外積）
	rotation_axis = Vector((0, 0, 1)).cross(normal_vector).normalized()

	# 回転行列を生成
	rotation_matrix = Matrix.Rotation(angle, 4, rotation_axis)
	inverse_rotation_matrix = rotation_matrix.inverted()

	# startとendを元の円の平面に投影
	start_local = inverse_rotation_matrix @ (start - circle_center)
	end_local = inverse_rotation_matrix @ (end - circle_center)

	# startとendの局所座標系での角度を計算
	start_angle = math.atan2(start_local.y, start_local.x)
	end_angle = math.atan2(end_local.y, end_local.x)

	# 角度の差を計算
	angle_diff = (end_angle - start_angle) % (2 * math.pi)
	if angle_diff <= 0:
		angle_diff += 2 * math.pi

	vertices = []
	for i in range(segments + 1):
		# 分割された角度で点を計算
		angle = start_angle + (angle_diff / segments) * i
		x = math.cos(angle) * r
		y = math.sin(angle) * r
		z = 0
		# ローカル座標系からワールド座標系へ変換
		vertex_coord = Vector((x, y, z))
		vertex_coord.rotate(rotation_matrix)
		vertex_coord += circle_center
		vertices.append(vertex_coord)

	return vertices

















# 親となるメニュー
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_reuleaux_tetrahedron.bl_idname, icon='MESH_CONE')





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')




# blenderへのクラス登録処理
def register():
	# 翻訳辞書の登録
	try:
		bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)
	except ValueError:
		bpy.app.translations.unregister(__name__)
		bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)

	try:
		bpy.utils.register_class(ROMLYADDON_OT_add_reuleaux_tetrahedron)
	except RuntimeError:
		pass
	try:
		bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	except RuntimeError:
		pass
	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	try:
		bpy.utils.unregister_class(ROMLYADDON_OT_add_reuleaux_tetrahedron)
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
	register()
