import bpy
import math
import mathutils
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple



from . import romly_utils










# 定数的な...
AXIS_X = 'X'
AXIS_Y = 'Y'
AXIS_Z = 'Z'










def create_panhead(diameter: float, height: float, segments: int, r_segments: int) -> bpy.types.Object:
	"""
	なべネジの頭を作成する。

	Parameters
	----------
	diameter : float
		頭部の直径。
	height : float
		頭部の高さ。
	segments : int
		円周方向のセグメント数。
	r_segments : int
		丸みのセグメント数。

	Returns
	-------
	bpy.types.Object
		作成されたなべネジ頭のBlenderオブジェクト。

	Notes
	-----
	断面図の頂点群を作って回転体として作成する。
	"""
	vertices = []
	faces = []

	# 上部と下部それぞれのアールの半径
	top_r = height / 4 * 3
	bottom_r = height / 6

	# 回転体の元となる断面を作成
	vertices.append(Vector((0, 0, 0)))

	if r_segments > 0:
		# 下部のアール
		vertices.extend(romly_utils.make_arc_vertices(
			start=Vector((-diameter / 2 + bottom_r, 0, 0)),
			center=Vector((-diameter / 2 + bottom_r, 0, bottom_r)),
			axis=AXIS_Y, rotate_degrees=90, segments=r_segments))

		# 上部のアール
		vertices.extend(romly_utils.make_arc_vertices(
			start=Vector((-diameter / 2, 0, height - top_r)),
			center=Vector((-diameter / 2 + top_r, 0, height - top_r)),
			axis=AXIS_Y, rotate_degrees=90, segments=r_segments))
	else:
		vertices.append(Vector((-diameter / 2, 0, 0)))
		vertices.append(Vector((-diameter / 2, 0, height)))

	vertices.append(Vector((0, 0, height)))

	# 回転させて立体に
	romly_utils.add_revolved_surface(vertices=vertices, faces=faces, rotation_vertex_count=len(vertices), segments=segments)

	obj = romly_utils.create_object(vertices=vertices, faces=faces, name='Pan Head')
	romly_utils.cleanup_mesh(object=obj)
	return obj










def create_flathead(diameter: float, edge_thickness: float, segments: int, r_segments: int) -> bpy.types.Object:
	"""
	皿ネジの頭部のオブジェクトを作成する。

	Parameters
	----------
	diameter : float
		頭部の直径。
	edge_thickness : float
		頭部の縁の幅。
	segments : int
		円周方向のセグメント数。
	r_segments : int
		丸みのセグメント数。

	Returns
	-------
	bpy.types.Object
		作成された皿ネジ頭のBlenderオブジェクト。

	Notes
	-----
	断面図の頂点群を作って回転体として作成する。
	"""
	vertices = []
	faces = []

	# 回転体の元となる断面を作成
	# 皿ネジの角度は45度なので計算しやすいなー
	if edge_thickness > 0:
		bevel_r = edge_thickness * 0.3
		vertices.append(mathutils.Vector([-diameter / 2 + bevel_r, 0, 0]))
		for i in range(r_segments):
			v = romly_utils.rotated_vector(vector=mathutils.Vector([0, 0, bevel_r]), angle_radians=math.radians(-90.0 / r_segments * i), axis=AXIS_Y)
			v.x += -diameter / 2 + bevel_r
			v.z += -bevel_r
			vertices.append(v)
		vertices.append(mathutils.Vector([-diameter / 2, 0, -edge_thickness]))
	else:
		vertices.append(mathutils.Vector([-diameter / 2, 0, 0]))
	vertices.append(mathutils.Vector([0, 0, -diameter / 2 - edge_thickness]))

	# 回転させて立体に
	rotation_vertex_count = len(vertices)
	romly_utils.add_revolved_surface(vertices=vertices, faces=faces, rotation_vertex_count=rotation_vertex_count, segments=segments)

	# 蓋となる面
	faces.append(range(0, rotation_vertex_count * segments, rotation_vertex_count))

	obj = romly_utils.create_object(vertices=vertices, faces=faces, name='Flat Head')
	romly_utils.cleanup_mesh(object=obj)
	return obj










