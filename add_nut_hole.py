import bpy
import math
import mathutils
import bmesh
from bmesh.types import BMVert
from bpy.props import *
from mathutils import Vector, Matrix, Quaternion
from typing import NamedTuple, Literal



from . import romly_utils










class SlitSize(NamedTuple):
	"""
	スリットの寸法を表すクラス。

	Parameters
	----------
	length : float
		スリットの長さ。
	thickness : float
		スリットの厚み（幅）。
	height : float, optional
		スリットの高さ（Z方向）。デフォルトは1.0。
	"""
	length: float
	thickness: float
	height: float = 1.0

	def has_size(self) -> bool:
		"""
		スリットが大きさを持つか（長さ、厚み、高さが全て0より大きい）を取得する。

		Returns
		-------
		bool
			すべての寸法が0より大きい場合はTrue。
		"""
		return self.length > 0 and self.thickness > 0 and self.height > 0










def create_nut_hole_object(type: Literal['sacrificial', 'bridge'], nut_diameter: float, screw_hole_diameter: float, layer_thickness: float, screw_hole_segments: int, nut_hole_depth: float, nut_hole_surplus: float, screw_hole_length: float, seam_slit: SlitSize, seam_slit_count: int, first_layer_slit: SlitSize, first_layer_slit_angle: float) -> bpy.types.Object:
	"""_summary_

	Parameters
	----------
	type : Literal['sacrificial', 'bridge']
		穴の形成方法。
	nut_diameter : float
		ナットの外径。ナットの外接円の直径。
	screw_hole_diameter : float
		_description_
	layer_thickness : float
		_description_
	screw_hole_segments : int
		_description_
	nut_hole_depth : float
		ナット穴の深さ。
	nut_hole_surplus : float
		ナット穴の下部の余長。
	screw_hole_length : float
		_description_
	seam_slit : SlitSize
		シーム避けスリットのサイズ。高さはナット穴、ネジ穴と同じになるため無視される。
	seam_slit_count : int
		シーム避けスリットをいくつ作るか。1の場合は一箇所のみ、それ以外の場合は各頂点に六ヶ所作る。
	first_layer_slit : SlitSize
		ファーストレイヤーの定着用スリットのサイズ。
	first_layer_slit_angle : float
		ファーストレイヤーの定着用スリットの向き。

	Returns
	-------
	bpy.types.Object
	"""
	# 底部を綺麗にするために余分に伸ばしてカットする長さ。適当。
	SURPLUS_LENGTH = 3

	# XY平面上に十分な大きさ
	enough_size = (nut_diameter + max(seam_slit.length, first_layer_slit.length)) * 2

	# 六角形を作成して下方向に掃引、六角柱を作成
	vertices = romly_utils.make_circle_vertices(radius=nut_diameter / 2, num_vertices=6, center=(0, 0, nut_hole_depth))
	faces = [list(range(6))]
	romly_utils.extrude_face(vertices, faces=faces, extrude_vertex_indices=list(range(6)), z_offset=-(nut_hole_depth + nut_hole_surplus + SURPLUS_LENGTH))
	hexagon_cylinder = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=vertices, faces=faces))

	# ブーリアン適用処理のためシーンにリンクする必要がある
	bpy.context.collection.objects.link(hexagon_cylinder)



	# 六角柱のシーム避けスリット
	if seam_slit.has_size():
		corner2_y = 0 if seam_slit_count == 1 else -nut_diameter / 2 - seam_slit.length
		tool_object = romly_utils.create_box_from_corners(corner1=(-seam_slit.thickness / 2, nut_diameter / 2 + seam_slit.length, nut_hole_depth), corner2=(seam_slit.thickness / 2, corner2_y, -(nut_hole_surplus + SURPLUS_LENGTH)))
		tool_object.select_set(True)
		bpy.ops.transform.rotate(value=math.pi / 2, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', center_override=(0, 0, 0))
		romly_utils.apply_boolean_object(hexagon_cylinder, tool_object, operation='UNION');



	# 円柱を合体
	circle_vertices = romly_utils.make_circle_vertices(radius=screw_hole_diameter / 2, num_vertices=screw_hole_segments, center=(0, 0, nut_hole_depth - 0.1))
	faces = [list(range(len(circle_vertices)))]
	romly_utils.extrude_face(vertices=circle_vertices, faces=faces, extrude_vertex_indices=list(range(len(circle_vertices))), z_offset=screw_hole_length + SURPLUS_LENGTH)
	cylinder = romly_utils.cleanup_mesh(romly_utils.create_object(vertices=circle_vertices, faces=faces))
	bpy.context.collection.objects.link(cylinder)
	romly_utils.apply_boolean_object(hexagon_cylinder, cylinder, operation='UNION')




	if layer_thickness > 0:
		ENOUGH_HEIGHT = 5

		if type == 'bridge':
			# 直方体を二つ作って左右を削る
			cutter_object = romly_utils.create_box_from_corners(corner1=(-nut_diameter, nut_diameter, 0), corner2=(-screw_hole_diameter / 2, -nut_diameter, ENOUGH_HEIGHT))
			cutter_object.location += Vector((0, 0, nut_hole_depth - layer_thickness * 2))
			romly_utils.apply_boolean_object(hexagon_cylinder, cutter_object);
			cutter_object = romly_utils.create_box_from_corners(corner1=(nut_diameter, nut_diameter, 0), corner2=(screw_hole_diameter / 2, -nut_diameter, ENOUGH_HEIGHT))
			cutter_object.location += Vector((0, 0, nut_hole_depth - layer_thickness * 2))
			romly_utils.apply_boolean_object(hexagon_cylinder, cutter_object);

		# 六角柱のシーム避けスリット（2本目以降）
		if seam_slit.has_size() and seam_slit_count > 1:
			for i in range(1, 3):
				tool_object = romly_utils.create_box_from_corners(corner1=(-seam_slit.thickness / 2, nut_diameter / 2 + seam_slit.length, nut_hole_depth), corner2=(seam_slit.thickness / 2, -nut_diameter / 2 - seam_slit.length, -(nut_hole_surplus + SURPLUS_LENGTH)))
				tool_object.select_set(True)
				bpy.ops.transform.rotate(value=math.pi / 2 + math.radians(60 * i), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', center_override=(0, 0, 0))
				romly_utils.apply_boolean_object(hexagon_cylinder, tool_object, operation='UNION');

		if type == 'bridge':
			# 直方体2つを使って上下を削る
			cutter_object = romly_utils.create_box_from_corners(corner1=(-nut_diameter, nut_diameter, 0), corner2=(nut_diameter, screw_hole_diameter / 2, ENOUGH_HEIGHT))
			cutter_object.location += Vector((0, 0, nut_hole_depth - layer_thickness))
			romly_utils.apply_boolean_object(hexagon_cylinder, cutter_object);
			cutter_object = romly_utils.create_box_from_corners(corner1=(-nut_diameter, -nut_diameter, 0), corner2=(nut_diameter, -screw_hole_diameter / 2, ENOUGH_HEIGHT))
			cutter_object.location += Vector((0, 0, nut_hole_depth - layer_thickness))
			romly_utils.apply_boolean_object(hexagon_cylinder, cutter_object);

	# 円柱のシーム避けスリット
	if seam_slit.has_size():
		tool_object = romly_utils.create_box_from_corners(corner1=(-seam_slit.thickness / 2, screw_hole_diameter / 2 + seam_slit.length, nut_hole_depth), corner2=(seam_slit.thickness / 2, 0, nut_hole_depth + screw_hole_length + SURPLUS_LENGTH))
		tool_object.select_set(True)
		bpy.ops.transform.rotate(value=math.pi / 2, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', center_override=(0, 0, 0))
		romly_utils.apply_boolean_object(hexagon_cylinder, tool_object, operation='UNION');



	# 犠牲レイヤーの場合のレイヤー作成
	if type == 'sacrificial':
		cutter_object = romly_utils.create_box_from_corners(corner1=(-enough_size, enough_size, nut_hole_depth + layer_thickness), corner2=(enough_size, -enough_size, nut_hole_depth))
		romly_utils.apply_boolean_object(hexagon_cylinder, cutter_object);



	# ファーストレイヤーの定着用スリット
	if first_layer_slit.has_size():
		x_size = first_layer_slit.thickness / 2
		y_size = nut_diameter / 2 + first_layer_slit.length
		cutter_object = romly_utils.create_box_from_corners(corner1=(-x_size, 0, first_layer_slit.height), corner2=(x_size, y_size, -(nut_hole_surplus + SURPLUS_LENGTH)))
		cutter_object.select_set(True)
		bpy.ops.transform.rotate(value=math.pi / 2 + first_layer_slit_angle, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', center_override=(0, 0, 0))
		romly_utils.apply_boolean_object(hexagon_cylinder, cutter_object, operation='UNION');



	enough_size_y = nut_diameter / 2 + max(seam_slit.length, first_layer_slit.length) * 2

	# 余分に伸ばした円柱（上部）を削る
	cutter_object = romly_utils.create_box_from_corners(corner1=(-enough_size, enough_size, nut_hole_depth + screw_hole_length), corner2=(enough_size, -enough_size, nut_hole_depth + screw_hole_length + SURPLUS_LENGTH * 2))
	romly_utils.apply_boolean_object(hexagon_cylinder, cutter_object);

	# 余分に伸ばした下部を削る
	cutter_object = romly_utils.create_box_from_corners(corner1=(-enough_size, enough_size_y, -nut_hole_surplus), corner2=(enough_size, -enough_size_y, -nut_hole_surplus - SURPLUS_LENGTH * 2))
	romly_utils.apply_boolean_object(hexagon_cylinder, cutter_object);

	return hexagon_cylinder










def get_nut_hole_object_name(nut_diameter: float) -> str:
	"""ナットの外径から、ナット穴オブジェクトの名前を取得する。"""
	s = bpy.app.translations.pgettext_data('Nut Hole')
	for name, spec in romly_utils.SCREW_SPECS.items():
		if abs(spec.bolthead_diameter() - nut_diameter) < 0.001:
			return s + ' ' + name.upper()

	return s










def update_sizes(self, context):
	"""プロパティのパネルでM2〜M8などのボタンを押した時の処理。プロパティの値を押したボタンに合わせてセットする。"""

	# 指定されたスクリューサイズに基づいて直径とピッチを設定
	spec = romly_utils.SCREW_SPECS.get(self.val_sizes)
	if spec:
		self.val_nut_diameter = spec.bolthead_diameter()
		self.val_screw_hole_diameter = spec.diameter










# MARK: Class
class ROMLYADDON_OT_add_nut_hole(bpy.types.Operator):
	bl_idname = 'romlyaddon.add_nut_hole'
	bl_label = bpy.app.translations.pgettext_iface('Add Nut Hole')
	bl_description = 'Construct a hole for a nut for 3D printing'
	bl_options = {'REGISTER', 'UNDO'}

	enable_create_method: bool = True



	# 作成方法
	CREATE_METHOD_ONLY_OBJECT = 'object_only'
	CREATE_METHOD_BOOLEAN = 'boolean'
	CREATE_METHOD_ITEMS = [
		(CREATE_METHOD_ONLY_OBJECT, 'Only Tool Object', 'Create a nut hole object for boolean modifier'),
		(CREATE_METHOD_BOOLEAN, 'Boolean', 'Create a nut hole for the selected object'),
	]

	val_create_method: EnumProperty(name='Create Method', items=CREATE_METHOD_ITEMS, default=CREATE_METHOD_BOOLEAN)
	val_keep_modifier: BoolProperty(name='Keep Modifier', default=True)



	# 規定サイズ
	SIZE_ITEMS = [
		('m2', 'M2', 'Set specs to M2 size'),
		('m2_5', 'M2.5', 'Set specs to M2.5 size'),
		('m3', 'M3', 'Set specs to M3 size'),
		('m4', 'M4', 'Set specs to M4 size'),
		('m5', 'M5', 'Set specs to M5 size'),
		('m6', 'M6', 'Set specs to M6 size'),
	]

	# デフォルトのサイズ
	DEFAULT_SIZE = 'm3'

	val_sizes: EnumProperty(name='sizes', items=SIZE_ITEMS, default=DEFAULT_SIZE, update=update_sizes)

	# 穴の形成方法
	val_type: EnumProperty(name='Type', items=[('sacrificial', 'Sacrificial Layer', ''), ('bridge', 'Bridge Layer', '')], default='sacrificial')

	# ナットの外径。外接円の直径。
	val_nut_diameter: FloatProperty(name='Nut Diameter', description='Nut Diameter', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].bolthead_diameter(), min=0.1, soft_max=30, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# ネジ穴の直径
	val_screw_hole_diameter: FloatProperty(name='Screw Hole Diameter', description='Screw Hole Diameter', default=romly_utils.SCREW_SPECS[DEFAULT_SIZE].diameter, min=0.1, soft_max=30, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# レイヤーの厚み
	val_layer_thickness: FloatProperty(name='Layer Thickness', description='Layer Thickness', default=0.2, min=0.0, soft_max=1, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH, precision=3)

	# ネジ穴のセグメント数
	val_screw_hole_segments: IntProperty(name='Screw Hole Segments', description='Screw Hole Segments', default=32, min=3, max=80)

	# ナットの穴の遊び
	val_nut_hole_clearance: FloatProperty(name='Nut Diameter Clearance', description='Nut Diameter Clearance', default=0.4, min=0.0, soft_max=1.0, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH, precision=3)

	# ネジ穴の遊び
	val_screw_hole_clearance: FloatProperty(name='Screw Hole Clearance', description='Screw Hole Clearance', default=0.4, min=0.0, soft_max=1.0, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH, precision=3)

	# ナット穴の長さ
	val_nut_hole_length_above: FloatProperty(name='Nut Hole Depth', default=5, min=0.1, soft_max=10, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_nut_hole_length_below: FloatProperty(name='Nut Hole Surplus Length', default=10, min=1, soft_max=50, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# ネジ穴の長さ
	val_screw_hole_length: FloatProperty(name='Screw Hole Length', description='Screw Hole Length', default=30, min=0.1, soft_max=100, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)

	# シームを隠すためのスリットの長さ
	val_no_seam_slit_length: FloatProperty(name='Seam Avoidance Slit Depth', default=1, min=0.1, soft_max=3, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_no_seam_slit_width: FloatProperty(name='Seam Avoidance Slit Thickness', default=0.1, min=0.1, soft_max=1, precision=3, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_no_seam_slit_count: EnumProperty(name='Seam Avoidance Slit Count', items=[('1', '1', 'Single Point'), ('6', '6', '6 Points')], default='1')

	# ファーストレイヤーの定着を良くするためのスリット
	val_first_layer_slit_length: FloatProperty(name='First Layer Slit Depth', default=10, min=0, soft_max=300, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_first_layer_slit_width: FloatProperty(name='First Layer Slit Thickness', default=0.1, min=0.1, soft_max=1, precision=3, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_first_layer_slit_height: FloatProperty(name='First Layer Slit Height', default=0.5, min=0.1, soft_max=1, precision=3, subtype='DISTANCE', unit=bpy.utils.units.categories.LENGTH)
	val_first_layer_slit_angle: FloatProperty(name='First Layer Slit Angle', default=0, min=-math.pi, max=math.pi * 2, subtype='ANGLE', unit='ROTATION')

	# ワイヤーフレーム表示
	val_wireframe: BoolProperty(name='Wireframe', default=True)



	def invoke(self, context, event):
		return self.execute(context)



	def draw(self, context):
		col = self.layout.column()

		col_create_method = col.column(align=True)
		col_create_method.prop(self, 'val_create_method', expand=False)
		col_create_method.enabled = self.enable_create_method
		col_keep_modifier = col_create_method.column(align=True)
		col_keep_modifier.prop(self, 'val_keep_modifier', expand=False)
		col_keep_modifier.enabled = self.val_create_method == self.CREATE_METHOD_BOOLEAN

		col.separator()

		row = col.row(align=True)
		row.prop(self, 'val_type', expand=True)
		col.separator()

		row = col.row(align=True)
		row.prop(self, 'val_sizes', expand=True)
		col.separator()

		col.prop(self, 'val_nut_diameter')
		col.prop(self, 'val_screw_hole_diameter')
		col.prop(self, 'val_layer_thickness')
		col.separator()

		col.label(text='Clearances')
		col.prop(self, 'val_nut_hole_clearance')
		col.prop(self, 'val_screw_hole_clearance')
		col.separator()

		col.label(text='Seam Avoidance Slit')
		row = col.row(align=True)
		row.prop(self, 'val_no_seam_slit_length', text='Depth')
		row.prop(self, 'val_no_seam_slit_width', text=romly_utils.translate('Thickness', 'IFACE'))	# 'Thickness'はBlender内部の辞書で『幅』に翻訳されてしまうので、自前で翻訳
		row = col.row(align=True)
		row.label(text='Count')
		row.prop(self, 'val_no_seam_slit_count', expand=True)
		col.separator()

		col.label(text='First Layer Slit')
		row = col.row(align=True)
		row.prop(self, 'val_first_layer_slit_length', text='Depth')
		row.prop(self, 'val_first_layer_slit_width', text=romly_utils.translate('Thickness', 'IFACE'))	# 'Thickness'はBlender内部の辞書で『幅』に翻訳されてしまうので、自前で翻訳
		row = col.row(align=True)
		row.prop(self, 'val_first_layer_slit_height', text='Height')
		row.prop(self, 'val_first_layer_slit_angle', text='Angle')
		col.separator()

		col.label(text='Mesh Settings')
		col_nut_hole = col.column(align=True)
		col_nut_hole.label(text='Nut Hole')
		row = col_nut_hole.row(align=True)
		row.prop(self, 'val_nut_hole_length_above', text='Depth')
		row.prop(self, 'val_nut_hole_length_below', text='Surplus')
		col.prop(self, 'val_screw_hole_length')
		col.prop(self, 'val_screw_hole_segments')
		col.prop(self, 'val_wireframe')




	def execute(self, context):
		# 現在選択されているオブジェクトを取得
		# 選択されているオブジェクトがない場合、作成方法は選択できなくなる
		active_obj = None
		if len(bpy.context.selected_objects) > 0:
			active_obj = bpy.context.selected_objects[0]
		self.enable_create_method = active_obj is not None
		if not self.enable_create_method:
			self.val_create_method = self.CREATE_METHOD_ONLY_OBJECT

		# 選択を解除。これをやっとかないとナット穴のオブジェクト作るときにbpy.ops.transform.rotateしてるので選択されてるのが全部回転してしまう。
		bpy.ops.object.select_all(action='DESELECT')

		obj = create_nut_hole_object(
			type=self.val_type,
			nut_diameter=self.val_nut_diameter + self.val_nut_hole_clearance * 2,
			screw_hole_diameter=self.val_screw_hole_diameter + self.val_screw_hole_clearance * 2,
			layer_thickness=self.val_layer_thickness,
			screw_hole_segments=self.val_screw_hole_segments,
			nut_hole_depth=self.val_nut_hole_length_above,
			nut_hole_surplus=self.val_nut_hole_length_below,
			screw_hole_length=self.val_screw_hole_length,
			seam_slit=SlitSize(length=self.val_no_seam_slit_length, thickness=self.val_no_seam_slit_width),
			seam_slit_count=1 if self.val_no_seam_slit_count == '1' else 6,
			first_layer_slit=SlitSize(length=self.val_first_layer_slit_length, thickness=self.val_first_layer_slit_width, height=self.val_first_layer_slit_height),
			first_layer_slit_angle=self.val_first_layer_slit_angle)

		# 名前
		obj.name = get_nut_hole_object_name(self.val_nut_diameter)

		# 3Dカーソルの位置へ
		obj.location = bpy.context.scene.cursor.location

		# ワイヤーフレーム表示
		obj.display_type = 'WIRE' if self.val_wireframe else 'TEXTURED'

		if self.val_create_method == self.CREATE_METHOD_ONLY_OBJECT:

			# 選択
			obj.select_set(state=True)
			bpy.context.view_layer.objects.active = obj

			return {'FINISHED'}

		else:
			# 選択されているオブジェクトにブーリアンモデファイアを適用
			if active_obj:
				if self.val_keep_modifier:
					romly_utils.apply_boolean_object(active_obj, obj, apply=False, unlink=False);
				else:
					romly_utils.apply_boolean_object(active_obj, obj);
				return {'FINISHED'}
			else:
				romly_utils.report(self, 'WARNING', msg_key='Please select the object to which the modifier is to be applied')
				return {'CANCELLED'}












class ROMLYADDON_MT_romly_add_mesh_menu_parent(bpy.types.Menu):
	bl_idname = 'ROMLYADDON_MT_romly_add_mesh_menu_parent'
	bl_label = 'Romly'
	bl_description = 'Romly Addon Menu'



	def draw(self, context):
		layout = self.layout
		layout.operator(ROMLYADDON_OT_add_nut_hole.bl_idname, text=bpy.app.translations.pgettext_iface('Add Nut Hole'), icon='SEQ_CHROMA_SCOPE')









# 新規作成メニューに登録
def menu_func(self, context):
	self.layout.separator()
	self.layout.menu(ROMLYADDON_MT_romly_add_mesh_menu_parent.bl_idname, icon='NONE')





classes = [
	ROMLYADDON_OT_add_nut_hole,
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
	# 既に登録されていないかのチェック。テキストエディタから直接実行する時に必要
	# if 'bpy' in locals():
	# 	unregister()
	register()
