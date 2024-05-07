import bpy
import math
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple



from . import romly_utils










class LinearGuideRailSpec(NamedTuple):
	"""リニアガイドのレールの寸法を格納するタプル。

	Parameters
	----------
	weight : float
		1メートル当たりのkg単位の重量。メッシュの作成には使われず、表示されるだけ。
	"""
	Wr: float
	Hr: float
	outer_hole_diameter: float
	outer_hole_depth: float
	inner_hole_diameter: float
	hole_pitch: float
	weight: float



# リニアガイドレールの寸法
RAIL_SPECS = {
	'mgn05': LinearGuideRailSpec(Wr=5, Hr=3.6, outer_hole_diameter=3.6, outer_hole_depth=0.8, inner_hole_diameter=2.4, hole_pitch=15, weight=0.15),
	'mgn07': LinearGuideRailSpec(Wr=7, Hr=4.8, outer_hole_diameter=4.2, outer_hole_depth=2.3, inner_hole_diameter=2.4, hole_pitch=15, weight=0.22),
	'mgn09': LinearGuideRailSpec(Wr=9, Hr=6.5, outer_hole_diameter=6.0, outer_hole_depth=3.5, inner_hole_diameter=3.5, hole_pitch=20, weight=0.38),
	'mgn12': LinearGuideRailSpec(Wr=12, Hr=8, outer_hole_diameter=6.0, outer_hole_depth=4.5, inner_hole_diameter=3.5, hole_pitch=25, weight=0.65),
	'mgn15': LinearGuideRailSpec(Wr=15, Hr=10, outer_hole_diameter=6.0, outer_hole_depth=4.5, inner_hole_diameter=3.5, hole_pitch=40, weight=1.06),
	'mgw05': LinearGuideRailSpec(Wr=10, Hr=4, outer_hole_diameter=5.5, outer_hole_depth=1.6, inner_hole_diameter=3, hole_pitch=20, weight=0.34),
	'mgw07': LinearGuideRailSpec(Wr=14, Hr=5.2, outer_hole_diameter=6, outer_hole_depth=3.2, inner_hole_diameter=3.5, hole_pitch=30, weight=0.51),
	'mgw09': LinearGuideRailSpec(Wr=18, Hr=7, outer_hole_diameter=6, outer_hole_depth=4.5, inner_hole_diameter=3.5, hole_pitch=30, weight=0.91),
	'mgw12': LinearGuideRailSpec(Wr=24, Hr=8.5, outer_hole_diameter=8, outer_hole_depth=4.5, inner_hole_diameter=4.5, hole_pitch=40, weight=1.49),
	'mgw15': LinearGuideRailSpec(Wr=42, Hr=9.5, outer_hole_diameter=8, outer_hole_depth=4.5, inner_hole_diameter=4.5, hole_pitch=40, weight=2.86),
}



LINEAR_GUIDE_SIZE_ITEMS = [
	('mgn05', 'MGN5', 'Set specs to MGN05 size'),
	('mgn07', 'MGN7', 'Set specs to MGN07 size'),
	('mgn09', 'MGN9', 'Set specs to MGN09 size'),
	('mgn12', 'MGN12', 'Set specs to MGN12 size'),
	('mgn15', 'MGN15', 'Set specs to MGN15 size'),
	('mgw05', 'MGW5', 'Set specs to MGW05 size'),
	('mgw07', 'MGW7', 'Set specs to MGW07 size'),
	('mgw09', 'MGW9', 'Set specs to MGW09 size'),
	('mgw12', 'MGW12', 'Set specs to MGW12 size'),
	('mgw15', 'MGW15', 'Set specs to MGW15 size'),
]










class LinearGuideBlockSpec(NamedTuple):
	"""リニアガイドのブロックの寸法を格納するタプル。

	Attributes
	----------
	width : float
		ブロックの幅。X方向の大きさ。(W)
	length : float
		ブロックのレールと並行方向の長さ。Z方向の大きさ。(L)
	middle_part_length : float
		ブロックの中央部分のレールと並行方向の長さ。(L1)
	total_height : float
		ブロックの浮き上がり距離を含む高さ。実質的なブロックの高さはこの値 - H1となる。(H)
	height_1 : float
		レールの下端からブロックの下端までの距離。ブロックの浮き上がりの距離。(H1)
	block_side_width : float
		ブロックのレールの両脇の幅。(N)
	screw : str
		ネジ穴のサイズ。'm3'など。
	screw_depth : float
		ネジ穴の深さ。(l)
	screw_b : float
		ネジ穴のブロックの幅方向（X方向）の間隔。(B)
	screw_c : float
		ネジ穴のブロックの長さ方向（Z方向）の間隔。(C)
		0の場合、長さ方向には1列（2個）のネジしか作成されない。
	rail : str
		レールのサイズ。'mgn09'など。
	grease_hole_diameter : float
		エンドシール（赤いところ）のグリース穴の直径。(Gn)
	grease_hole_position : float
		エンドシールのグリース穴表面からのY軸方向距離。(H2)
	weight : float
		kg単位の重量。メッシュの作成には使われず、表示されるだけ。
	"""
	width: float
	length: float
	middle_part_length: float
	total_height: float
	height_1: float
	block_side_width: float
	screw: str
	screw_depth: float
	screw_b: float
	screw_c: float
	rail: str
	grease_hole_diameter: float
	grease_hole_position: float
	weight: float