def create_phillips_shape(diameter: float, depth: float) -> bpy.types.Object:
	"""
	ドライバーの十字穴の形状のオブジェクト（ブーリアンモデファイア用）を作成する。

	Parameters
	----------
	diameter : float
		ネジ頭部の直径。この値から適当に十字の幅を算出する。
	depth : float
		穴の深さを指定。
	"""
	vertices = []
	faces = []

	# 十字の線の幅の規格がよくわからないので半径*0.16とする
	width = diameter * 0.16

	# 十字の縦棒の左上から反時計回り
	vertices.append(mathutils.Vector([-width / 2, diameter / 2, -depth]))
	vertices.append(mathutils.Vector([-width / 2, width / 2, -depth]))
	vertices.append(mathutils.Vector([-diameter / 2, width / 2, -depth]))
	vertices.append(mathutils.Vector([-diameter / 2, -width / 2, -depth]))
	vertices.append(mathutils.Vector([-width / 2, -width / 2, -depth]))
	vertices.append(mathutils.Vector([-width / 2, -diameter / 2, -depth]))

	vertices.append(mathutils.Vector([width / 2, -diameter / 2, -depth]))
	vertices.append(mathutils.Vector([width / 2, -width / 2, -depth]))
	vertices.append(mathutils.Vector([diameter / 2, -width / 2, -depth]))
	vertices.append(mathutils.Vector([diameter / 2, width / 2, -depth]))
	vertices.append(mathutils.Vector([width / 2, width / 2, -depth]))
	vertices.append(mathutils.Vector([width / 2, diameter / 2, -depth]))

	n = len(vertices)
	faces.append(list(range(n)))

	# 掃引
	romly_utils.extrude_face(vertices=vertices, faces=faces, extrude_vertex_indices=faces[0], z_offset=depth)

	# ドライバー先端の規定角度26.5度に従って十字上部のみ大きくする
	t = math.tan(math.radians(26.5))
	scale = (1.0 - t) / 1.0
	for i in range(n):
		vertices[i].x *= scale;
		vertices[i].y *= scale;


	obj = romly_utils.create_object(vertices=vertices, faces=faces, name='Phillips')
	romly_utils.cleanup_mesh(object=obj)
	return obj










def make_hexagon_beveled_vertices(radius: float, bevel_radius: float, bevel_segments: int) -> list[Vector]:
	"""六角形（ナット）の頂点一箇所分の断面図をベベルありで作った時の頂点群（回転体の元）を作成する。"""
	# 六角形の頂点
	hexagon_pt = Vector((0, radius, 0))

	# アールの開始位置
	bevel_start = romly_utils.rotated_vector(vector=Vector((0, -1, 0)) * bevel_radius, angle_radians=math.radians(60.0), axis=AXIS_Z)
	bevel_start.y += hexagon_pt.y

	# アールの開始位置から適当に伸ばした垂線
	bevel_perpendicular_pt = romly_utils.rotated_vector(vector=Vector((0, -1, 0)) * radius * 10, angle_radians=math.radians(-30.0), axis=AXIS_Z)
	bevel_perpendicular_pt += bevel_start

	# アール（ベベル）の中心を求める
	bevel_center = romly_utils.find_intersection(
		line1_start=romly_utils.project_to_xy(bevel_start), line1_end=romly_utils.project_to_xy(bevel_perpendicular_pt),
		line2_start=romly_utils.project_to_xy(hexagon_pt), line2_end=Vector((0, 0, 0)))

	# 円弧を構成する頂点郡を返す
	return romly_utils.make_arc_vertices(start=bevel_start, center=bevel_center, axis=AXIS_Z, rotate_degrees=60, segments=bevel_segments)










def create_nut(diameter: float, thickness: float, bevel_segments: int) -> bpy.types.Object:
	"""穴の空いていないナット状のオブジェクトを生成する

	Parameters
	----------
	diameter : float
		[description]
	thickness : float
		ナットの厚み（高さ）。
	bevel_segments : Float
		六角形の角のアールのセグメント数。0の場合はベベルなしとなる。
	"""
	vertices = []
	faces = []

	# 六角形を作る
	if bevel_segments > 0:
		# 六角形の角のベベルの半径を適当に決める。直径の1/40
		bevel_radius = diameter / 40

		for i in range(6):
			temp_vertices = make_hexagon_beveled_vertices(radius=diameter / 2, bevel_radius=bevel_radius, bevel_segments=bevel_segments)
			romly_utils.rotate_vertices(object=temp_vertices, degrees=60 * i, axis=AXIS_Z)
			vertices.extend(temp_vertices)
	else:
		hexagon_vertices = romly_utils.make_arc_vertices(start=mathutils.Vector([0, diameter / 2, 0]), center=mathutils.Vector([0, 0, 0]), axis=AXIS_Z, rotate_degrees=360, segments=6)
		del hexagon_vertices[-1]	# 最後の頂点は最初の頂点と同じ位置になるので削除
		vertices.extend(hexagon_vertices)

	# 面を貼る
	faces.append(list(range(len(vertices))))

	# 掃引
	romly_utils.extrude_face(vertices=vertices, faces=faces, extrude_vertex_indices=faces[0], z_offset=-thickness)

	obj = romly_utils.create_object(vertices=vertices, faces=faces, name='Nut')
	romly_utils.cleanup_mesh(object=obj)
	return obj










