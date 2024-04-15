import bpy
import math
import mathutils
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import List, Tuple, NamedTuple



from . import romly_utils















def remove_y_minus_vertices(vertices: List[Tuple[float, float, float]], edges: List[Tuple[int, int]]) -> Tuple[List[Tuple[float, float]], List[Tuple[int, int]]]:
	"""
	Y座標がマイナスの頂点を削除し、関連するエッジを更新する関数。

	Parameters
	----------
	vertices : List[Tuple[float, float, float]]
		頂点のリスト。
	edges : List[Tuple[int, int]]
		辺のリスト。各辺は頂点のインデックス2つを持つタプル。

	Returns
	-------
	Tuple[List[Tuple[float, float, float]], List[Tuple[int, int]]]
		更新された頂点とエッジのリスト。
	"""
	# y < -0.0001 の頂点を削除
	# 0にするとy座標が0の頂点も削除されてしまうことがあったのでこの値にした。
	vertices_to_delete = {i for i, v in enumerate(vertices) if v[1] < -0.0001}

	# 削除するエッジを見つける
	edges = [e for e in edges if e[0] not in vertices_to_delete and e[1] not in vertices_to_delete]

	# 頂点リストから削除する頂点を除外
	new_vertices = [v for i, v in enumerate(vertices) if i not in vertices_to_delete]

	# 新しい頂点リストでのインデックスに更新
	index_map = {old_idx: new_idx for new_idx, old_idx in enumerate(i for i in range(len(vertices)) if i not in vertices_to_delete)}
	new_edges = [(index_map[e[0]], index_map[e[1]]) for e in edges]

	return new_vertices, new_edges










# def distance(v1, v2) -> float:
# 	vec1 = v1 if isinstance(v1, Vector) else Vector(v1)
# 	vec2 = v2 if isinstance(v2, Vector) else Vector(v2)
# 	return (vec2 - vec1).length

def create_rotation_base_object(radius: float, num_vertices: int) -> bpy.types.Object:
	"""
	スフェリコンの基本となる回転体の元になるオブジェクトを作成する。
	これはYZ平面上に展開された半径radiusの円を外接円とする多角形をY=0でカットした形状。

	Parameters
	----------
	radius : float
		_description_
	num_vertices : int
		_description_

	Returns
	-------
	bpy.types.Object
		_description_
	"""
	# YZ平面上に円の頂点群を作成
	vertices = romly_utils.create_circle_vertices(radius=radius, num_vertices=num_vertices, start_angle_degree=0, normal_vector=(1, 0, 0))

	# 多角形になるよう辺を作成
	edges = []
	for i in range(len(vertices)):
		if i < len(vertices) - 1:
			edges.append((i, i + 1))
		else:
			edges.append((i, 0))

	# すべての辺についてZ軸との交点を調べ、交差していたら交点までの辺を追加
	for i in reversed(range(len(edges))):
		edge = edges[i]
		intersection, intersection_point_ratio = romly_utils.find_intersection(line1_start=vertices[edge[0]], line1_end=vertices[edge[1]], line2_start=Vector((0, 0, -1000)), line2_end=Vector((0, 0, 1000)), return_intersection_point_ratio=True)
		if (intersection is not None and
			0.0001 < intersection_point_ratio < 0.9999):
			vertices.append(intersection)
			edges.pop(i)
			if vertices[edge[0]][1] < 0:
				edges.append((len(vertices) - 1, edge[1]))
			else:
				edges.append((len(vertices) - 1, edge[0]))

	# 始点終点いずれかがYマイナスにある辺を削除する
	vertices, edges = remove_y_minus_vertices(vertices, edges)

	# オブジェクトを生成
	return romly_utils.create_object(vertices, faces=[], name='Sphericon', edges=edges)










class ROMLYADDON_OT_add_sphericon(bpy.types.Operator):
	bl_idname = "romlyaddon.add_sphericon"
	bl_label = bpy.app.translations.pgettext_iface('Add Sphericon')
	bl_description = 'Construct a Sphericon'
	bl_options = {'REGISTER', 'UNDO'}

	# 頂点数（何角形から作るか）
	val_vertices: IntProperty(name='Vertices', description='The number of vertices in the polygon that constructs the Sphericon', default=4, min=3, soft_max=16, max=32, step=1)

	val_num_rotation: IntProperty(name='Rotation', description='How many rotations should the shape be offset by on each side to create a sphericon', default=1, min=0, step=1)

	# 大きさ
	val_diagonal_length: FloatProperty(name='Diagonal Length', description='The diagonal length of the Sphericon', default=1.0, min=0.1, soft_max=100.0, step=1, precision=4, unit='LENGTH')

	# 円錐形状の回転方向のセグメント数
	val_segments: IntProperty(name='Segments', description='The number of segments in the conic parts of the Sphericon', default=32, min=2, soft_max=64, max=256, step=1)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_vertices')
		col.prop(self, 'val_num_rotation')
		col.prop(self, 'val_diagonal_length')
		col.prop(self, 'val_segments')



	def execute(self, context):
		bpy.ops.object.select_all(action='DESELECT')

		# まず回転体の元になる形状（正四角形の半分）を作成
		left_obj = create_rotation_base_object(radius=self.val_diagonal_length / 2, num_vertices=self.val_vertices)
		bpy.context.collection.objects.link(left_obj)

		bpy.context.view_layer.objects.active = left_obj

		# Screwモデファイアで回転体にする
		mod = bpy.context.object.modifiers.new(type='SCREW', name='Screw')
		mod.angle = math.pi
		mod.screw_offset = 0
		mod.axis = 'Z'
		mod.steps = self.val_segments
		mod.render_steps = self.val_segments
		mod.use_merge_vertices = False
		mod.use_smooth_shade = False	# これを忘れるとスムーズシェーディングになってしまうのだ
		bpy.ops.object.modifier_apply(modifier=mod.name)

		# 右側用に複製
		left_obj.select_set(state=True)
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False})

		# 右側を回転
		bpy.ops.transform.rotate(value=math.pi, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')

		# X軸で回転してスフェリコンに
		x_rot_degree = 360.0 / self.val_vertices * self.val_num_rotation
		bpy.ops.transform.rotate(value=math.radians(x_rot_degree), orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')

		right_obj = bpy.context.view_layer.objects.active

		# 2つのオブジェクトを合成
		left_obj.select_set(state=True)
		right_obj.select_set(state=True)
		bpy.context.view_layer.objects.active = left_obj
		bpy.ops.object.join()

		left_obj = romly_utils.cleanup_mesh(left_obj)

		# オブジェクトを3Dカーソル位置へ移動
		left_obj.location = bpy.context.scene.cursor.location

		return {'FINISHED'}










class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_sphericon.bl_idname, text=bpy.app.translations.pgettext_iface('Add Sphericon'), icon='MESH_CAPSULE')









# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	# 翻訳辞書の登録
	bpy.app.translations.register(__name__, romly_translation.TRANSLATION_DICT)

	bpy.utils.register_class(ROMLYADDON_OT_add_sphericon)
	bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	try:
		bpy.utils.unregister_class(ROMLYADDON_OT_add_sphericon)
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
