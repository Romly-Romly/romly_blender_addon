import bpy
import math
import mathutils
import bmesh
from bpy.props import *
from mathutils import Vector



from . import romly_utils









# MARK: Class
class ROMLYADDON_OT_add_reuleaux_polygon(bpy.types.Operator):
	bl_idname = 'romlyaddon.add_reuleaux_polygon'
	bl_label = bpy.app.translations.pgettext_iface('Add Reuleaux Polygon')
	bl_description = 'Construct a Reuleaux Polygon mesh'
	bl_options = {'REGISTER', 'UNDO'}

	# プロパティ

	# 何角形か
	val_num_sides: IntProperty(name='Sides', description='Number of sides for the polygon', default=3, min=3, soft_max=20, max=100, step=1)

	# 外接円の半径
	val_radius: FloatProperty(name='Radius', description='The radius of the circumradius', default=1.0, soft_min=0.01, soft_max=100.0, step=1, precision=2, unit=bpy.utils.units.categories.LENGTH)

	# 円弧部のセグメント数
	val_segments: IntProperty(name='Segments', description='Number of segments in each arc', default=16, min=1, max=128, step=1)

	# 整列（作成する平面）
	val_align_plane: EnumProperty(name='Construct on', items=romly_utils.ALIGN_PLANE_ITEMS, default='xy')



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_num_sides')
		col.prop(self, 'val_radius')
		col.prop(self, 'val_segments')
		col.prop(self, 'val_align_plane')



	def execute(self, context):
		# パラメータを取得
		num_sides = self.val_num_sides
		radius = self.val_radius
		segments = self.val_segments

		# まず多角形の頂点リストを作る
		polygon_vertices = romly_utils.make_circle_vertices(radius=radius, num_vertices=num_sides)

		# ルーローの多角形にするために各辺の始点と終点を始点、終点とする円弧を描いていく
		reuleaux_polygon_vertices = []
		if (num_sides % 2) == 1:
			# 頂点の数が奇数の場合、辺の反対にある頂点を中心として円弧を描く。
			# 指定されたインデックスの頂点に対する円弧の始点と終点は反対側の辺、つまり 頂点のインデックス+頂点数//2 と 頂点のインデックス+頂点数//2+1 になる。
			for i in range(num_sides):
				center = polygon_vertices[i]
				start = polygon_vertices[(i + num_sides // 2) % num_sides]
				end = polygon_vertices[(i + num_sides // 2 + 1) % num_sides]
				reuleaux_polygon_vertices.extend(create_arc(center=center, start=start, end=end, segments=segments))
		else:
			for i in range(num_sides):
				# 頂点の数が偶数の場合は、反対側の辺の中点を中心として円弧を描く。
				center = Vector(polygon_vertices[i]) + (Vector(polygon_vertices[(i + 1) % num_sides]) - Vector(polygon_vertices[i])) / 2
				start = polygon_vertices[(i + num_sides // 2) % num_sides]
				end = polygon_vertices[(i + num_sides // 2 + 1) % num_sides]
				reuleaux_polygon_vertices.extend(create_arc(center=center, start=start, end=end, segments=segments))

		# ngonで面を作成
		faces = [list(range(len(reuleaux_polygon_vertices)))]



		# オブジェクトを生成し、クリーンアップした上でシーンに追加
		obj = romly_utils.cleanup_mesh(romly_utils.create_object(reuleaux_polygon_vertices, faces, name=get_polygon_name(num_sides=num_sides)))
		bpy.context.collection.objects.link(obj)

		# 90度回転
		romly_utils.rotate_vertices(obj, degrees=90, axis='Z')




		# オブジェクトを3Dカーソル位置へ移動
		obj.location = bpy.context.scene.cursor.location

		# 整列
		romly_utils.set_object_rotation_to_plane(obj, plane=self.val_align_plane)

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}









def get_polygon_name(num_sides):
	"""
	辺の数に基づいて多角形の名前を返す関数。 'Reauleax + 多角形の名前' になるけど、辺の数が偶数の場合はルーローの多角形ではないので 'Reuleaux-ish' になる。20角形より多い場合は 'Polygon'。

	Parameters:
		num_sides (int): 多角形の辺の数。

	Returns:
		str: 指定された辺の数に基づく多角形の名前。
	"""
	# 辺の数に基づいて基本の名前を決定。辺の数が偶数の場合はルーローの多角形ではないので、 Reuleaux-ish とする。
	polygon_names = {
		3: 'Reuleaux Triangle',
		4: 'Reuleaux-ish Square',
		5: 'Reuleaux Pentagon',
		6: 'Reuleaux-ish Hexagon',
		7: 'Reuleaux Heptagon',
		8: 'Reuleaux-ish Octagon',
		9: 'Reuleaux Nonagon',
		10: 'Reuleaux-ish Decagon',
		11: 'Reuleaux Hendecagon',
		12: 'Reuleaux-ish Dodecagon',
		13: 'Reuleaux Tridecagon',
		14: 'Reuleaux-ish Tetradecagon',
		15: 'Reuleaux Pentadecagon',
		16: 'Reuleaux-ish Hexadecagon',
		17: 'Reuleaux Heptadecagon',
		18: 'Reuleaux-ish Octadecagon',
		19: 'Reuleaux Enneadecagon',
		20: 'Reuleaux-ish Icosagon'
	}

	# 辺の数が奇数か偶数かに応じて名前を修正
	if num_sides in polygon_names:
		result = polygon_names[num_sides]
	else:
		if num_sides % 2 == 1:
			result = 'Reuleaux Polygon'
		else:
			result = 'Reuleaux-ish Polygon'

	return bpy.app.translations.pgettext_data(result)










def create_arc(center: Vector, start: Vector, end: Vector, segments):
	# 半径を求める
	radius = (Vector(start) - Vector(center)).length

	# startとendのベクトルと中心点vを基に、角度を計算
	angle_start = math.atan2(start[1] - center[1], start[0] - center[0])
	angle_end = math.atan2(end[1] - center[1], end[0] - center[0])

	# 角度の差分を計算
	angle_diff = angle_end - angle_start
	if angle_diff <= 0:
		angle_diff += 2 * math.pi

	# 頂点リストを作成
	vertices = []
	for segment in range(segments + 1):
		angle = angle_start + (angle_diff / segments) * segment
		x = center[0] + math.cos(angle) * radius
		y = center[1] + math.sin(angle) * radius
		vertices.append((x, y, center[2]))

	return vertices








# 親となるメニュー
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = 'ROMLYADDON_MT_romly_add_mesh_menu_parent'
	bl_label = 'Romly'
	bl_description = 'Romly Addon Menu'



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_reuleaux_polygon.bl_idname, text=bpy.app.translations.pgettext_iface('Add Reuleaux Polygon'), icon='MESH_CIRCLE')





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_reuleaux_polygon,
	ROMLYADDON_MT_romly_add_mesh_menu_parent,
]





def register():
	# クラスと翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.append(menu_func)





def unregister():
	# クラスと翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