def create_nut_chamfering_object(diameter: float, segments: int, z: float, bottom: bool) -> bpy.types.Object:
	"""
	ナットの面取り用のオブジェクトを生成する

	Parameters
	----------
	z : float
		面取りを開始する高さ。
	bottom : bool
		Trueの場合は下部の面取り用オブジェクトを作成する。
	"""
	vertices = []
	faces = []

	# 六角形の内接円の半径
	in_circle_radius = math.sqrt(3) / 2 * (diameter / 2)

	contact = mathutils.Vector([-in_circle_radius, 0, z])

	v1 = mathutils.Vector([-in_circle_radius, 0, 0])
	if bottom:
		v1.rotate(mathutils.Matrix.Rotation(math.radians(30), 4, AXIS_Y))
	else:
		v1.rotate(mathutils.Matrix.Rotation(math.radians(-30), 4, AXIS_Y))
	v2 = romly_utils.rotated_vector(vector=v1, angle_radians=math.radians(180), axis=AXIS_Y)
	v1 += contact
	v2 += contact
	vertices.append(v1)
	vertices.append(mathutils.Vector([v1.x, 0, v2.z]))
	vertices.append(v2)

	romly_utils.add_revolved_surface(vertices=vertices, faces=faces, rotation_vertex_count=3, segments=segments, close=True)

	obj = romly_utils.create_object(vertices=vertices, faces=faces, name='Nut Chamfering')
	romly_utils.cleanup_mesh(object=obj)
	return obj










def create_screw_shaft(length: float, unthreaded_length: float, diameter: float, pitch: float, lead: int, thread_depth: float, top_extra_cut: float, segments: int, thread_bevel_segments: int) -> bpy.types.Object:
	"""
	指定されたパラメータに基づいて、ねじ切り部分とねじ切りのない部分を含むネジのシャフトを生成する。

	Parameters
	----------
	length : float
		ネジ全体の長さ。
	unthreaded_length : float
		ねじ切りのない部分の長さ。
	diameter : float
		ネジの直径。
	pitch : float
		ネジのピッチ（ねじ山間の距離）。
	lead : int
		ネジのリード（一回転で進む距離）。ピッチの倍数で指定。
	thread_depth : float
		ねじ山の深さ。
	top_extra_cut : float
		上部を削る場合は削る長さを指定（皿ネジ用）。
	segments : int
		円筒のセグメント数。
	thread_bevel_segments : int
		ねじ切り部分のベベルセグメント数。

	Returns
	-------
	bpy.types.Object
		生成されたネジの芯のオブジェクト。
	"""

	thread_length = max(0, length - unthreaded_length)

	objects = []

	# ねじ切り部分のオブジェクトを生成
	if thread_length > 0:
		obj = romly_utils.create_threaded_cylinder(diameter=diameter, length=thread_length,
			pitch=pitch, lead=lead, thread_depth=thread_depth,
			segments=segments, bevel_segments=thread_bevel_segments)

		# モデファイアを使って上部をカットする
		# この時、ネジの座標がぴったり0だとブーリアンできないので、ごく僅かにずらす
		# blenderが2.8になってブーリアンのメソッドが選択できなくなった結果、回転も加えないといけなくなった。
		tool_obj_size = 100
		romly_utils.translate_vertices(obj, [0, 0, 0.001])
		bpy.ops.mesh.primitive_cube_add(size=tool_obj_size, enter_editmode=False, location=(0, 0, tool_obj_size / 2), rotation=(0, 0, 30))
		bool_tool_obj = bpy.data.objects[bpy.context.active_object.name]

		# 高速ソルバーにしないとピッチの値によっては正しくカットされない事があるので
		romly_utils.apply_boolean_object(object=obj, boolObject=bool_tool_obj, unlink=True, fast_solver=True)

		# 同様に下部をカット
		bpy.ops.mesh.primitive_cube_add(size=100, enter_editmode=False, location=(0, 0, -thread_length - 50), rotation=(0, 0, 30))
		bool_tool_obj = bpy.data.objects[bpy.context.active_object.name]
		romly_utils.apply_boolean_object(object=obj, boolObject=bool_tool_obj, unlink=True, fast_solver=True)

		# ねじ切りのない部分の長さだけ下に移動
		if unthreaded_length > 0:
			romly_utils.translate_vertices(object=obj, vector=mathutils.Vector([0, 0, -unthreaded_length]))

		objects.append(obj)
		bpy.context.collection.objects.unlink(obj)

	# ねじ切りのない部分の円筒
	if unthreaded_length > 0:
		bpy.ops.mesh.primitive_cylinder_add(vertices=segments, radius=diameter / 2, depth=unthreaded_length, end_fill_type='NGON', enter_editmode=False, location=(0, 0, 0))
		cylinderObject = bpy.data.objects[bpy.context.active_object.name]
		romly_utils.translate_vertices(object=cylinderObject, vector=mathutils.Vector([0, 0, -unthreaded_length / 2]))
		objects.append(cylinderObject)
		bpy.context.collection.objects.unlink(cylinderObject)

	# ねじ切り部分とねじ切りのない部分を結合
	obj = romly_utils.create_combined_object(objects, obj_name='shaft')
	bpy.context.collection.objects.link(obj)

	# 皿ネジの場合は十字の深さだけくなる
	if top_extra_cut > 0:
		tool_obj_size=100
		bpy.ops.mesh.primitive_cube_add(size=tool_obj_size, enter_editmode=False, location=(0, 0, tool_obj_size / 2 - top_extra_cut), rotation=(0, 0, 30))
		bool_tool_obj = bpy.data.objects[bpy.context.active_object.name]
		romly_utils.apply_boolean_object(object=obj, boolObject=bool_tool_obj, unlink=True, fast_solver=True)

	bpy.context.collection.objects.unlink(obj)
	return obj










