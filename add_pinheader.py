import bpy
import mathutils
import bmesh
from bpy.props import *





def create_object(vertices: list, faces: list, name: str = '', mesh_name=None):
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





def create_box(size: mathutils.Vector, offset: mathutils.Vector):
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
	return cleanup_mesh(create_object(vertices=actual_vertices, faces=faces))





def create_combined_object(objects, obj_name: str, mesh_name: str = None):
	"""
	2つのオブジェクトを統合する。

	Parameters
	----------
	objects : list
		結合するオブジェクトのリスト。先頭のオブジェクトの位置が維持される。
	obj_name : str
		生成するメッシュにつける名前。
	mesh_name : str
		生成するメッシュにつける名前。
	"""
	vertices = []
	faces = []
	vertexIndexOffset = 0
	for obj in objects:
		for v in obj.data.vertices:
			vertices.append(obj.location + v.co - objects[0].location)
		for f in obj.data.polygons:
			faces.append([])
			for v in f.vertices:
				faces[len(faces) - 1].append(v + vertexIndexOffset)
		vertexIndexOffset += len(obj.data.vertices)

	if mesh_name is None:
		mesh_name = obj_name + '_mesh'
	mesh = bpy.data.meshes.new(mesh_name)
	mesh.from_pydata(vertices, [], faces)

	combinedObject = bpy.data.objects.new(obj_name, mesh)
	combinedObject.location = objects[0].location
	return combinedObject





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





PIN_PITCH_127 = '127'
PIN_PITCH_200 = '200'
PIN_PITCH_254 = '254'
PIN_PITCHES = [
	(PIN_PITCH_127, '1.27mm', ''),
	(PIN_PITCH_200, '2.00mm', ''),
	(PIN_PITCH_254, '2.54mm', '')
]

def pin_pitch_to_value(pin_pitch: str):
	if pin_pitch == PIN_PITCH_127:
		return 1.27
	elif pin_pitch == PIN_PITCH_200:
		return 2.00
	else:
		return 2.54





