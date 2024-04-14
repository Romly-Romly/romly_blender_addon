import bpy
import math
import mathutils
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import List, Tuple, NamedTuple



from . import romly_utils
















def on_update_thickness(self, context):
	""" アンチオロイドの厚みとベベル幅プロパティの更新時の処理 """
	# ベベルの幅は厚みの半分に制限
	if self.val_bevel_width > self.val_thickness / 2:
		self.val_bevel_width = self.val_thickness / 2





class ROMLYADDON_OT_add_oloid(bpy.types.Operator):
	bl_idname = "romlyaddon.add_oloid"
	bl_label = bpy.app.translations.pgettext_iface('Add Oloid')
	bl_description = 'Construct an Oloid mesh'
	bl_options = {'REGISTER', 'UNDO'}

	# 形状
	TYPE_OLOID = 'oloid'
	TYPE_ANTI_OLOID = 'anti-oloid'
	TYPE_ITEMS = [
		(TYPE_OLOID, 'Oloid', 'Constructs a normal Oloid'),
		(TYPE_ANTI_OLOID, 'Anti-Oloid', 'Constructs an Anti-Oloid'),
	]
	val_type: EnumProperty(name='Type', description='The type of the Oloid', default=TYPE_OLOID, items=TYPE_ITEMS)

	val_radius: FloatProperty(name='Radius', description='The circles radius that construct the Oloid', default=1.0, soft_min=0.1, soft_max=100.0, step=1, precision=2, unit='LENGTH')
	val_segments: IntProperty(name='Vertices', description='The number of vertices in each circle that construct the Oloid. The actual number will be much fewer because some of them are deleted during construction', default=32, min=3, soft_max=128, step=1)

	# アンチオロイドのプロパティ
	val_thickness: FloatProperty(name='Thickness', description='The thickness of the Anti-Oloid', default=0.05, min=0.0, soft_max=1.0, step=1, precision=2, unit='LENGTH', update=on_update_thickness)
	val_loop_cuts: IntProperty(name='Loop Cut', description='The number of loop cuts of long faces. Subdivide it more solve the face distortion', default=0, min=0, soft_max=10, max=64, step=1)
	val_bevel_width: FloatProperty(name='Width', description='The bevel width of the Anti-Oloid', default=0.02, min=0.0, soft_max=1.0, step=1, precision=2, unit='LENGTH', update=on_update_thickness)
	val_bevel_segments: IntProperty(name='Segments', description='The number of segments in the bevel of the Anti-Oloid', default=5, min=1, soft_max=10, max=32, step=1)
	val_keep_modifiers: BoolProperty(name='Keep Modifiers', description="Keep modifiers if it's checked", default=False)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		row = col.row(align=True)
		row.prop(self, 'val_type', expand=True)
		col.prop(self, 'val_radius')
		col.prop(self, 'val_segments')

		if self.val_type == self.TYPE_ANTI_OLOID:
			col.prop(self, 'val_thickness')
			col.prop(self, 'val_loop_cuts')
			col.separator()

			col.label(text='Bevel')
			col.prop(self, 'val_bevel_width')
			col.prop(self, 'val_bevel_segments')
			col.prop(self, 'val_keep_modifiers')



	def execute(self, context):
		# パラメータを取得
		type = self.val_type
		radius = self.val_radius
		num_vertices = self.val_segments

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		theObject = None
		if type == self.TYPE_OLOID:
			theObject = create_oloid(radius=radius, num_vertices=num_vertices)
		else:
			theObject = create_anti_oloid(
				radius=radius,
				num_vertices=num_vertices,
				thickness=self.val_thickness,
				bevel_width=self.val_bevel_width,
				bevel_segments=self.val_bevel_segments,
				num_loop_cuts=self.val_loop_cuts)

			# モデファイアを適用
			if not self.val_keep_modifiers:
				for mod in theObject.modifiers:
					bpy.ops.object.modifier_apply(modifier=mod.name)



		# 重複する頂点を削除
		obj = romly_utils.cleanup_mesh(theObject, recalc_normals=False)

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		# オブジェクトの原点を3Dカーソル位置に設定
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

		return {'FINISHED'}