def calc_unthreaded_length(length: float, diameter: float) -> float:
	"""
	ネジの長さから、半ねじのねじ切りされていない部分の長さを算出する。

	Parameters
	----------
	length : float
		ネジ全体の（頭を含まない）長さ。
	diameter : float
		ネジの経。

	Returns
	-------
	float
		半ねじのねじ切りされていない部分の長さ。
	"""
	if length <= 129:
		thread_length = diameter * 2 + 6
	elif length <= 219:
		thread_length = diameter * 2 + 12
	else:
		thread_length = diameter * 2 + 25

	if thread_length <= length:
		return length - thread_length
	else:
		return length










def update_properties(self, context):
	"""プロパティのパネルでM2〜M8などのボタンを押した時の処理。プロパティの値を押したボタンに合わせてセットする。"""

	# 指定されたスクリューサイズに基づいて直径とピッチを設定
	spec = romly_utils.SCREW_SPECS.get(self.val_ms)
	if spec:
		self.val_diameter, self.val_pitch = spec.diameter, spec.pitch
		self.val_lead = 1
		self.val_thread_depth = spec.thread_depth()

	if hasattr(self, 'val_head_diameter'):
		if spec:
			self.val_head_diameter = spec.head_diameter
			self.val_panhead_height = spec.panhead_height
			self.val_phillips_size = spec.phillips_size
			self.val_phillips_depth = spec.phillips_depth
			# 皿ネジ頭部径
			self.val_flatHeadDiameter = spec.flathead_diameter
			self.val_flathead_edge_thickness = spec.flathead_edge_thickness
			# 六角ボルト
			self.val_boltHeadDiameter = spec.bolthead_diameter()
			self.val_boltHeadHeight = spec.bolthead_height

	# ナットの場合の設定
	if hasattr(self, 'val_nutHeight'):
		if spec:
			self.val_nutDiameter = spec.bolthead_diameter()
			self.val_nutHeight = spec.nut_height_thin if self.val_nut_type_number == '3' else spec.nut_height

		if self.val_nut_type_number == '1':
			self.val_topChamfering = False
			self.val_bottomChamfering = True
		elif self.val_nut_type_number == '2':
			self.val_topChamfering = True
			self.val_bottomChamfering = True
		else:
			self.val_topChamfering = True
			self.val_bottomChamfering = True

	if hasattr(self, 'val_length'):
		if self.val_lengths.startswith('l') and self.val_lengths[1:].isdigit():
			self.val_length = int(self.val_lengths[1:])






M_ITEMS = [
	('m2', 'M2', 'Set specs to M2 size'),
	('m2_5', 'M2.5', 'Set specs to M2.5 size'),
	('m3', 'M3', 'Set specs to M3 size'),
	('m4', 'M4', 'Set specs to M4 size'),
	('m5', 'M5', 'Set specs to M5 size'),
	('m6', 'M6', 'Set specs to M6 size'),
	('m8', 'M8', 'Set specs to M8 size'),
]

# デフォルトのサイズ。ネジとナットで共通
DEFAULT_SIZE = 'm3'