# リニアガイドブロックの寸法
BLOCK_SPECS = {
	'mgn05c': LinearGuideBlockSpec(width=12, length=16, middle_part_length=9.6, total_height=6, height_1=1.5, block_side_width=3.5, screw='m2', screw_depth=1.5, screw_b=8, screw_c=0, rail='mgn05', grease_hole_diameter=0.8, grease_hole_position=1, weight=0.008),
	'mgn05h': LinearGuideBlockSpec(width=12, length=19, middle_part_length=12.6, total_height=6, height_1=1.5, block_side_width=3.5, screw='m2', screw_depth=1.5, screw_b=8, screw_c=0, rail='mgn05', grease_hole_diameter=0.8, grease_hole_position=1, weight=0.01),
	'mgn07c': LinearGuideBlockSpec(width=17, length=22.5, middle_part_length=13.5, total_height=8, height_1=1.5, block_side_width=5, screw='m2', screw_depth=2.5, screw_b=12, screw_c=8, rail='mgn07', grease_hole_diameter=1.2, grease_hole_position=1.5, weight=0.01),
	'mgn07h': LinearGuideBlockSpec(width=17, length=30.8, middle_part_length=21.8, total_height=8, height_1=1.5, block_side_width=5, screw='m2', screw_depth=2.5, screw_b=12, screw_c=13, rail='mgn07', grease_hole_diameter=1.2, grease_hole_position=1.5, weight=0.02),
	'mgn09c': LinearGuideBlockSpec(width=20, length=28.9, middle_part_length=18.9, total_height=10, height_1=2, block_side_width=5.5, screw='m3', screw_depth=3, screw_b=15, screw_c=10, rail='mgn09', grease_hole_diameter=1.4, grease_hole_position=1.8, weight=0.02),
	'mgn09h': LinearGuideBlockSpec(width=20, length=39.9, middle_part_length=29.9, total_height=10, height_1=2, block_side_width=5.5, screw='m3', screw_depth=3, screw_b=15, screw_c=16, rail='mgn09', grease_hole_diameter=1.4, grease_hole_position=1.8, weight=0.03),
	'mgn12c': LinearGuideBlockSpec(width=27, length=34.7, middle_part_length=21.7, total_height=13, height_1=3, block_side_width=7.5, screw='m3', screw_depth=3.5, screw_b=20, screw_c=15, rail='mgn12', grease_hole_diameter=2, grease_hole_position=2.5, weight=0.03),
	'mgn12h': LinearGuideBlockSpec(width=27, length=45.4, middle_part_length=32.4, total_height=13, height_1=3, block_side_width=7.5, screw='m3', screw_depth=3.5, screw_b=20, screw_c=20, rail='mgn12', grease_hole_diameter=2, grease_hole_position=2.5, weight=0.05),
	'mgn15c': LinearGuideBlockSpec(width=32, length=42.1, middle_part_length=26.7, total_height=16, height_1=4, block_side_width=8.5, screw='m3', screw_depth=4, screw_b=25, screw_c=20, rail='mgn15', grease_hole_diameter=3, grease_hole_position=3, weight=0.06),
	'mgn15h': LinearGuideBlockSpec(width=32, length=58.8, middle_part_length=43.4, total_height=16, height_1=4, block_side_width=8.5, screw='m3', screw_depth=4, screw_b=25, screw_c=25, rail='mgn15', grease_hole_diameter=3, grease_hole_position=3, weight=0.09),
	'mgw05c': LinearGuideBlockSpec(width=17, length=20.5, middle_part_length=14.1, total_height=6.5, height_1=1.5, block_side_width=3.5, screw='m2_5', screw_depth=1.5, screw_b=13, screw_c=0, rail='mgw05', grease_hole_diameter=0.8, grease_hole_position=1, weight=0.016),
	'mgw05cl': LinearGuideBlockSpec(width=17, length=20.5, middle_part_length=14.1, total_height=6.5, height_1=1.5, block_side_width=3.5, screw='m3', screw_depth=10, screw_b=0, screw_c=6.5, rail='mgw05', grease_hole_diameter=0.8, grease_hole_position=1, weight=0.016),
	'mgw07c': LinearGuideBlockSpec(width=25, length=31.2, middle_part_length=21, total_height=9, height_1=1.9, block_side_width=5.5, screw='m3', screw_depth=3, screw_b=19, screw_c=10, rail='mgw07', grease_hole_diameter=1.2, grease_hole_position=1.85, weight=0.02),
	'mgw07h': LinearGuideBlockSpec(width=25, length=41, middle_part_length=30.8, total_height=9, height_1=1.9, block_side_width=5.5, screw='m3', screw_depth=3, screw_b=19, screw_c=19, rail='mgw07', grease_hole_diameter=1.2, grease_hole_position=1.85, weight=0.029),
	'mgw09c': LinearGuideBlockSpec(width=30, length=39.3, middle_part_length=27.5, total_height=12, height_1=2.9, block_side_width=6, screw='m3', screw_depth=3, screw_b=12, screw_c=12, rail='mgw09', grease_hole_diameter=1.2, grease_hole_position=2.4, weight=0.04),
	'mgw09h': LinearGuideBlockSpec(width=30, length=50.7, middle_part_length=38.5, total_height=12, height_1=2.9, block_side_width=6, screw='m3', screw_depth=3, screw_b=23, screw_c=24, rail='mgw09', grease_hole_diameter=1.2, grease_hole_position=2.4, weight=0.057),
	'mgw12c': LinearGuideBlockSpec(width=40, length=46.1, middle_part_length=31.3, total_height=14, height_1=3.4, block_side_width=8, screw='m3', screw_depth=3.6, screw_b=28, screw_c=15, rail='mgw12', grease_hole_diameter=1.2, grease_hole_position=2.8, weight=0.071),
	'mgw12h': LinearGuideBlockSpec(width=40, length=60.4, middle_part_length=45.6, total_height=14, height_1=3.4, block_side_width=8, screw='m3', screw_depth=3.6, screw_b=28, screw_c=28, rail='mgw12', grease_hole_diameter=1.2, grease_hole_position=2.8, weight=0.103),
	'mgw15c': LinearGuideBlockSpec(width=60, length=54.8, middle_part_length=38, total_height=16, height_1=3.4, block_side_width=9, screw='m4', screw_depth=4.2, screw_b=45, screw_c=20, rail='mgw15', grease_hole_diameter=3, grease_hole_position=3.2, weight=0.143),
	'mgw15h': LinearGuideBlockSpec(width=60, length=73.8, middle_part_length=57, total_height=16, height_1=3.4, block_side_width=9, screw='m4', screw_depth=4.2, screw_b=45, screw_c=35, rail='mgw15', grease_hole_diameter=3, grease_hole_position=3.2, weight=0.215),
}