def create_two_circle_oloid_base(radius: float, num_vertices: int, make_edges: bool, name: str) -> bpy.types.Object:
	"""
	オロイドのベースとなる2つの円で構成されたオブジェクトを作成する。
	この基本形状は、指定された半径と頂点の数を持つ2つの円で、一つは基準位置に、もう一つはx軸周りに90度回転させた後、半径分右に移動させた位置に配置される。

	Parameters
	----------
	radius : float
		作成する円の半径。
	num_vertices : int
		各円に含まれる頂点の数。
	make_edges : bool
		Trueの場合、円の頂点間に辺を作成する。
	name : str
		作成されるオブジェクトにつける名前。

	Returns
	-------
	bpy.types.Object
		作成されたオロイドベースのオブジェクト。
	"""
	circle_vertices1 = create_circle_vertices((0, 0, 0), radius=radius, num_vertices=num_vertices, start_angle=180)

	# 2個目の円はx軸で90度回転させて半径分右に移動
	circle_vertices2 = create_circle_vertices((0, 0, 0), radius=radius, num_vertices=num_vertices, start_angle=0)
	for i in range(len(circle_vertices2)):
		v = rotate_vertex_90_degrees_x_axis(circle_vertices2[i])
		circle_vertices2[i] = (v[0] + radius, v[1], v[2])

	all_vertices = circle_vertices1 + circle_vertices2

	# edges が True の場合は辺を作成
	edges = []
	if make_edges:
		def add_edges(edges: List[Tuple[int, int]], vertices: List[Tuple[float, float, float]], start: int, count: int):
			"""指定された頂点群に対して順番に辺を追加し、最後の頂点は最初の頂点とで辺を作成"""
			for i in range(start, start + count - 1):
				edges.append((i, i + 1))
			edges.append((start + count - 1, start))

		add_edges(edges, all_vertices, start=0, count=len(circle_vertices1))
		add_edges(edges, all_vertices, start=len(circle_vertices1), count=len(circle_vertices2))

	# 頂点群からオブジェクトを生成
	obj = romly_utils.create_object(all_vertices, faces=[], name=name, edges=edges)
	return obj










def create_oloid(radius: float, num_vertices: int) -> bpy.types.Object:
	"""
	オロイド形状のオブジェクトを生成する。

	Parameters
	----------
	radius : float
		オロイドを構成する2つの円の半径。
	num_vertices : int
		円を構成する頂点の数。

	Returns
	-------
	bpy.types.Object
		作成されたオロイドオブジェクト。
	"""
	# オロイドの基礎となる2つの円で構成されるオブジェクトを作成
	obj = create_two_circle_oloid_base(radius=radius, num_vertices=num_vertices, make_edges=False, name=bpy.app.translations.pgettext_data('Oloid'))

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

	return obj







def create_anti_oloid(radius: float, num_vertices: int, thickness: float, bevel_width: float, bevel_segments: int, num_loop_cuts: int) -> bpy.types.Object:
	"""
	アンチオロイド形状のオブジェクトを生成する。

	Parameters
	----------
	radius : float
		オロイドを構成する2つの円の半径。
	num_vertices : int
		円を構成する頂点の数。
	thickness : float
		アンチオロイドの厚み。
	bevel_width : float
		厚みの縁に付けるベベルの幅。
	bevel_segments : int
		ベベルのセグメント数。
	num_loop_cuts : int
		ループカットの回数。

	Returns
	-------
	bpy.types.Object
		作成されたアンチオロイドオブジェクト。
	"""

	# オロイドの基礎となる2つの円で構成されるオブジェクトを作成
	obj = create_two_circle_oloid_base(radius=radius, num_vertices=num_vertices, make_edges=True, name=bpy.app.translations.pgettext_data('Anti-Oloid'))
	bpy.context.collection.objects.link(obj)
	bpy.context.view_layer.objects.active = obj

	bpy.ops.object.mode_set(mode='EDIT')

	# Bevel Weightを設定
	mesh = bmesh.from_edit_mesh(obj.data)
	# Bevel Weightのレイヤーを取得（存在しない場合は新しく作成）
	bevel_layer = mesh.edges.layers.float.get('bevel_weight_edge', mesh.edges.layers.float.new('bevel_weight_edge'))
	for edge in mesh.edges:
		edge[bevel_layer] = 1.0

	# ブリッジループで繋ぎ、面の向きを統一
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.bridge_edge_loops()
	bpy.ops.mesh.normals_make_consistent(inside=False)

	# ループカット。増やすと細長い面が分割されて滑らかになる。
	if num_loop_cuts > 0:
		mesh.edges.ensure_lookup_table()
		edge_index = len(mesh.edges) - 1
		bpy.ops.mesh.loopcut_slide(
			MESH_OT_loopcut={"number_cuts":num_loop_cuts, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":edge_index, "mesh_select_mode_init":(True, False, False)},
			TRANSFORM_OT_edge_slide={"value":0, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":True, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False, "alt_navigation":False})

	# オブジェクトモードに戻す
	bpy.ops.object.mode_set(mode='OBJECT')

	# Solidifyモデファイアを追加して厚みを設定
	mod = bpy.context.object.modifiers.new(type='SOLIDIFY', name='Solidify')
	mod.thickness = thickness
	mod.offset = 0
	# Even ThicknessはTrueにすると円の頂点数が少ない時に破綻しやすいので辞めた
	mod.use_even_offset = False

	# ベベルを追加。ベベルは幅が0だと適用するとエラーになるので、0より大きい場合にのみ追加する
	if bevel_width > 0:
		mod = bpy.context.object.modifiers.new(type='BEVEL', name='Bevel')
		mod.width = bevel_width
		mod.segments = bevel_segments
		mod.limit_method = 'WEIGHT'

	return obj








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
		layout.operator(ROMLYADDON_OT_add_oloid.bl_idname, text=bpy.app.translations.pgettext_iface('Add Oloid'), icon='MESH_CAPSULE')









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