# MARK: Class
class ROMLYADDON_OT_add_jis_screw(bpy.types.Operator):
	bl_idname = 'romlyaddon.add_jis_screw'
	bl_label = bpy.app.translations.pgettext_iface('Add JIS Screw')
	bl_description = 'Cunstruct a JIS standard screw'
	bl_options = {'REGISTER', 'UNDO'}

	# ネジ頭のリスト
	SCREW_HEAD_SHAPE_NONE = 'none'
	SCREW_HEAD_SHAPE_PAN = 'pan'
	SCREW_HEAD_SHAPE_FLAT = 'flat'
	SCREW_HEAD_SHAPE_BOLT = 'bolt'
	HeadShape = [
		(SCREW_HEAD_SHAPE_NONE, 'None', 'No Screw Head'),
		(SCREW_HEAD_SHAPE_PAN, 'Pan Head', 'Pan Head Screw'),
		(SCREW_HEAD_SHAPE_FLAT, 'Flat Head', 'Flat Head Screw'),
		(SCREW_HEAD_SHAPE_BOLT, 'Hexagon Head', 'Hexagon Head Screw')
	]

	LENGTH_ITEMS = [
		('l4', '4㎜', 'Set length to 4mm'),
		('l6', '6㎜', 'Set length to 6mm'),
		('l8', '8㎜', 'Set length to 8mm'),
		('l10', '10㎜', 'Set length to 10mm'),
		('l15', '15㎜', 'Set length to 15mm'),
		('l20', '20㎜', 'Set length to 20mm'),
		('l25', '25㎜', 'Set length to 25mm'),
	]

	# 半ねじ設定
	SCREW_THREAD_TYPE_ALLTHREAD = 'all thread'
	SCREW_THREAD_TYPE_HALFTHREAD = 'half thread'
	SCREW_THREAD_TYPE_HALFTHREAD_MANUAL = 'half thread manual'
	SCREW_THREAD_TYPE = [
		(SCREW_THREAD_TYPE_ALLTHREAD, 'Fully Threaded', 'Fully Threaded'),
		(SCREW_THREAD_TYPE_HALFTHREAD, 'Partially Threaded', 'Partially Threaded'),
		(SCREW_THREAD_TYPE_HALFTHREAD_MANUAL, 'Specify Length', 'Partially Threaded (Specify Length)')
	]

	SCREW_DIRECTIONS = [
		('z', 'Z', "It's a screw towards Z minus direction"),
		('-z', '-Z', "It's a screw towards Z plus direction"),
		('x', 'X', "It's a screw towards X plus direction"),
		('-x', '-X', "It's a screw towards X minus direction"),
		('y', 'Y', "It's a screw towards Y plus direction"),
		('-y', '-Y', "It's a screw towards Y minus direction")
	]

	val_ms: EnumProperty(name='sizes', items=M_ITEMS, default=DEFAULT_SIZE, update=update_properties)

	val_head_shape: EnumProperty(name='Head Shape', items=HeadShape, default=SCREW_HEAD_SHAPE_PAN)

	# なべネジのサイズ
	val_head_diameter: FloatProperty(name='Head Diameter', description='Head Diameter', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].head_diameter, min=1, max=55, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_panhead_height: FloatProperty(name='Head Height', description='Head Height', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].panhead_height, min=0.1, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# 皿ネジのサイズ
	val_flatHeadDiameter: FloatProperty(name='Flat Head Diameter', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].flathead_diameter, min=1, max=55, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_flathead_edge_thickness: FloatProperty(name='Thickness of Flat Head Screw Edge', description='Thickness of Flat Head Screw Edge', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].flathead_edge_thickness, min=0, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# 六角ボルトのサイズ
	val_boltHeadDiameter: FloatProperty(name='Head Diameter', description="Hexagon head's diagonal length", default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].bolthead_diameter(), min=1, max=55, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_boltHeadHeight: FloatProperty(name='Head Height', description='Head Height', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].bolthead_height, min=0.1, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# 十字穴のサイズ
	val_phillips_size: FloatProperty(name='Phillips Width', description='Phillips Width', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].phillips_size, min=0, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_phillips_depth: FloatProperty(name='Phillips Slit Depth', description='Phillips Slit Depth', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].phillips_depth, min=0, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_phillips_rotation: FloatProperty(name='Phillips Rotation', description='Phillips Rotation', min=0, max=math.pi / 2, default=math.pi / 4, subtype='ANGLE', unit='ROTATION')

	val_diameter: FloatProperty(name='Shaft Diameter', description='Shaft Diameter', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].diameter, min=1, max=55, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# ネジの長さ
	val_lengths: EnumProperty(name='Lengths', items=LENGTH_ITEMS, default='l10', update=update_properties)
	val_length: FloatProperty(name='Length', description='Screw Length', default=10.0, min=0, max=300, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# ねじ切りのサイズ設定
	val_pitch: FloatProperty(name='Pitch', description='The distance between two adjacent threads', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].pitch, min=0.25, max=5, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_lead: IntProperty(name='Thread Lead', description='How many times the pitch distance does the screw advance when turned once', min=1, max=10, default=1)
	val_thread_depth: FloatProperty(name='Thread Depth', description='The depth of each thread', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].thread_depth(), min=0.1, soft_max=5, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH, precision=4)

	# 半ねじ設定
	val_thread_type: EnumProperty(name='Thread Type', items=SCREW_THREAD_TYPE, update=update_properties)
	val_unthreaded_length: FloatProperty(name='Unthreaded Length', description='Unthreaded Length', default=0.0, min=0, max=300, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# メッシュ設定
	val_direction: EnumProperty(name='Direction', description='The direction of the screw', default='z', items=SCREW_DIRECTIONS)
	val_segments: IntProperty(name='Segments', default=32, min=3, max=128, subtype='NONE')
	val_head_bevel_segments: IntProperty(name='Head Bevel Segments', default=10, min=0, max=32, subtype='NONE')
	val_thread_bevel_segments: IntProperty(name='Thread Bevel Segments', default=5, min=0, max=16, subtype='NONE')
	val_chamferingSegments: IntProperty(name='Chamfering Segments of Hexagon Head', default=48, min=3, max=128, subtype='NONE')



	def base_object_name(self) -> str:
		"""作成するオブジェクトに付ける名前を取得する。"""
		name = ''
		if self.val_head_shape == self.SCREW_HEAD_SHAPE_PAN:
			name = 'Pan Head Screw'
		elif self.val_head_shape == self.SCREW_HEAD_SHAPE_FLAT:
			name = 'Flat Head Screw'
		elif self.val_head_shape == self.SCREW_HEAD_SHAPE_BOLT:
			name = 'Hexagon Head Screw'
		else:
			name = 'Screw'
		return bpy.app.translations.pgettext_data(name)



	def draw(self, context):
		col = self.layout.column()

		row = col.row(align=True)
		row.prop(self, 'val_ms', expand=True)
		col.separator()

		col.prop(self, 'val_diameter')
		col.separator()

		col.label(text='Head Shape')
		row = col.row(align=True)
		row.prop(self, 'val_head_shape', expand=True)
		headShapeColumn = col.column()
		if self.val_head_shape == self.SCREW_HEAD_SHAPE_PAN:
			headShapeColumn.prop(self, 'val_head_diameter')
			headShapeColumn.prop(self, 'val_panhead_height')
		elif self.val_head_shape == self.SCREW_HEAD_SHAPE_FLAT:
			headShapeColumn.prop(self, 'val_flatHeadDiameter')
			headShapeColumn.prop(self, 'val_flathead_edge_thickness')
		elif self.val_head_shape == self.SCREW_HEAD_SHAPE_BOLT:
			headShapeColumn.prop(self, 'val_boltHeadDiameter')
			headShapeColumn.prop(self, 'val_boltHeadHeight')
		headShapeColumn.enabled = self.val_head_shape != self.SCREW_HEAD_SHAPE_NONE
		col.separator()

		col.label(text='Phillips Head Slit')
		col.prop(self, 'val_phillips_size')
		col.prop(self, 'val_phillips_depth')
		col.prop(self, 'val_phillips_rotation')
		col.separator()

		col.label(text='Length')
		row = col.row(align=True)
		row.prop(self, 'val_lengths', expand=True)
		col.prop(self, 'val_length')
		col.row(align=True).prop(self, 'val_thread_type', expand=True)
		if self.val_thread_type == self.SCREW_THREAD_TYPE_HALFTHREAD:
			row = col.row()
			row.alignment = 'RIGHT'
			row.label(text=f"{bpy.app.translations.pgettext_iface('The length of the unthreaded part')}: {romly_utils.units_to_string(value=self.val_unthreaded_length)}")
			row = col.row()
			row.alignment = 'RIGHT'
			row.label(text=f"{bpy.app.translations.pgettext_iface('The length of the threaded part')}: {romly_utils.units_to_string(value=self.val_length - self.val_unthreaded_length)}")

		elif self.val_thread_type == self.SCREW_THREAD_TYPE_HALFTHREAD_MANUAL:
			col.prop(self, 'val_unthreaded_length')
			row = col.row()
			row.alignment = 'RIGHT'
			row.label(text=f"{bpy.app.translations.pgettext_iface('The length of the threaded part')}: {romly_utils.units_to_string(value=self.val_length - self.val_unthreaded_length)}")
		col.separator()

		col.label(text='Threading')
		row = col.row(align=True)
		row.prop(self, 'val_pitch')
		row.prop(self, 'val_lead')
		col.prop(self, 'val_thread_depth')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_direction')
		col.prop(self, 'val_segments')
		if self.val_head_shape != self.SCREW_HEAD_SHAPE_NONE:
			col.prop(self, 'val_head_bevel_segments')
		if self.val_head_shape == self.SCREW_HEAD_SHAPE_BOLT:
			col.prop(self, 'val_chamferingSegments')
		col.prop(self, 'val_thread_bevel_segments')



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		# 設定に従ってネジ切り無しとあり部分の長さを求める
		if self.val_thread_type == self.SCREW_THREAD_TYPE_ALLTHREAD:
			self.val_unthreaded_length = 0
		elif self.val_thread_type == self.SCREW_THREAD_TYPE_HALFTHREAD:
			self.val_unthreaded_length = calc_unthreaded_length(length=self.val_length, diameter=self.val_diameter)

		# 選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		objects = []

		# ねじ切り無しの長さの方が全体より長い場合はエラー
		if self.val_unthreaded_length > self.val_length:
			romly_utils.report(self, 'WARNING', msg_key='The length of the unthreaded part cannot be longer than the total length')
			return {'CANCELLED'}

		# ネジの芯の作成
		if self.val_length > 0:
			# 皿ネジの場合、十字穴の深さだけ芯の上部を削る
			top_extra_cut = self.val_phillips_depth if self.val_head_shape == self.SCREW_HEAD_SHAPE_FLAT else 0

			objects.append(create_screw_shaft(
				length=self.val_length,
				unthreaded_length=self.val_unthreaded_length,
				diameter=self.val_diameter,
				pitch=self.val_pitch,
				lead=self.val_lead,
				thread_depth=self.val_thread_depth,
				top_extra_cut=top_extra_cut,
				segments=self.val_segments,
				thread_bevel_segments=self.val_thread_bevel_segments))

		# 頭部の作成
		if self.val_head_shape != self.SCREW_HEAD_SHAPE_NONE and self.val_panhead_height > 0:
			if self.val_head_shape == self.SCREW_HEAD_SHAPE_FLAT:
				head = create_flathead(diameter=self.val_flatHeadDiameter, edge_thickness=self.val_flathead_edge_thickness, segments=self.val_segments, r_segments=self.val_head_bevel_segments)
				bpy.context.collection.objects.link(head)
			elif self.val_head_shape == self.SCREW_HEAD_SHAPE_BOLT:
				head = create_nut(diameter=self.val_boltHeadDiameter, thickness=self.val_boltHeadHeight, bevel_segments=self.val_head_bevel_segments)
				bpy.context.collection.objects.link(head)
				chamferingObject = create_nut_chamfering_object(diameter=self.val_boltHeadDiameter, segments=self.val_chamferingSegments, z=0, bottom=False)
				chamferingObject.location = mathutils.Vector([0, 0, 0.001])
				romly_utils.apply_boolean_object(object=head, boolObject=chamferingObject, unlink=False)
				head.location.z = self.val_boltHeadHeight
			else:
				head = create_panhead(diameter=self.val_head_diameter, height=self.val_panhead_height, segments=self.val_segments, r_segments=self.val_head_bevel_segments)
				bpy.context.collection.objects.link(head)

			# 十字穴
			if self.val_phillips_depth > 0:
				booleanOffset = 0.01
				phillips = create_phillips_shape(diameter=self.val_phillips_size, depth=self.val_phillips_depth + booleanOffset)
				if self.val_head_shape == self.SCREW_HEAD_SHAPE_PAN:
					phillips.location.z = self.val_panhead_height + booleanOffset
				elif self.val_head_shape == self.SCREW_HEAD_SHAPE_BOLT:
					phillips.location.z = self.val_boltHeadHeight + booleanOffset
				else:
					phillips.location.z = booleanOffset
				phillips.rotation_euler = [0, 0, self.val_phillips_rotation]
				bpy.context.collection.objects.link(phillips)
				romly_utils.apply_boolean_object(object=head, boolObject=phillips, unlink=True)

			bpy.context.collection.objects.unlink(head)
			objects.append(head)

		# 芯と頭部をひとつのオブジェクトに統合する
		if len(objects) > 0:
			obj = romly_utils.create_combined_object(objects=objects, obj_name=f"{self.base_object_name()} M{romly_utils.remove_decimal_trailing_zeros(self.val_diameter)}x{romly_utils.remove_decimal_trailing_zeros(self.val_length)}mm")
			bpy.context.collection.objects.link(obj)
			obj.select_set(state=True)

			# 回転
			if self.val_direction == '-z':
				romly_utils.rotate_vertices(object=obj, degrees=180, axis=AXIS_Y)
			elif self.val_direction == 'x':
				romly_utils.rotate_vertices(object=obj, degrees=-90, axis=AXIS_Y)
			elif self.val_direction == '-x':
				romly_utils.rotate_vertices(object=obj, degrees=90, axis=AXIS_Y)
			elif self.val_direction == 'y':
				romly_utils.rotate_vertices(object=obj, degrees=90, axis=AXIS_X)
			elif self.val_direction == '-y':
				romly_utils.rotate_vertices(object=obj, degrees=-90, axis=AXIS_X)

			# 3Dカーソルの位置へ
			obj.location = bpy.context.scene.cursor.location

			# アクティブオブジェクトに設定
			bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}