# リニアガイドブロックの寸法洗濯用Enum
BLOCK_SIZE_ITEMS = [
	('mgn05c', 'MGN5C', 'Set specs to MGN05C size'),
	('mgn05h', 'MGN5H', 'Set specs to MGN05H size'),
	('mgn07c', 'MGN7C', 'Set specs to MGN07C size'),
	('mgn07h', 'MGN7H', 'Set specs to MGN07H size'),
	('mgn09c', 'MGN9C', 'Set specs to MGN09C size'),
	('mgn09h', 'MGN9H', 'Set specs to MGN09H size'),
	('mgn12c', 'MGN12C', 'Set specs to MGN12C size'),
	('mgn12h', 'MGN12H', 'Set specs to MGN12H size'),
	('mgn15c', 'MGN15C', 'Set specs to MGN15C size'),
	('mgn15h', 'MGN15H', 'Set specs to MGN15H size'),
	('mgw05c', 'MGW5C', 'Set specs to MGW05C size'),
	('mgw05cl', 'MGW5CL', 'Set specs to MGW05CL size'),
	('mgw07c', 'MGW7C', 'Set specs to MGW07C size'),
	('mgw07h', 'MGW7H', 'Set specs to MGW07H size'),
	('mgw09c', 'MGW9C', 'Set specs to MGW09C size'),
	('mgw09h', 'MGW9H', 'Set specs to MGW09H size'),
	('mgw12c', 'MGW12C', 'Set specs to MGW12C size'),
	('mgw12h', 'MGW12H', 'Set specs to MGW12H size'),
	('mgw15c', 'MGW15C', 'Set specs to MGW15C size'),
	('mgw15h', 'MGW15H', 'Set specs to MGW15H size'),
]










def create_hole(obj: bpy.types.Object, diameter: float, center: tuple[float, float, float], normal: Vector, extrude_vector: Vector, segments: int, fast_solver: bool = False) -> None:
	"""
	指定したオブジェクトに円柱で穴を開ける。

	Parameters
	----------
	obj : bpy.types.Object
		穴を開ける対象のオブジェクト。
	diameter : float
		円柱の直径。
	center : tuple[float, float, float]
		円柱の底面の中心座標 (x, y, z)。
	normal : Vector
		円柱の底面の法線ベクトル。
	extrude_vector : Vector
		円柱の方向と長さを表すベクトル。
	segments : int
		円柱のセグメント数。
	"""
	vertices = romly_utils.make_circle_vertices(radius=diameter / 2, num_vertices=segments, center=center, normal_vector=normal)
	faces = [list(range(len(vertices)))]
	romly_utils.extrude_face(vertices, faces=faces, extrude_vertex_indices=list(range(len(vertices))), offset=extrude_vector)
	hole_obj = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=vertices, faces=faces))
	bpy.context.collection.objects.link(hole_obj)

	# オブジェクトにブーリアンで穴を開ける
	romly_utils.apply_boolean_object(obj, hole_obj, fast_solver=fast_solver);










def create_block(width: float, height: float, length: float, y_offset: float, thickness: float = 0, bevel_width: float = 0, diff: bool = False) -> bpy.types.Object:
	obj = romly_utils.create_box(size=Vector((width, height, length)), offset=Vector((0, -y_offset - height / 2, 0)))

	# ベベル
	if bevel_width > 0:
		if diff:
			bpy.context.view_layer.objects.active = obj

			bm = bmesh.new()
			bm.from_mesh(obj.data)
			KEY = 'bevel_weight_edge'
			bevel_layer = bm.edges.layers.float.get(KEY, bm.edges.layers.float.new(KEY))
			for edge in bm.edges:
				if abs((edge.verts[0].co - edge.verts[1].co).dot(Vector((0, 0, 1)))) > 0.999:
					if edge.verts[0].co[1] < -(y_offset + height / 2):
						edge[bevel_layer] = 1.0
					else:
						edge[bevel_layer] = 0.5
			bm.to_mesh(obj.data)
			bm.free()

			# ベベルモディファイアを追加、適用
			romly_utils.apply_bevel_modifier(obj, bevel_width)
		else:
			romly_utils.apply_bevel_modifier_to_edges(obj, bevel_width, lambda edge: not romly_utils.is_edge_along_z_axis(edge))

	# 真ん中を削る
	if thickness > 0:
		cutter = romly_utils.create_box(size=Vector((width * 2, height * 2, length - thickness * 2)), offset=Vector((0, -y_offset - height / 2, 0)))
		romly_utils.apply_boolean_object(obj, cutter)

	return obj










