import bpy
import math
import mathutils
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import List, Tuple, NamedTuple



from . import romly_utils

















class ROMLYADDON_OT_add_oloid(bpy.types.Operator):
	bl_idname = "romlyaddon.add_oloid"
	bl_label = bpy.app.translations.pgettext_iface('Add Oloid')
	bl_description = 'Construct an Oloid mesh'
	bl_options = {'REGISTER', 'UNDO'}

	val_radius: FloatProperty(name='Radius', description='The circles radius that construct the Oloid', default=1.0, soft_min=0.1, soft_max=100.0, step=1, precision=2, unit='LENGTH')
	val_segments: IntProperty(name='Vertices', description='The number of vertices in each circle that construct the Oloid. The actual number will be much fewer because some of them are deleted during construction', default=32, min=3, soft_max=128, step=1)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_radius')
		col.prop(self, 'val_segments')



	def execute(self, context):
		# パラメータを取得
		radius = self.val_radius
		num_vertices = self.val_segments

		circle_vertices1 = create_circle_vertices((0, 0, 0), radius=radius, num_vertices=num_vertices, start_angle=180)

		# 2個目の円はx軸で90度回転させて半径分右に移動
		circle_vertices2 = create_circle_vertices((0, 0, 0), radius=radius, num_vertices=num_vertices, start_angle=0)
		for i in range(len(circle_vertices2)):
			v = rotate_vertex_90_degrees_x_axis(circle_vertices2[i])
			circle_vertices2[i] = (v[0] + radius, v[1], v[2])

		# 頂点群からオブジェクトを生成
		obj = romly_utils.create_object(circle_vertices1 + circle_vertices2, faces=[], name='Oloid')
		bpy.context.collection.objects.link(obj)

		bpy.context.view_layer.objects.active = obj
		bpy.ops.object.mode_set(mode='EDIT')

		# 円を繋いでオロイドを形成
		bpy.ops.mesh.select_all(action='SELECT')
		bpy.ops.mesh.convex_hull(shape_threshold=0)
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')



		# 円を構成する辺にシームを設定
		mesh = bmesh.from_edit_mesh(obj.data)

		# 頂点、辺、面にアクセスする前にインデックステーブルを更新
		mesh.verts.ensure_lookup_table()
		mesh.edges.ensure_lookup_table()
		mesh.faces.ensure_lookup_table()

		bpy.ops.mesh.select_mode(type="EDGE")

		bpy.ops.mesh.select_all(action='DESELECT')	# 選択をクリア
		for edge in mesh.edges:
			v1, v2 = edge.verts
			if (abs(v1.co.z) < 1e-9 and abs(v2.co.z) < 1e-9 and
				distance_to_point(v1, origin=(0, 0, 0)) <= radius * 1.001 and
				distance_to_point(v2, origin=(0, 0, 0)) <= radius * 1.001):
				edge.select = True
		bpy.ops.mesh.mark_seam(clear=False)

		bpy.ops.mesh.select_all(action='DESELECT')	# 選択をクリア
		for edge in mesh.edges:
			v1, v2 = edge.verts
			if (abs(v1.co.y) < 1e-9 and abs(v2.co.y) < 1e-9 and
				distance_to_point(v1, origin=(radius, 0, 0)) <= radius * 1.001 and
				distance_to_point(v2, origin=(radius, 0, 0)) <= radius * 1.001):
				edge.select = True
		bpy.ops.mesh.mark_seam(clear=False)

		bpy.ops.mesh.select_all(action='DESELECT')	# 選択をクリア
		farthest_v = farthest_x_vertex(mesh)
		for edge in mesh.edges:
			v1, v2 = edge.verts
			if ((v1.co.z < 0 and distance_to_point(v2, origin=farthest_v) < 1e-9) or
				(v2.co.z < 0 and distance_to_point(v1, origin=farthest_v) < 1e-9)):
				edge.select = True
				break
		bpy.ops.mesh.mark_seam(clear=False)

		# UVを設定
		bpy.ops.mesh.select_all(action='SELECT')
		bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)

		bpy.ops.object.mode_set(mode='OBJECT')



		# 重複する頂点を削除
		obj = romly_utils.cleanup_mesh(obj)

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		# オブジェクトの原点を3Dカーソル位置に設定
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

		return {'FINISHED'}










def farthest_x_vertex(mesh: bmesh.types.BMesh) -> Tuple[float, float, float]:
	"""
	X軸上で一番左（マイナス）にある頂点の座標を探すメソッド。

	Parameters
	----------
	mesh : bmesh.types.BMesh
		検索対象のメッシュオブジェクト。

	Returns
	-------
	Tuple[float, float, float]
		一番左にある頂点の座標。全ての頂点が正のX値を持つ場合はNoneを返す。

	"""
	max_distance = 0
	result = None
	for v in mesh.verts:
		if v.co.x < max_distance:
			max_distance = v.co.x
			result = v.co

	return result












def distance_to_point(v: BMVert, origin: Tuple[float, float, float]) -> float:
	"""
	与えられた頂点と特定の点との間の距離を計算する。

	Parameters
	----------
	vertex : BMVert
		距離を計算する対象の頂点。
	origin : Tuple[float, float, float]
		始点となる座標のタプル。(x, y, z)の形式。

	Returns
	-------
	float
		`vertex`と`origin`の間のユークリッド距離。

	"""
	return math.sqrt(
		(v.co.x - origin[0]) ** 2 +
		(v.co.y - origin[1]) ** 2 +
		(v.co.z - origin[2]) ** 2)








def rotate_vertex_90_degrees_x_axis(vertex: Tuple[float, float, float]) -> Tuple[float, float, float]:
	"""
	頂点をx軸で90度回転させる

	パラメータ
	----------
	vertex : Tuple[float, float, float]
		回転させる頂点の座標 (x, y, z)

	戻り値
	-------
	Tuple[float, float, float]
		x軸で90度回転後の頂点の座標 (x, -z, y)
	"""
	return (vertex[0], -vertex[2], vertex[1])










def create_circle_vertices(center: Tuple[float, float, float], radius: float, num_vertices: int, start_angle: float = 0) -> List[Tuple[float, float, float]]:
	"""
	円周上の頂点群を生成する。

	Parameters
	----------
	center : Tuple[float, float, float]
		円の中心座標 (x, y)。
	radius : float
		円の半径。
	num_vertices : int
		生成する頂点の数。
	start_angle_degree : float, optional
		開始角度（度単位）。デフォルトは0（右）。90で上、180で左、270で下からになる。

	Returns
	-------
	List[Tuple[float, float, float]]
		生成された頂点の座標リスト (x, y)。
	"""
	vertices = []
	for i in range(num_vertices):
		angle = 2 * math.pi * i / num_vertices + math.radians(start_angle)
		x = center[0] + radius * math.cos(angle)
		y = center[1] + radius * math.sin(angle)
		vertices.append((x, y, 0))
	return vertices










class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_oloid.bl_idname, icon='MESH_CAPSULE')









# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	# 翻訳辞書の登録
	bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)

	bpy.utils.register_class(ROMLYADDON_OT_add_oloid)
	bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	try:
		bpy.utils.unregister_class(ROMLYADDON_OT_add_oloid)
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