class ROMLYADDON_OT_add_pinheader(bpy.types.Operator):
	bl_idname = "romlyaddon.add_pinheader"
	bl_label = "Add Pin Header"
	bl_description = 'ピンヘッダのメッシュを追加します'
	bl_options = {'REGISTER', 'UNDO'}



	def __init__(self):
		self.on_pitch_update(None)



	def on_pitch_update(self, context):
		if self.val_pitch == PIN_PITCH_127:
			self.val_block_size = mathutils.Vector([1.27, 2.1, 1.5])
			self.val_pin_thickness = 0.4
			self.val_pin_length_top = 3
			self.val_pin_length_bottom = 2.3
			self.val_block_concave_size = mathutils.Vector([0, 0, 0])
		elif self.val_pitch == PIN_PITCH_200:
			self.val_block_size = mathutils.Vector([2, 2, 2])
			self.val_pin_thickness = 0.5
			self.val_pin_length_top = 4
			self.val_pin_length_bottom = 2.8
			self.val_block_concave_size = mathutils.Vector([3, 1.4, 0.3])
		elif self.val_pitch == PIN_PITCH_254:
			self.val_block_size = mathutils.Vector([2.54, 2.5, 2.5])
			self.val_pin_thickness = 0.64
			self.val_pin_length_top = 6.1
			self.val_pin_length_bottom = 3
			self.val_block_concave_size = mathutils.Vector([3, 1.6, 0.4])



	# プロパティ
	val_pitch: EnumProperty(name='Pitch', description='ピッチ', default=PIN_PITCH_254, items=PIN_PITCHES, update=on_pitch_update)

	val_block_size: FloatVectorProperty(name='Block Size', size=3, min=0.1, soft_max=2.54, description='プラスチック部分のサイズ', subtype='TRANSLATION', unit='LENGTH')
	val_pin_thickness: FloatProperty(name='Pin Thickness', min=0.1, soft_max=1, description='ピンの太さ', unit='LENGTH')
	val_pin_length_top: FloatProperty(name='Pin Length (Top)', min=0.1, soft_max=10, description='ピンの長さ（上部）', unit='LENGTH')
	val_pin_length_bottom: FloatProperty(name='Pin Length (Bottom)', min=0.1, soft_max=10, description='ピンの長さ（下部）', unit='LENGTH')
	val_block_concave_size: FloatVectorProperty(name='Block Concave Size', size=3, min=0, soft_max=2, description='プラスチック部分の凹みのサイズ', subtype='TRANSLATION', unit='LENGTH')

	val_num_cols: IntProperty(name='Columns', description='ピン数', default=4, min=1, soft_max=20)
	val_num_rows: IntProperty(name='Rows', description='行数', default=1, min=1, soft_max=3)
	val_size: FloatVectorProperty(name='Size', description='大きさ', default=[10, 10, 10], soft_min=-1000.0, soft_max=1000.0, size=3, subtype='TRANSLATION', unit='LENGTH')






	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col.label(text="Pitch")
		row = col.row(align=True)
		row.prop(self, 'val_pitch', expand=True)
		row = col.row(align=True)
		row.prop(self, 'val_block_size')
		row = col.row(align=True)
		row.prop(self, 'val_pin_thickness')
		row = col.row(align=True)
		row.prop(self, 'val_pin_length_top')
		row = col.row(align=True)
		row.prop(self, 'val_pin_length_bottom')
		col.separator()

		col.prop(self, 'val_block_concave_size')
		col.separator()

		col.label(text="Pins")
		col.prop(self, 'val_num_cols')
		col.prop(self, 'val_num_rows')
		col.separator()

		col.prop(self, 'val_size')
		col.separator()


	def execute(self, context):
		# ピンヘッダのプラスチック部分のサイズ
		pin_pitch = pin_pitch_to_value(self.val_pitch)

		# ----------------------------------------
		# プラスチック部分の作成

		# 設定に従った頂点を生成
		obj_plastic = create_box(size=self.val_block_size, offset=mathutils.Vector([0, 0, self.val_block_size[2] / 2]))

		# BMeshオブジェクトを生成
		mesh = bmesh.new()
		mesh.from_mesh(obj_plastic.data)

		# Bevel Weight のカスタムデータレイヤーを取得。存在しない場合は作成される。
		bevel_weight_layer = mesh.edges.layers.bevel_weight.verify()

		for edge in mesh.edges:
			# Z方向に伸びる辺にベベルウェイトを設定
			if edge.verts[0].co[2] != edge.verts[1].co[2]:
				edge[bevel_weight_layer] = 1.0
		mesh.to_mesh(obj_plastic.data)
		mesh.free()

		# ベベルモディファイアを追加、適用
		bevel_modifier = obj_plastic.modifiers.new(name='Bevel', type='BEVEL')
		bevel_modifier.offset_type = 'OFFSET'
		bevel_modifier.use_clamp_overlap = True
		bevel_modifier.limit_method = 'WEIGHT'
		bevel_modifier.width = self.val_block_size[1] * 0.15
		bevel_modifier.segments = 1
		bevel_modifier.profile = 0.5
		bpy.ops.object.modifier_apply({'object': obj_plastic}, modifier=bevel_modifier.name)

		# ----------------------------------------
		# プラスチックの下部を削る

		if self.val_block_concave_size[0] > 0 and self.val_block_concave_size[1] > 0 and self.val_block_concave_size[2] > 0:
			# ブーリアン処理のため一旦リンクする必要がある
			bpy.context.collection.objects.link(obj_plastic)

			obj_plastic_concave = create_box(size=self.val_block_concave_size, offset=mathutils.Vector([0, 0, self.val_block_concave_size[2] / 2]))
			bpy.context.collection.objects.link(obj_plastic_concave)
			boolean_modifier = obj_plastic.modifiers.new(type='BOOLEAN', name='bool')
			boolean_modifier.object = obj_plastic_concave
			boolean_modifier.operation = 'DIFFERENCE'
			bpy.ops.object.modifier_apply({'object': obj_plastic}, modifier=boolean_modifier.name)

			# リンク解除
			bpy.context.collection.objects.unlink(obj_plastic)
			bpy.context.collection.objects.unlink(obj_plastic_concave)

		# ----------------------------------------
		# ピン部分の作成

		pin_length = self.val_pin_length_top + self.val_block_size[2] + self.val_pin_length_bottom
		pin_scale = mathutils.Vector([self.val_pin_thickness, self.val_pin_thickness, pin_length])
		obj_pin = create_box(size=pin_scale, offset=mathutils.Vector([0, 0, pin_length / 2 - self.val_pin_length_bottom]))

		# BMeshオブジェクトを生成
		mesh = bmesh.new()
		mesh.from_mesh(obj_pin.data)

		# Bevel Weight のカスタムデータレイヤーを取得。存在しない場合は作成される。
		bevel_weight_layer = mesh.edges.layers.bevel_weight.verify()

		for edge in mesh.edges:
			# Z方向がゼロの辺にベベルウェイトを設定
			if edge.verts[0].co[2] == edge.verts[1].co[2]:
				edge[bevel_weight_layer] = 1.0
		mesh.to_mesh(obj_pin.data)
		mesh.free()

		# ベベルモディファイアを追加、適用
		bevel_modifier = obj_pin.modifiers.new(name='Bevel', type='BEVEL')
		bevel_modifier.offset_type = 'OFFSET'
		bevel_modifier.use_clamp_overlap = True
		bevel_modifier.limit_method = 'WEIGHT'
		bevel_modifier.width = self.val_pin_thickness * 0.3
		bevel_modifier.segments = 1
		bevel_modifier.profile = 0.5
		bpy.ops.object.modifier_apply({'object': obj_pin}, modifier=bevel_modifier.name)

		# ----------------------------------------
		# プラスチック部分とピン部分の結合、配列作成

		obj = create_combined_object(objects=(obj_plastic, obj_pin), obj_name=f"Pin Header {pin_pitch}mm {self.val_num_rows}x{self.val_num_cols}")
		bpy.context.collection.objects.link(obj)

		# 配列を追加

		# Arrayモデファイアを追加
		array_modifier = obj.modifiers.new(name='Pin Header Columns', type='ARRAY')
		array_modifier.count = self.val_num_cols
		array_modifier.use_relative_offset = False
		array_modifier.use_constant_offset = True
		array_modifier.constant_offset_displace = mathutils.Vector([pin_pitch, 0, 0])
		array_modifier.use_merge_vertices = False	# 隣接する頂点をマージしない

		# Arrayモデファイアのパラメータを設定
		array_modifier_rows = obj.modifiers.new(name='Pin Header Rows', type='ARRAY')
		array_modifier_rows.count = self.val_num_rows
		array_modifier_rows.use_relative_offset = False
		array_modifier_rows.use_constant_offset = True
		array_modifier_rows.constant_offset_displace = mathutils.Vector([0, pin_pitch, 0])
		array_modifier_rows.use_merge_vertices = False	# 隣接する頂点をマージしない

		# ----------------------------------------

		# オブジェクトを3Dカーソル位置へ移動
		obj.location = bpy.context.scene.cursor.location

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}





# 親となるメニュー
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_pinheader.bl_idname, icon='EMPTY_SINGLE_ARROW')





# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





# blenderへのクラス登録処理
def register():
	bpy.utils.register_class(ROMLYADDON_OT_add_pinheader)
	bpy.utils.register_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	bpy.utils.unregister_class(ROMLYADDON_OT_add_pinheader)
	bpy.utils.unregister_class(ROMLYADDON_MT_romly_add_mesh_menu_parent)
	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == "__main__":
	register()