def update_rail_spec(self, context):
	"""プロパティのパネルでMGN7〜MGN15などのボタンを押した時の処理。プロパティの値を押したボタンに合わせてセットする。"""
	spec = RAIL_SPECS.get(self.val_spec)
	if spec:
		self.val_rail_width = spec.Wr
		self.val_rail_height = spec.Hr
		self.val_rail_outer_hole_diameter = spec.outer_hole_diameter
		self.val_rail_outer_hole_depth = spec.outer_hole_depth
		self.val_rail_inner_hole_diameter = spec.inner_hole_diameter
		self.val_rail_hole_pitch = spec.hole_pitch
		self.val_spec_name_from_property = self.val_spec
	else:
		self.val_spec_name_from_property = ''



def cuurent_rail_spec_to_name(operator) -> str:
	"""現在の寸法設定から、寸法の名前（MGH07など）を取得する。値が一つでも異なる場合は空文字列を返す。"""
	for name, spec in RAIL_SPECS.items():
		if (math.isclose(spec.Wr, operator.val_rail_width) and
			math.isclose(spec.Hr, operator.val_rail_height) and
			math.isclose(spec.outer_hole_diameter, operator.val_rail_outer_hole_diameter) and
			math.isclose(spec.outer_hole_depth, operator.val_rail_outer_hole_depth) and
			math.isclose(spec.inner_hole_diameter, operator.val_rail_inner_hole_diameter) and
			math.isclose(spec.hole_pitch, operator.val_rail_hole_pitch)):
			return name

	return ''



def update_spec_property(self: bpy.types.OperatorProperties, context):
	"""
	リニアガイドレールの寸法に関わるプロパティの変更時処理。
	寸法の値から当てはまる寸法名を self.val_spec_name_from_property にセットする。
	"""
	self.val_spec_name_from_property = cuurent_rail_spec_to_name(self)