# MARK: Class
class ROMLYADDON_OT_add_jis_nut(bpy.types.Operator):
	bl_idname = 'romlyaddon.add_jis_nut'
	bl_label = bpy.app.translations.pgettext_iface('Add JIS Nut')
	bl_description = 'Cunstruct a JIS standard nut'
	bl_options = {'REGISTER', 'UNDO'}



	val_ms: EnumProperty(name='sizes', items=M_ITEMS, default='m3', update=update_properties)

	NUT_TYPE_NUMBERS = [
		('1', 'Type-1', 'The nut chamfered on one side only'),
		('2', 'Type-2', 'The nut chamfered on both side'),
		('3', 'Type-3', 'Thinner nut chamfered on both side'),
	]
	val_nut_type_number: EnumProperty(name='types', items=NUT_TYPE_NUMBERS, default='1', update=update_properties)

	val_nutDiameter: FloatProperty(name='Nut Diameter', description='Nut Diameter', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].bolthead_diameter(), min=0.1, max=55, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_diameter: FloatProperty(name='Hole Diameter', description='Hole Diameter', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].diameter, min=0, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_nutHeight: FloatProperty(name='Thickness', description='The thickness of the nut', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].nut_height, min=0.1, max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# ねじ切りのサイズ設定
	val_pitch: FloatProperty(name='Pitch', description='The distance between two adjacent threads', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].pitch, min=0.25, max=5, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_lead: IntProperty(name='Thread Lead', description='How many times the pitch distance does the screw advance when turned once', min=1, max=10, default=1)
	val_thread_depth: FloatProperty(name='Thread Depth', description='The depth of each thread', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].thread_depth(), min=0.1, soft_max=5, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH, precision=4)

	val_topChamfering: BoolProperty(name='Top Chamfering', description='Top Chamfering', default=False)
	val_bottomChamfering: BoolProperty(name='Bottom Chamfering', description='Bottom Chamfering', default=True)

	# メッシュ設定
	val_segments: IntProperty(name='Thread Segments', default=32, min=3, max=128, subtype='NONE')
	val_thread_bevel_segments: IntProperty(name='Thread Bevel Segments', default=5, min=0, max=16, subtype='NONE')
	val_chamferingSegments: IntProperty(name='Chamfering Segments', default=48, min=3, max=128, subtype='NONE')
	val_bevelSegments: IntProperty(name='Nut Corner Segments', default=5, min=0, max=16, subtype='NONE')



	def draw(self, context):
		col = self.layout.column()

		row = col.row(align=True)
		row.prop(self, 'val_nut_type_number', expand=True)
		col.separator()

		row = col.row(align=True)
		row.prop(self, 'val_ms', expand=True)

		col.prop(self, 'val_nutDiameter')
		col.prop(self, 'val_diameter')
		col.prop(self, 'val_nutHeight', text=romly_utils.translate('Thickness', 'IFACE'))	# 'Thickness'はBlender内部の辞書で『幅』に翻訳されてしまうので、自前で翻訳

		col.label(text='Threading')
		row = col.row(align=True)
		row.prop(self, 'val_pitch')
		row.prop(self, 'val_lead')
		col.prop(self, 'val_thread_depth')
		col.separator()

		row = col.row()
		row.label(text='Chamfering')
		row.prop(self, 'val_topChamfering', text='Top')
		row.prop(self, 'val_bottomChamfering', text='Bottom')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_segments')
		col.prop(self, 'val_thread_bevel_segments')
		col.prop(self, 'val_bevelSegments')
		col.prop(self, 'val_chamferingSegments')



	def invoke(self, context, event):
		return self.execute(context)



	def execute(self, context):
		# 穴の直径の方が大きい場合は警告してキャンセル
		if self.val_diameter >= self.val_nutDiameter:
			romly_utils.report(self, 'WARNING', msg_key='The nut hole diameter must be smaller than the diameter')
			return {'CANCELLED'}

		nutObject = create_nut(diameter=self.val_nutDiameter, thickness=self.val_nutHeight, bevel_segments=self.val_bevelSegments)
		bpy.context.collection.objects.link(nutObject)

		# ネジ切り
		if self.val_diameter > 0:
			threadObject = romly_utils.create_threaded_cylinder(diameter=self.val_diameter, length=self.val_nutHeight,
				pitch=self.val_pitch, lead=self.val_lead, thread_depth=self.val_thread_depth,
				segments=self.val_segments, bevel_segments=self.val_thread_bevel_segments)
			romly_utils.apply_boolean_object(object=nutObject, boolObject=threadObject)

		# 面取り（ブーリアンできない事があるので、ごく僅かにずらす）
		if self.val_topChamfering:
			chamferingObject = create_nut_chamfering_object(diameter=self.val_nutDiameter, segments=self.val_chamferingSegments, z=0, bottom=False)
			chamferingObject.location = mathutils.Vector([0, 0, 0.001])
			romly_utils.apply_boolean_object(object=nutObject, boolObject=chamferingObject, unlink=False)
		if self.val_bottomChamfering:
			chamferingObject = create_nut_chamfering_object(diameter=self.val_nutDiameter, segments=self.val_chamferingSegments, z=-self.val_nutHeight, bottom=True)
			chamferingObject.location = mathutils.Vector([0, 0, -0.001])
			romly_utils.apply_boolean_object(object=nutObject, boolObject=chamferingObject, unlink=False)

		# 3Dカーソルの位置へ
		nutObject.location = bpy.context.scene.cursor.location

		# 選択
		bpy.ops.object.select_all(action='DESELECT')
		nutObject.select_set(state=True)
		bpy.context.view_layer.objects.active = nutObject

		# 名前
		nutObject.name = f"{bpy.app.translations.pgettext_data('Nut')} M{romly_utils.remove_decimal_trailing_zeros(self.val_diameter)}"

		return {'FINISHED'}










# MARK: Menu
class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = "ROMLYADDON_MT_romly_add_mesh_menu_parent"
	bl_label = "Romly"
	bl_description = "Romly Addon Menu"



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_jis_screw.bl_idname, text=bpy.app.translations.pgettext_iface('Add JIS Screw'), icon='MOD_SCREW')
		layout.operator(ROMLYADDON_OT_add_jis_nut.bl_idname, text=bpy.app.translations.pgettext_iface('Add JIS Nut'), icon='SEQ_CHROMA_SCOPE')









# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_jis_screw,
	ROMLYADDON_OT_add_jis_nut,
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
