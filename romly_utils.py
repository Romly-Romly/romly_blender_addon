import bpy
import bmesh
import mathutils
import math
from mathutils import Vector, Matrix
from typing import List, Tuple, NamedTuple, Callable





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





def create_object(vertices: list, faces: list, name: str = '', mesh_name: str = None, edges: List[Tuple[int, int]] = []) -> bpy.types.Object:
	"""
	指定された頂点リストと面リストから新しいオブジェクトを生成する。

	Parameters
	----------
	vertices : list of tuple of float
		オブジェクトの頂点座標のリスト。
	faces : list of tuple of int
		オブジェクトの面を構成する頂点のインデックスのリスト。
	name : str
		作成されるオブジェクトの名前。
	mesh_name : str, optional
		作成されるメッシュデータの名前。デフォルトでは、オブジェクト名に '_mesh' を追加されたものになる。
	edges : List[Tuple[int, int]], optional
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





def extrude_face(vertices, faces, extrude_vertex_indices: List[int], z_offset: float, cap=True):
	"""
	指定された面を掃引して、新しくできた頂点と面を追加する。

	Parameters
	----------
	vertices : list of Vector
		頂点のリスト
	faces : list of list of int
		面を構成する頂点インデックスのリスト
	extrude_vertex_indices : List[int]
		掃引する頂点のインデックスのリスト。頂点(Vector)のリストじゃないので注意してね。
	z_offset : float
		掃引する距離
	cap : bool, optional
		掃引したすべての頂点を結ぶ面を作るか。つまり、面をキャップ（閉じる）するかどうか。
	"""
	# 各頂点を掃引した位置に複製する
	for i in extrude_vertex_indices:
		v = vertices[i].copy()
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





def units_to_string(value, removeSpace=False):
	"""
	Blender内の単位を文字列に変換する。

	Parameters
	----------
	value : float
		変換する単位の値。
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
	s = bpy.utils.units.to_string(unit_system=bpy.context.scene.unit_settings.system, unit_category=bpy.utils.units.categories.LENGTH, value=value * bpy.context.scene.unit_settings.scale_length)

	# スペースの削除
	if removeSpace:
		s = s.replace(' ', '')

	return s





def rotated_vector(vector, angleRadians, axis):
	"""原点周りで回転したベクトルを生成して返す。

	Parameters
	----------
	vector : Vector
		元になるベクトル。
	angleRadians : Float
		ラジアン単位の回転角度。
	axis : ['X', 'Y', 'Z']
		回転軸。Matrix.Rotationメソッドにそのまま渡される。

	Returns
	-------
	Vector
		回転したベクトル。新しいベクトルが生成されて返される。
	"""
	v = vector.copy()
	v.rotate(mathutils.Matrix.Rotation(angleRadians, 4, axis))
	return v





def rotate_vertices(object, degrees: float, axis: str):
	"""MeshまたはVectorの配列のすべての頂点を原点周りで回転する

	Parameters
	----------
	object : Mesh or list[Vector]
		回転する頂点を含むMeshオブジェクトか、Vectorの配列。
	axis : ['X', 'Y', 'Z']
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
	mod_name = 'Boolean'
	mod = bpy.context.object.modifiers.new(type='BOOLEAN', name=mod_name)
	mod.operation = operation
	mod.object = boolObject
	mod.use_self = use_self
	if fast_solver:
		mod.solver = 'FAST'
	if apply:
		bpy.ops.object.modifier_apply(modifier=mod_name)
	if unlink:
		bpy.context.collection.objects.unlink(boolObject)










def select_edges_on_fair_surface(object: bpy.types.Object) -> None:
	"""
	平面上にある辺（隣接する面の法線が同じ辺）を選択します。

	Parameters
	----------
	object : bpy.types.Object
		法線を比較して辺を選択する対象のBlenderオブジェクト。
	"""
	bpy.ops.mesh.select_mode(type='EDGE')
	bm = bmesh.from_edit_mesh(object.data)

	# まず選択を解除
	bpy.ops.mesh.select_all(action='DESELECT')

	THRESHOLD = 0.999
	for edge in bm.edges:
		linked_faces = edge.link_faces
		if len(linked_faces) == 2:
			# 両面の法線を取得
			normal1 = linked_faces[0].normal
			normal2 = linked_faces[1].normal

			# 法線の内積を計算
			dot = normal1.dot(normal2)

			# ドット積が閾値以上なら、その辺を選択
			if dot > THRESHOLD:
				edge.select = True

	# 更新を反映
	bmesh.update_edit_mesh(object.data)










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










def select_edges_by_condition(condition_func: Callable[[bmesh.types.BMEdge], bool]) -> None:
	"""
	指定された条件に合った全てのエッジを選択する。

	Parameters
	----------
	condition_func : Callable[[bmesh.types.BMEdge], bool]
		選択の条件となるboolを返す関数。
	"""
	# from_edit_mesh は編集モードでないとエラーになるので、必要に応じて編集モードに変更
	obj = bpy.context.view_layer.objects.active
	current_mode = bpy.context.object.mode
	if current_mode != 'EDIT':
		bpy.ops.object.mode_set(mode='EDIT')

	bpy.ops.mesh.select_all(action='DESELECT')	# 選択をクリア

	bm = bmesh.from_edit_mesh(obj.data)
	for edge in bm.edges:
		edge.select = condition_func(edge)
	bmesh.update_edit_mesh(obj.data)

	if current_mode != bpy.context.object.mode:
		bpy.ops.object.mode_set(mode=current_mode)










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










def create_circle_vertices(radius: float, num_vertices: int, center: Tuple[float, float, float] = (0, 0, 0), start_angle_degree: float = 0, normal_vector: Tuple[float, float, float] = (0, 0, 1)) -> List[Tuple[float, float, float]]:
	"""
	円周上の頂点群を生成する。指定された半径を持つ円を外接円とする多角形の作成にも使えるよ。頂点はディフォルトではXY平面上に配置され、Z座標はすべて0だけど、法線ベクトルを指定することで任意の平面に配置できるよ。

	Parameters
	----------
	radius : float
		円（外接円）の半径。
	num_vertices : int
		生成する頂点の数、または多角形の辺の数。
	center : Tuple[float, float, float], optional
		円の中心座標 (x, y, z)
	start_angle_degree : float, optional
		開始角度（度単位）。デフォルトは0（右、X軸プラス）。90で上、180で左、270で下からになる。
	normal_vector : Tuple[float, float, float], optional
		円を配置する平面の法線ベクトル。デフォルトは(0, 0, 1)、つまりZ軸で、XY平面に配置される。

	Returns
	-------
	List[Tuple[float, float, float]]
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
		angle = 2 * math.pi * i / num_vertices + start_angle
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