# MARK: add_linear_guide_rail
class ROMLYADDON_OT_add_linear_guide_rail(bpy.types.Operator):
	"""リニアガイドのレールを作成するオペレーター。"""
	bl_idname = 'romlyaddon.add_linear_guide_rail'
	bl_label = bpy.app.translations.pgettext_iface('Add Linear Guide Rail')
	bl_description = 'Construct a Rail for Linear Guide'
	bl_options = {'REGISTER', 'UNDO'}

	DEFAULT_SIZE = 'mgn09'
	val_spec: EnumProperty(name='Size', items=LINEAR_GUIDE_SIZE_ITEMS, default=DEFAULT_SIZE, update=update_rail_spec)

	val_rail_width: FloatProperty(name='Width', description='Width of the rail', default=RAIL_SPECS[DEFAULT_SIZE].Wr, min=1, soft_max=15.0, unit=bpy.utils.units.categories.LENGTH, update=update_spec_property)
	val_rail_height: FloatProperty(name='Height', description='Height (Thickness) of the rail', default=RAIL_SPECS[DEFAULT_SIZE].Hr, min=1, soft_max=10.0, unit=bpy.utils.units.categories.LENGTH, update=update_spec_property)

	# レールの長さ
	val_rail_length: FloatProperty(name='Length', description='Full length of the rail', default=100.0, min=50, soft_max=1000.0, unit=bpy.utils.units.categories.LENGTH)

	val_rail_outer_hole_diameter: FloatProperty(name='Outer Diameter', description='Outer Diameter of each hole', default=RAIL_SPECS[DEFAULT_SIZE].outer_hole_diameter, min=1, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH, update=update_spec_property)
	val_rail_inner_hole_diameter: FloatProperty(name='Inner Diameter', description='Inner Diameter of each hole', default=RAIL_SPECS[DEFAULT_SIZE].inner_hole_diameter, min=1, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH, update=update_spec_property)
	val_rail_outer_hole_depth: FloatProperty(name='Outer Hole Depth', description='Depth of outer hole', default=RAIL_SPECS[DEFAULT_SIZE].outer_hole_depth, min=1, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH, update=update_spec_property)
	val_rail_hole_pitch: FloatProperty(name='Hole Pitch', description='Hole Pitch', default=RAIL_SPECS[DEFAULT_SIZE].hole_pitch, min=1, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH, update=update_spec_property)

	val_first_hole_offset: FloatProperty(name='First Hole Offset', description='First Hole Offset', default=5, min=0, soft_max=100.0, unit=bpy.utils.units.categories.LENGTH)

	val_hole_segments: IntProperty(name='Hole Segments', description='Hole Segments', default=32, min=3, soft_max=64, max=128)

	val_slit_diameter: FloatProperty(name='Slit Diameter', description='Slit Diameter', default=1.5, min=1, soft_max=2.0, unit=bpy.utils.units.categories.LENGTH)
	val_slit_offset: FloatProperty(name='Slit Position', description='Position of the slits (from the surface)', default=2.0, min=0.5, soft_max=10.0, unit=bpy.utils.units.categories.LENGTH)
	val_slit_segments: IntProperty(name='Slit Segments', description='Slit Segments', default=24, min=3, soft_max=32, max=64)

	# 現在の設定値にマッチする寸法の名前を格納するためのプロパティ
	val_spec_name_from_property: StringProperty(name='spec_name_from_property', default=DEFAULT_SIZE)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_spec')

		box = col.box()
		box_col = box.column()
		row = box_col.row(align=True)
		row.prop(self, 'val_rail_width')
		row.prop(self, 'val_rail_height')
		box_col.separator()
		split = box_col.split(factor=0.2, align=True)
		split.label(text='Hole Diameter')
		row = split.row(align=True)
		row.prop(self, 'val_rail_outer_hole_diameter', text='Outer')
		row.prop(self, 'val_rail_inner_hole_diameter', text='Inner')
		box_col.prop(self, 'val_rail_outer_hole_depth')
		box_col.prop(self, 'val_rail_hole_pitch')

		# 重さを表示
		if self.val_spec_name_from_property:
			spec = RAIL_SPECS.get(self.val_spec_name_from_property)
			if spec:
				weight_per_mm = spec.weight / 1000.0 # 1mmあたりの重さ
				row = box_col.row(align=True)
				row.alignment = 'RIGHT'
				row.label(text=f"{bpy.app.translations.pgettext_iface('Weight')}: {romly_utils.units_to_string(self.val_rail_length * weight_per_mm, category=bpy.utils.units.categories.MASS)}")
		col.separator()

		col.prop(self, 'val_rail_length')
		col.prop(self, 'val_first_hole_offset')
		col.separator()

		split = col.split(factor=0.1, align=True)
		split.label(text='Slit')
		row = split.row(align=True)
		row.prop(self, 'val_slit_diameter', text='Diameter')
		row.prop(self, 'val_slit_offset', text='Offset')
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_hole_segments')
		col.prop(self, 'val_slit_segments')



	def execute(self, context):
		obj = romly_utils.create_box(Vector((self.val_rail_width, self.val_rail_height, self.val_rail_length)), offset=Vector((0, -self.val_rail_height / 2, self.val_rail_length / 2)))

		# オブジェクト名を設定
		obj_name = bpy.app.translations.pgettext_data('Linear Guide Rail')
		if self.val_spec_name_from_property:
			obj_name = obj_name + self.val_spec_name_from_property.upper()
		obj.name = obj_name + ' ' + romly_utils.units_to_string(self.val_rail_length, removeSpace=True)



		# ベベルモディファイアを追加、適用
		romly_utils.apply_bevel_modifier_to_edges(obj, 0.3, lambda edge: not romly_utils.is_edge_along_z_axis(edge))



		# 穴を開ける
		hole_z = self.val_first_hole_offset
		while hole_z <= self.val_rail_length:
			# 表側の大きい穴
			create_hole(obj, diameter=self.val_rail_outer_hole_diameter, center=(0, -self.val_rail_height + self.val_rail_outer_hole_depth, hole_z), normal=Vector((0, 1, 0)), extrude_vector=Vector((0, -self.val_rail_outer_hole_depth * 2, 0)), segments=self.val_hole_segments)

			# 裏まで貫通する穴
			create_hole(obj, diameter=self.val_rail_inner_hole_diameter, center=(0, 0.1, hole_z), normal=Vector((0, 1, 0)), extrude_vector=Vector((0, -self.val_rail_height + 0.2, 0)), segments=self.val_hole_segments)

			hole_z += self.val_rail_hole_pitch



		# ボール溝を作る
		extrude_vector = Vector((0, 0, self.val_rail_length + 0.2))
		normal = Vector((0, 0, 1))
		create_hole(obj, diameter=self.val_slit_diameter, center=(-self.val_rail_width / 2, -self.val_rail_height + self.val_slit_offset, -0.1), normal=normal, extrude_vector=extrude_vector, segments=self.val_slit_segments)
		create_hole(obj, diameter=self.val_slit_diameter, center=(self.val_rail_width / 2, -self.val_rail_height + self.val_slit_offset, -0.1), normal=normal, extrude_vector=extrude_vector, segments=self.val_slit_segments)



		# オブジェクトを3Dカーソル位置へ移動
		obj.location = bpy.context.scene.cursor.location

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		obj.select_set(state=True)
		bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}










def update_block_spec(self, context):
	"""プロパティのパネルでMGN7〜MGN15などのボタンを押した時の処理。プロパティの値を押したボタンに合わせてセットする。"""
	spec = BLOCK_SPECS.get(self.val_spec)
	if spec:
		self.val_width = spec.width
		self.val_length = spec.length
		self.val_middle_part_length = spec.middle_part_length
		self.val_height = spec.total_height
		self.val_height_1 = spec.height_1
		self.val_side_width = spec.block_side_width

		screw_spec = romly_utils.SCREW_SPECS.get(spec.screw)
		if screw_spec:
			self.val_screw_hole_diameter = screw_spec.diameter

		self.val_screw_depth = spec.screw_depth
		self.val_screw_b = spec.screw_b
		self.val_screw_c = spec.screw_c

		rail_spec = RAIL_SPECS.get(spec.rail)
		if rail_spec:
			self.val_rail_height = rail_spec.Hr

		self.val_grease_hole_diameter = spec.grease_hole_diameter
		self.val_grease_hole_position = spec.grease_hole_position










