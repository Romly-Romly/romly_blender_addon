import bpy
import bmesh
import mathutils
import math





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





def create_object(vertices: list, faces: list, name: str = '', mesh_name: str = None):
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

	Returns
	-------
	bpy.types.Object
		作成されたオブジェクトのインスタンス。
	"""
	if mesh_name is None:
		mesh_name = name + '_mesh'
	mesh = bpy.data.meshes.new(mesh_name)
	mesh.from_pydata(vertices, [], faces)
	obj = bpy.data.objects.new(name, mesh)
	return obj





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





def extrude_face(vertices, faces, extrude_vertex_indices, z_offset, cap=True):
	"""
	指定された面を掃引して、新しくできた頂点と面を追加する。

	Parameters
	----------
	vertices : list of Vector
		頂点のリスト
	faces : list of list of int
		面を構成する頂点インデックスのリスト
	extrude_vertex_indices : list of int
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





def rotate_vertices(object, degrees, axis):
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
		for v in object:
			v.rotate(mathutils.Matrix.Rotation(math.radians(degrees), 4, axis))