def current_block_spec_to_name(operator) -> str:
	"""現在の寸法設定から、寸法の名前（MGN09Cなど）を取得する。値が一つでも異なる場合は空文字列を返す。"""
	for name, spec in BLOCK_SPECS.items():
		rail_spec = RAIL_SPECS.get(spec.rail)
		if (math.isclose(spec.width, operator.val_width, abs_tol=0.01) and
			math.isclose(spec.length, operator.val_length, abs_tol=0.01) and
			math.isclose(spec.middle_part_length, operator.val_middle_part_length, abs_tol=0.01) and
			math.isclose(spec.total_height, operator.val_height, abs_tol=0.01) and
			math.isclose(spec.height_1, operator.val_height_1, abs_tol=0.01) and
			math.isclose(spec.block_side_width, operator.val_side_width, abs_tol=0.01) and
			math.isclose(spec.screw_depth, operator.val_screw_depth, abs_tol=0.01) and
			math.isclose(spec.screw_b, operator.val_screw_b, abs_tol=0.01) and
			math.isclose(spec.screw_c, operator.val_screw_c, abs_tol=0.01) and
			(rail_spec and math.isclose(rail_spec.Hr, operator.val_rail_height, abs_tol=0.01))):
			return name

	return ''



def update_block_spec_property(self: bpy.types.OperatorProperties, context):
	"""
	リニアガイドブロックの寸法に関わるプロパティの変更時処理。
	寸法の値から当てはまる寸法名を self.val_spec_name_from_property にセットする。
	"""
	self.val_spec_name_from_property = current_block_spec_to_name(self)










# MARK: add_linear_guide_block
class ROMLYADDON_OT_add_linear_guide_block(bpy.types.Operator):
	"""リニアガイドのブロックを作成するオペレーター。"""
	bl_idname = 'romlyaddon.add_linear_guide_block'
	bl_label = bpy.app.translations.pgettext_iface('Add Linear Guide Block')
	bl_description = 'Construct a Block for Linear Guide'
	bl_options = {'REGISTER', 'UNDO'}

	DEFAULT_SIZE = 'mgn09c'
	val_spec: EnumProperty(name='Size', items=BLOCK_SIZE_ITEMS, default=DEFAULT_SIZE, update=update_block_spec)

	val_width: FloatProperty(name='W Width', description='Width of the block (perpendicular size to the rail)', default=BLOCK_SPECS[DEFAULT_SIZE].width, min=1, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_length: FloatProperty(name='L Length', description='Length of the block (parallel size to the rail)', default=BLOCK_SPECS[DEFAULT_SIZE].length, min=1, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_middle_part_length: FloatProperty(name='L1 Metal Part Length', description='Length of the middle metal part', default=BLOCK_SPECS[DEFAULT_SIZE].middle_part_length, min=1, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_height: FloatProperty(name='H Total Height', description='Height to the block surface from the rail bottom', default=BLOCK_SPECS[DEFAULT_SIZE].total_height, min=1, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_height_1: FloatProperty(name='H1 Bottom Space', description='Height to the block bottom from the rail bottom', default=BLOCK_SPECS[DEFAULT_SIZE].height_1, min=1, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_side_width: FloatProperty(name='N Rail Side Width', description='Width of the both sides part of the rail', default=BLOCK_SPECS[DEFAULT_SIZE].block_side_width, min=1, soft_max=10, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)

	val_screw_hole_diameter: FloatProperty(name='Diameter', default=romly_utils.SCREW_SPECS[BLOCK_SPECS[DEFAULT_SIZE].screw].diameter, min=1, soft_max=6, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_screw_depth: FloatProperty(name='l Depth', description='Depth of the screw holes', default=BLOCK_SPECS[DEFAULT_SIZE].screw_depth, min=1, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_screw_b: FloatProperty(name='Horizontal Distance', description='[B] Horizontal distance (perpendicular to the rail) between the screw holes', default=BLOCK_SPECS[DEFAULT_SIZE].screw_b, min=0, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_screw_c: FloatProperty(name='Vertical Distance', description='[C] Vertical distance (parallel to the rail) between the screw holes', default=BLOCK_SPECS[DEFAULT_SIZE].screw_c, min=0, soft_max=100, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_screw_pitch: FloatProperty(name='Pitch', description='Pitch of the screw threads', default=romly_utils.SCREW_SPECS[BLOCK_SPECS[DEFAULT_SIZE].screw].pitch, min=0.25, max=5, unit=bpy.utils.units.categories.LENGTH, precision=3)
	val_screw_thread_depth: FloatProperty(name='Thread Depth', description='Depth of threads of screw holes', default=romly_utils.SCREW_SPECS[BLOCK_SPECS[DEFAULT_SIZE].screw].thread_depth(), min=0.1, max=5, unit=bpy.utils.units.categories.LENGTH, precision=3)
	val_threading: BoolProperty(name='Threading', description="Thread screw holes if it's checked", default=False)

	val_grease_hole_diameter: FloatProperty(name='Diameter', description='[Gn] Diameter of the grease hole in the end seal (the red part)', default=BLOCK_SPECS[DEFAULT_SIZE].grease_hole_diameter, min=0.0, soft_max=3, unit=bpy.utils.units.categories.LENGTH, precision=3)
	val_grease_hole_position: FloatProperty(name='Position', description='[H2] Distance to the grease hole on the end seal (the red part) from the block surface', default=BLOCK_SPECS[DEFAULT_SIZE].grease_hole_position, min=0.0, soft_max=5, unit=bpy.utils.units.categories.LENGTH, precision=3)

	val_rail_height: FloatProperty(name='Rail Height', description='[HR] Height of the linear guide rail. Used to create indentations in the block', default=RAIL_SPECS[BLOCK_SPECS[DEFAULT_SIZE].rail].Hr, min=1, soft_max=10, unit=bpy.utils.units.categories.LENGTH, precision=3, update=update_block_spec_property)
	val_rail_clearance: FloatProperty(name='Rail Clearance', description='Clearance between the block and linear guide rail. The height of indentation of the block will be the total of this value and Rail Height', default=0.2, min=0.0, soft_max=1, unit=bpy.utils.units.categories.LENGTH, precision=3)

	# エンドシールの厚み。この値は寸法図にないので適当
	val_endseal_thickness: FloatProperty(name='End Seal Thickness', description='Thickness of the end seal (the red part on top and bottom)', default=1, min=0.0, soft_max=3, unit=bpy.utils.units.categories.LENGTH, precision=3)

	# ブロックのベベル幅。この値も寸法図にないので適当
	val_block_bevel_width: FloatProperty(name='Block Bevel Width', default=0.5, min=0.0, soft_max=2, unit=bpy.utils.units.categories.LENGTH, precision=3)

	# 穴のセグメント数。ネジ穴と縁の穴共通。
	val_hole_segments: IntProperty(name='Hole Segments', default=32, min=3, soft_max=64, max=128)

	# 現在の設定値にマッチする寸法の名前を格納するためのプロパティ
	val_spec_name_from_property: StringProperty(name='spec_name_from_property', default=DEFAULT_SIZE)



	def create_screw_holes_and_cut_rail(self, obj: bpy.types.Object, threading: bool):
		"""_summary_

		Parameters
		----------
		obj : bpy.types.Object
			_description_
		threading : bool
			ねじ切りするかどうか
		"""
		# ネジ穴を開ける
		hole_center_y = -self.val_height + self.val_screw_depth
		centers = []
		if self.val_screw_b > 0 and self.val_screw_c > 0:
			centers.append((-self.val_screw_b / 2, hole_center_y, self.val_screw_c / 2))
			centers.append((self.val_screw_b / 2, hole_center_y, self.val_screw_c / 2))
			centers.append((-self.val_screw_b / 2, hole_center_y, -self.val_screw_c / 2))
			centers.append((self.val_screw_b / 2, hole_center_y, -self.val_screw_c / 2))
		elif self.val_screw_b > 0:
			centers.append((-self.val_screw_b / 2, hole_center_y, 0))
			centers.append((self.val_screw_b / 2, hole_center_y, 0))
		elif self.val_screw_c > 0:
			centers.append((0, hole_center_y, self.val_screw_c / 2))
			centers.append((0, hole_center_y, -self.val_screw_c / 2))
		else:
			centers.append((0, hole_center_y, 0))
		l = self.val_screw_depth * 2
		if threading:
			# 全ネジの円柱を作成
			pitch = self.val_screw_pitch
			thread_depth = self.val_screw_thread_depth
			screw_obj = romly_utils.create_threaded_cylinder(diameter=self.val_screw_hole_diameter, length=l, pitch=pitch, lead=1, thread_depth=thread_depth, segments=self.val_hole_segments, bevel_segments=5, edge_flat=True)
			screw_obj.rotation_euler = (-math.pi / 2, 0, 0)
			for index, c in enumerate(centers):
				screw_obj.location = c
				is_last = index == len(centers) - 1
				romly_utils.apply_boolean_object(obj, screw_obj, unlink=is_last)
		else:
			for c in centers:
				create_hole(obj, diameter=self.val_screw_hole_diameter, center=c, normal=Vector((0, 1, 0)), extrude_vector=Vector((0, -l, 0)), segments=self.val_hole_segments, fast_solver=True)

		# レール部分を削る
		h = self.val_rail_height + self.val_rail_clearance
		w = self.val_width - self.val_side_width * 2
		rail_obj = romly_utils.create_box(size=Vector((w, h, self.val_length + 0.1 * 2)), offset=Vector((0, -h / 2, 0)))
		romly_utils.apply_boolean_object(obj, rail_obj, fast_solver=True)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()
		col.prop(self, 'val_spec')

		box = col.box()
		box_col = box.column()
		row = box_col.row(align=True)
		row.prop(self, 'val_width')
		row.prop(self, 'val_length')
		box_col.prop(self, 'val_middle_part_length')
		row = box_col.row(align=True)
		row.prop(self, 'val_height')
		row.prop(self, 'val_height_1')
		box_col.prop(self, 'val_side_width')
		box_col.separator()

		box_col.label(text='Screw Holes')
		row = box_col.row(align=True)
		row.prop(self, 'val_screw_hole_diameter')
		row.prop(self, 'val_screw_depth')
		row = box_col.row(align=True)
		row.prop(self, 'val_screw_b')
		row.prop(self, 'val_screw_c')
		box_col.prop(self, 'val_threading')
		col_threading = box_col.column(align=True)
		col_threading.enabled = self.val_threading
		col_threading.prop(self, 'val_screw_pitch')
		col_threading.prop(self, 'val_screw_thread_depth')
		box_col.separator()

		box_col.label(text='Grease Holes')
		row = box_col.row(align=True)
		row.prop(self, 'val_grease_hole_diameter')
		row.prop(self, 'val_grease_hole_position')
		box_col.separator()

		box_col.prop(self, 'val_rail_height')

		# 重さを表示
		if self.val_spec_name_from_property:
			spec = BLOCK_SPECS.get(self.val_spec_name_from_property)
			if spec:
				row = box_col.row(align=True)
				row.alignment = 'RIGHT'
				row.label(text=f"{bpy.app.translations.pgettext_iface('Weight')}: {romly_utils.units_to_string(spec.weight, category=bpy.utils.units.categories.MASS)}")
		col.separator()

		col.label(text='Mesh Settings')
		col.prop(self, 'val_rail_clearance')
		col.prop(self, 'val_endseal_thickness')
		col.prop(self, 'val_block_bevel_width')
		col.prop(self, 'val_hole_segments')



	def execute(self, context):
		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')



		# 中央部分と上下部分との大きさの差
		TOP_BOTTOM_SIZE_DIFF = 0.1

		# 縁と上下部分を除く本体
		block_obj = create_block(
			width=self.val_width,
			height=self.val_height - self.val_height_1,
			length=self.val_middle_part_length,
			y_offset=self.val_height_1, bevel_width=self.val_block_bevel_width)
		self.create_screw_holes_and_cut_rail(block_obj, threading=self.val_threading)

		# 縁の部分（赤いところ）
		endseal_obj = None
		if self.val_endseal_thickness > 0.0:
			endseal_obj = create_block(
				width=self.val_width - TOP_BOTTOM_SIZE_DIFF * 2,
				height=self.val_height - self.val_height_1 - TOP_BOTTOM_SIZE_DIFF,
				length=self.val_length,
				y_offset=self.val_height_1,
				thickness=self.val_endseal_thickness, bevel_width=self.val_block_bevel_width * 2, diff=True)
			self.create_screw_holes_and_cut_rail(endseal_obj, threading=self.val_threading)

			# 縁の穴
			hole_y = -self.val_height + self.val_grease_hole_position
			hole_z = -self.val_length / 2 - 0.1
			create_hole(endseal_obj, diameter=self.val_grease_hole_diameter, center=(0, hole_y, hole_z), normal=Vector((0, 0, 1)), extrude_vector=Vector((0, 0, self.val_length + 0.1 * 2)), segments=self.val_hole_segments)

		# エンドキャップ（緑のところ）
		endcap_part = create_block(
			width=self.val_width - TOP_BOTTOM_SIZE_DIFF * 2,
			height=self.val_height - self.val_height_1 - TOP_BOTTOM_SIZE_DIFF,
			length=self.val_length - self.val_endseal_thickness * 2,
			y_offset=self.val_height_1,
			thickness=(self.val_length - self.val_middle_part_length - self.val_endseal_thickness * 2) / 2,
			bevel_width=self.val_block_bevel_width)
		self.create_screw_holes_and_cut_rail(endcap_part, threading=self.val_threading)

		# 結合
		block_obj.select_set(state=True)
		endcap_part.select_set(state=True)
		if endseal_obj:
			endseal_obj.select_set(state=True)
		bpy.context.view_layer.objects.active = block_obj
		bpy.ops.object.join()



		# オブジェクト名を設定
		obj_name = bpy.app.translations.pgettext_data('Linear Guide Block')
		if self.val_spec_name_from_property:
			obj_name += self.val_spec_name_from_property.upper()
		block_obj.name = obj_name



		# オブジェクトを3Dカーソル位置へ移動
		block_obj.location = bpy.context.scene.cursor.location

		# 現在の選択を解除
		bpy.ops.object.select_all(action='DESELECT')

		# 生成したオブジェクトを選択
		block_obj.select_set(state=True)
		bpy.context.view_layer.objects.active = block_obj

		return {'FINISHED'}












class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = 'ROMLYADDON_MT_romly_add_mesh_menu_parent'
	bl_label = 'Romly'
	bl_description = 'Romly Addon Menu'



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_linear_guide_block.bl_idname, text=bpy.app.translations.pgettext_iface('Add Linear Guide Block'), icon='SNAP_MIDPOINT')
		layout.operator(ROMLYADDON_OT_add_linear_guide_rail.bl_idname, text=bpy.app.translations.pgettext_iface('Add Linear Guide Rail'), icon='FIXED_SIZE')









# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_linear_guide_rail,
	ROMLYADDON_OT_add_linear_guide_block,
	ROMLYADDON_MT_romly_add_mesh_menu_parent,
]



def register():
	# 翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.append(menu_func)





# クラスの登録解除
def unregister():
	# 翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)

	bpy.types.VIEW3D_MT_add.remove(menu_func)





# スクリプトのエントリポイント
# スクリプト単体のデバッグ用で、 __init__.py でアドオンとして追加したときは呼ばれない。
if __name__ == '__main__':
	register()
