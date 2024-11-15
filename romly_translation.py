# 翻訳辞書
TRANSLATION_DICT = {
	'ja_JP': {
		# Add Box
		('*', 'Add Box'): '直方体を作成',
		('*', 'Construct a cuboid mesh'): '直方体のメッシュを作成します',
		('*', 'Set the X coordinate of the origin to the left surface'): '原点のX座標を左面に設定します',
		('*', 'Set the X coordinate of the origin to the center'): '原点のX座標を中心に設定します',
		('*', 'Set the X coordinate of the origin to the right surface'): '原点のX座標を右面に設定します',
		('*', 'Set the Y coordinate of the origin to the front surface'): '原点のY座標を正面に設定します',
		('*', 'Set the Y coordinate of the origin to the center'): '原点のY座標を中心に設定します',
		('*', 'Set the Y coordinate of the origin to the back surface'): '原点のY座標を背面に設定します',
		('*', 'Set the Z coordinate of the origin to the top surface'): '原点のZ座標を上面に設定します',
		('*', 'Set the Z coordinate of the origin to the center'): '原点のZ座標を中心に設定します',
		('*', 'Set the Z coordinate of the origin to the bottom surface'): '原点のZ座標を底面に設定します',
		('*', 'Size of the cuboid'): '直方体の大きさ',
		('*', 'X coordinate of the origin'): '原点のX座標',
		('*', 'Y coordinate of the origin'): '原点のY座標',
		('*', 'Z coordinate of the origin'): '原点のZ座標',

		# Add Donut Cylinder
		('*', 'Add Donut Cylinder'): '中空の円柱を作成',
		('*', 'Construct a donut cylinder mesh'): '中空構造の円柱のメッシュを作成します',
		('*', 'How to specify its size'): 'サイズを指定する方法',
		('*', 'Diameter & Hole Diameter'): '直径と穴径',
		('*', 'Specify its size by the diameter and the hole diameter'): '直径と穴径でサイズを指定します',
		('*', 'Diameter & Thickness'): '直径と厚み',
		('*', 'Specify its size by the diameter and the thickness'): '直径と厚みでサイズを指定します',
		('*', 'Hole Diameter & Thickness'): '穴径と厚み',
		('*', 'Specify its size by the hole diameter and the thickness'): '穴径と厚みでサイズを指定します',
		('*', 'The outer diameter of the cylinder'): '円柱の外径',
		('*', 'Hole Diameter'): '穴径',
		('*', 'Diameter of the hole'): '穴の直径',
		('*', 'Height of the cylinder'): '円柱の高さ',
		('*', 'The origin point of the cylinder mesh'): '円柱の原点位置',
		('*', 'The hole diameter must be smaller than the outer diameter'):
			'穴の直径を外径より大きくすることはできません',
		('*', 'The hole diameter must be larger than zero'):
			'穴の直径をマイナスにすることはできません',
		('*', 'Donut Cylinder'): '中空の円柱',

		# ルーローの多角形
		('*', 'Add Reuleaux Polygon'): 'ルーローの多角形を作成',
		('*', 'Construct a Reuleaux Polygon mesh'): 'ルーローの多角形のメッシュを作成します',
		('*', 'Number of sides for the polygon'): '多角形の辺の数',
		('*', 'The radius of the circumradius'): '外接円の半径',
		('*', 'Number of segments in each arc'): '円弧部の分割数',
		('*', 'Thickness of the extrusion'): '押し出しの厚み',
		('*', 'Revolution Angle'): '回転角度',
		('*', 'Angle of the rotational solid'): '回転体の角度',
		('*', 'Revolve Segments'): '回転体の分割数',
		('*', 'Number of segments in the revolutional solid'): '回転体の分割数',
		('*', 'Reuleaux Triangle'): 'ルーローの三角形',
		('*', 'Reuleaux-ish Square'): 'ルーローもどきの四角形',
		('*', 'Reuleaux Pentagon'): 'ルーローの五角形',
		('*', 'Reuleaux-ish Hexagon'): 'ルーローもどきの六角形',
		('*', 'Reuleaux Heptagon'): 'ルーローの七角形',
		('*', 'Reuleaux-ish Octagon'): 'ルーローもどきの八角形',
		('*', 'Reuleaux Nonagon'): 'ルーローの九角形',
		('*', 'Reuleaux-ish Decagon'): 'ルーローもどきの十角形',
		('*', 'Reuleaux Hendecagon'): 'ルーローの十一角形',
		('*', 'Reuleaux-ish Dodecagon'): 'ルーローもどきの十二角形',
		('*', 'Reuleaux Tridecagon'): 'ルーローの十三角形',
		('*', 'Reuleaux-ish Tetradecagon'): 'ルーローもどきの十四角形',
		('*', 'Reuleaux Pentadecagon'): 'ルーローの十五角形',
		('*', 'Reuleaux-ish Hexadecagon'): 'ルーローもどきの十六角形',
		('*', 'Reuleaux Heptadecagon'): 'ルーローの十七角形',
		('*', 'Reuleaux-ish Octadecagon'): 'ルーローもどきの十八角形',
		('*', 'Reuleaux Enneadecagon'): 'ルーローの十九角形',
		('*', 'Reuleaux-ish Icosagon'): 'ルーローもどきの二十角形',

		# ルーローの四面体関連
		('*', 'Add Reuleaux Tetrahedron'): 'ルーローの四面体を作成',
		('*', 'Construct a Reuleaux Tetrahedron mesh'): 'ルーローの四面体のメッシュを作成します',
		('*', 'The radius of spheres that construct Reuleaux Tetrahedron (Edge length of Regular Tetrahedron)'): 'ルーローの四面体を構成する球の半径（正四面体の辺の長さ）です',
		('*', 'Build Method'): '構築方法',
		('*', 'How to construct Reuleaux Tetrahedron mesh'): 'ルーローの四面体のメッシュを構築する方法',
		('*', 'Calc Vertices'): '頂点を計算',
		('*', 'Use UV spheres intersection part. It collapses when the number of segments/ring count is few'):
			'UV球の交差部分を取ります。セグメント数が少ないと破綻します',
		('*', 'Use Ico spheres intersection part. It collapses when the number of subdivisions is few'):
			'ICO球の交差部分を取ります。分割数が少ないと破綻します',
		('*', "Calculate vertex positions without using spheres. It won't collapse even if the number of subdivisions is few"):
			'球を使わずに頂点を計算します。少ないセグメント数でも破綻しません',
		('*', 'The number of UV spheres segments'): 'UV球のセグメント数',
		('*', 'The number of UV spheres ring counts'): 'UV球のリングの数',
		('*', 'The number of ICO spheres subdivisions / Mesh subdivisions'): 'ICO球の分割数 / メッシュの分割数',
		('*', 'Triangulate quad faces'): '四角形の面を三角形に分割します',
		('*', 'Bottom Face'): '底面 ',
		('*', 'Apex'): '頂点',
		('*', 'Set mesh origin to its center.'):
			'メッシュの原点を中心に設定します',
		('*', 'Set mesh origin to its bottom face center.'):
			'メッシュの原点を底面の中心に設定します',
		('*', 'Set mesh origin to its apex.'):
			'メッシュの原点を頂点に設定します',
		('*', 'Regular Tetrahedron'): '正四面体',
		('*', 'Reuleaux Tetrahedron'): 'ルーローの四面体',

		# オロイド関連
		('*', 'Add Oloid'): 'オロイドを作成',
		('*', 'Oloid'): 'オロイド',
		('*', 'Anti-Oloid'): 'アンチオロイド',
		('*', 'Construct an Oloid mesh'): 'オロイドのメッシュを作成します',
		('*', "The circles radius that construct the Oloid"): 'オロイドを構成する円の半径',
		('*', 'The number of vertices in each circle that construct the Oloid. The actual number will be much fewer because some of them are deleted during construction'):
			'オロイドを構成する円の頂点数。一部は構築中に削除されるため、実際の数はより少なくなります',
		('*', 'Constructs a normal Oloid'): '通常のオロイドを作成します',
		('*', 'Constructs an Anti-Oloid'): 'アンチオロイドを作成します',
		('*', 'The type of the Oloid'): '作成するオロイドの種類',
		('*', 'The thickness of the Anti-Oloid'): 'アンチオロイドの厚み',
		('*', 'The number of loop cuts of long faces. Subdivide it more solve the face distortion'):
			'細長い面のループカット数。細分化すると面の歪みが少なくなります',
		('*', 'The bevel width of the Anti-Oloid'): 'アンチオロイドのベベル幅',
		('*', 'The number of segments in the bevel of the Anti-Oloid'): 'アンチオロイドのベベルのセグメント数',
		('*', 'Keep Modifiers'): 'モデファイアを維持',
		('*', "Keep modifiers if it's checked"): 'オンの場合、モデファイアをそのままにします',

		# スフェリコン関連
		('*', 'Add Sphericon'): 'スフェリコンを作成',
		('*', 'The number of vertices in the polygon that constructs the Sphericon'):
			'スフェリコンの元になる多角形の頂点数',
		('*', 'How many rotations should the shape be offset by on each side to create a sphericon'):
			'形状を左右で何回転ずらしてスフェリコンを作るか',
		('*', 'Diagonal Length'): '対角線の長さ',
		('*', 'The diagonal length of the Sphericon'): 'スフェリコンの対角線の長さ',
		('*', 'The number of segments in the conic parts of the Sphericon'): 'スフェリコンの円錐部分のセグメント数',

		# MARK: クロソイド曲線関連
		('*', 'Add Clothoid Curve'): 'クロソイド曲線を作成',
		('*', 'Construct a Clothoid Curve'): 'クロソイド曲線を作成します',
		('*', 'Add Clothoid Corner Plate'): 'クロソイド角丸板を作成',
		('*', 'Construct a Clothoid Corner Plate'): 'クロソイド角丸板を作成します',
		('*', 'Curve Specification Method'): '曲線の指定方法',
		('*', 'Input Clothoid Parameter and Curve Length to determine the clothoid curve.'):
			'クロソイドパラメータと曲線長を入力してクロソイド曲線を決定します。',
		('*', 'Input Curve Length and Clothoid Parameter to determine the clothoid curve.'):
			'曲線長とクロソイドパラメータを入力してクロソイド曲線を決定します。',
		('*', 'Input Curve Radius and Clothoid Parameter to determine the clothoid curve.'):
			'曲線半径とクロソイドパラメータを入力してクロソイド曲線を決定します。',
		('*', 'Curve Radius'): '曲線半径',
		('*', 'Curve Length'): '曲線長',
		('*', 'Clothoid Parameter'): 'クロソイドパラメータ',
		('*', 'Rectangle Size'): '矩形サイズ',
		('*', 'Thickness'): '厚み',
		('*', 'Curve Vertices'): '曲線の頂点数',
		('*', 'Arc Vertices'): '円弧の頂点数',
		('*', 'Angle of Circular Arc'): '円弧の角度',
		('*', 'Total width(height) of rounded corner'): '角丸部全体の幅（高さ）',
		('*', 'Clothoid Curve'): 'クロソイド曲線',
		('*', 'Clothoid Corner Plate'): 'クロソイド角丸板',
		('*', 'Construct on'): '作成する平面',
		('*', 'Cunstructs a curve on the XY Plane'): '曲線をXY平面に作成します',
		('*' ,'Cunstructs a curve on the XZ Plane'): '曲線をXZ平面に作成します',
		('*', 'Cunstructs a curve on the YZ Plane'): '曲線をYZ平面に作成します',
		('*', 'Cunstructs a curve on the View Plane'): '曲線をビュー平面に作成します',

		# ねじ関連
		('*', 'Add JIS Screw'): 'ねじを作成',
		('*', 'Cunstruct a JIS standard screw'): 'JIS規格のネジを追加します',
		('*', 'Head Shape'): 'ネジ頭の形状',
		('*', 'Pan Head'): 'なべネジ',
		('*', 'Flat Head'): '皿ネジ',
		('*', 'Hexagon Head'): '六角',
		('*', 'No Screw Head'): 'ネジ頭なし',
		('*', 'Pan Head Screw'): 'なべネジ',
		('*', 'Flat Head Screw'): '皿ネジ',
		('*', 'Hexagon Head Screw'): '六角ボルト',
		('*', 'Set length to 4mm'): '長さを4mmにします',
		('*', 'Set length to 6mm'): '長さを6mmにします',
		('*', 'Set length to 8mm'): '長さを8mmにします',
		('*', 'Set length to 10mm'): '長さを10mmにします',
		('*', 'Set length to 15mm'): '長さを15mmにします',
		('*', 'Set length to 20mm'): '長さを20mmにします',
		('*', 'Set length to 25mm'): '長さを25mmにします',
		('*', 'Fully Threaded'): '全ネジ',
		('*', 'Partially Threaded'): '半ネジ',
		('*', 'Specify Length'): '長さ指定',
		('*', 'Partially Threaded (Specify Length)'): '半ネジ（長さ指定）',
		('*', 'Unthreaded Length'): 'ネジ切りなし部分の長さ',
		('*', "It's a screw towards Z minus direction"): 'マイナスZ方向に締まるネジです',
		('*', "It's a screw towards Z plus direction"): 'プラスZ方向に締まるネジです',
		('*', "It's a screw towards Y minus direction"): 'マイナスY方向に締まるネジです',
		('*', "It's a screw towards Y plus direction"): 'プラスY方向に締まるネジです',
		('*', "It's a screw towards X minus direction"): 'マイナスX方向に締まるネジです',
		('*', "It's a screw towards X plus direction"): 'プラスX方向に締まるネジです',
		('*', 'Head Diameter'): 'ネジ頭の径',
		('*', 'Head Height'): 'ネジ頭の高さ',
		('*', 'Flat Head Diameter'): '皿ネジのネジ頭径',
		('*', 'Thickness of Flat Head Screw Edge'): '皿ネジの縁の厚み',
		('*', "Hexagon head's diagonal length"): '六角ボルトの頭部対角距離',
		('*', 'Phillips Head Slit'): '十字穴',
		('*', 'Phillips Width'): '十字穴の幅',
		('*', 'Phillips Slit Depth'): '十字穴の深さ',
		('*', 'Phillips Rotation'): '十字穴の回転',
		('*', 'The length of the unthreaded part'): 'ネジ切りなし部分の長さ',
		('*', 'The length of the threaded part'): 'ネジ切り部分の長さ',
		('*', 'Set specs to M2 size'): 'M2サイズにします',
		('*', 'Set specs to M2.5 size'): 'M2.5サイズにします',
		('*', 'Set specs to M3 size'): 'M3サイズにします',
		('*', 'Set specs to M4 size'): 'M4サイズにします',
		('*', 'Set specs to M5 size'): 'M5サイズにします',
		('*', 'Set specs to M6 size'): 'M6サイズにします',
		('*', 'Set specs to M8 size'): 'M8サイズにします',
		('*', 'Shaft Diameter'): '芯の直径',
		('*', 'Screw Length'): 'ネジの長さ',
		('*', 'Threaded'): 'ねじ切り',
		('*', 'The distance between two adjacent threads'): 'ネジの山と山の間の距離',
		('*', 'Thread Lead'): 'リード',
		('*', 'How many times the pitch distance does the screw advance when turned once'):
			'ネジを一回転させたときにピッチの何倍進むか',
		('*', 'Thread Depth'): 'ねじ切りの深さ',
		('*', 'The depth of each thread'): 'ねじ切りの深さ',
		('*', 'The direction of the screw'): 'ネジの方向',
		('*', 'Head Bevel Segments'): 'ネジ頭のベベルのセグメント数',
		('*', 'Thread Bevel Segments'): 'ねじ山のベベルのセグメント数',
		('*', 'Chamfering Segments of Hexagon Head'): '六角ボルトの面取りのセグメント数',
		('*', 'The length of the unthreaded part cannot be longer than the total length'):
			'ネジ切りのない部分の長さを全長より長くすることはできません',
		('*', 'Pan Head Screw'): 'なべネジ',
		('*', 'Flat Head Screw'): '皿ネジ',
		('*', 'Hexagon Head Screw'): '六角ボルト',
		('*', 'Screw'): 'ネジ',
		('*', 'Mesh Settings'): 'メッシュ設定',

		# ナット
		('*', 'Add JIS Nut'): 'ナットを作成',
		('*', 'Cunstruct a JIS standard nut'): 'JIS規格のナットを追加します',
		('*', 'Type-1'): '一種',
		('*', 'Type-2'): '二種',
		('*', 'Type-3'): '三種',
		('*', 'The nut chamfered on one side only'): '片面のみ面取りしたナットです',
		('*', 'The nut chamfered on both side'): '両面を面取りしたナットです',
		('*', 'Thinner nut chamfered on both side'): '両面を面取りした薄いナットです',
		('*', 'Nut Diameter'): 'ナットの外径',
		('*', 'The thickness of the nut'): 'ナットの厚み',
		('*', 'Top Chamfering'): '上面の面取り',
		('*', 'Bottom Chamfering'): '底面の面取り',
		('*', 'Thread Segments'): 'ねじ切りのセグメント数',
		('*', 'Chamfering Segments'): '面取りのセグメント数',
		('*', 'Nut Corner Segments'): 'ナットの角のセグメント数',
		('*', 'The nut hole diameter must be smaller than the diameter'):
			'穴の直径をナットの外径より大きくすることはできません',
		('*', 'Nut'): 'ナット',

		# アルミフレーム関連
		('*', 'Add Aluminium Extrusion'): 'アルミフレームを作成',
		('*', 'Construct an aluminum extrusion'): 'アルミフレームを作成します',
		('*', 'The length of the extrusion'): 'アルミフレームの長さ',
		('*', 'Set length to 100 mm'): '長さを100mmに設定します',
		('*', 'Set length to 150 mm'): '長さを150mmに設定します',
		('*', 'Set length to 200 mm'): '長さを200mmに設定します',
		('*', 'Set length to 250 mm'): '長さを250mmに設定します',
		('*', 'Set length to 300 mm'): '長さを300mmに設定します',
		('*', 'Set length to 400 mm'): '長さを400mmに設定します',
		('*', 'Set length to 500 mm'): '長さを500mmに設定します',
		('*', 'Template'): '規定サイズ',
		('*', 'Specs'): '寸法',
		('*', 'Frame Size'): '角数',
		('*', 'The basic frame size'): 'アルミフレームの基本サイズ',
		('*', 'X Slots'): '溝の数(横)',
		('*', 'The number of slots in the X direction'): '横方向の溝の数（列数）',
		('*', 'Y Slots'): '溝の数(縦)',
		('*', 'The number of slots in the Y direction'): '縦方向の溝の数（列数）',
		('*', 'Slot Width'): '溝の幅',
		('*', 'The width of the slot'): '溝の幅',
		('*', 'Inner Slot Width'): '溝の内部幅',
		('*', 'The inner width of the slot'): '溝の内部の幅',
		('*', 'Core Width'): '芯部分の幅',
		('*', 'The width of the core part'): '芯部分の幅',
		('*', 'Wall Thickness'): '壁の厚み',
		('*', 'The thickness of the walls sandwiching the slot'): '溝の両側の壁の厚み',
		('*', 'Middle Wall Thickness'): '中間列の壁の厚み',
		('*', 'The thickness of the walls in the middle column'): '中間列の壁の厚み',
		('*', 'Center Hole Diameter'): '中心の穴の直径',
		('*', 'The diameter of the center hole'): '中心の穴の直径',
		('*', 'X Bone Thickness'): 'X部分の厚み',
		('*', 'The thickness of the X bone'): 'X部分の厚み',
		('*', 'Diameter'): '直径',
		('*', 'Corner Holes'): '四隅の穴',
		('*', 'The distance between corner holes'): '四隅の穴間の距離',
		('*', 'Corner Bevel'): '角のアール',
		('*', 'The bevel width of the corner bevels'): '角のアールのベベル幅',
		('*', 'Hole Segments'): '穴のセグメント数',
		('*', 'The number of segments in the holes'): '各穴のセグメント数',
		('*', 'Bevel Segments'): 'アールのセグメント数',
		('*', 'The number of segments in the corner bevels'): '角のアールのセグメント数',

		# Add Linear Guide Rail
		('*', 'Add Linear Guide Rail'): 'リニアガイドレールを追加',
		('*', 'Construct a Rail for Linear Guide'): 'リニアガイドのレールを作成します',
		('*', 'Set specs to MGN05 size'): '各寸法をMGN05サイズに設定します',
		('*', 'Set specs to MGN07 size'): '各寸法をMGN07サイズに設定します',
		('*', 'Set specs to MGN09 size'): '各寸法をMGN09サイズに設定します',
		('*', 'Set specs to MGN12 size'): '各寸法をMGN12サイズに設定します',
		('*', 'Set specs to MGN15 size'): '各寸法をMGN15サイズに設定します',
		('*', 'Set specs to MGW05 size'): '各寸法をMGW05サイズに設定します',
		('*', 'Set specs to MGW07 size'): '各寸法をMGW07サイズに設定します',
		('*', 'Set specs to MGW09 size'): '各寸法をMGW09サイズに設定します',
		('*', 'Set specs to MGW12 size'): '各寸法をMGW12サイズに設定します',
		('*', 'Set specs to MGW15 size'): '各寸法をMGW15サイズに設定します',
		('*', 'Outer Hole Depth'): '外側の穴の深さ',
		('*', 'Hole Pitch'): '穴の間隔',
		('*', 'First Hole Offset'): '最初の穴のオフセット',
		('*', 'Slit'): '溝',
		('*', 'Slit Diameter'): '溝の直径',
		('*', 'Slit Segments'): '溝のセグメント数',
		('*', 'Width of the rail'): 'レールの幅',
		('*', 'Height (Thickness) of the rail'): 'レールの高さ（厚み）',
		('*', 'Outer Diameter of each hole'): '各穴の外側の直径',
		('*', 'Inner Diameter of each hole'): '各穴の内側の直径',
		('*', 'Depth of outer hole'): '外側の穴の深さ',
		('*', 'Full length of the rail'): 'レールの全長',
		('*', 'Position of the slits (from the surface)'): '溝の位置（表面からの距離）',
		('*', 'Linear Guide Rail'): 'リニアガイドレール',
		('*', 'Weight'): '重量',

		# MARK: Add Linear Guide Block
		('*', 'Add Linear Guide Block'): 'リニアガイドブロックを追加',
		('*', 'Construct a Block for Linear Guide'): 'リニアガイドのブロックを作成します',
		('*', 'W Width'): 'W 幅',
		('*', 'L Length'): 'L 長さ',
		('*', 'L1 Metal Part Length'): 'L1 金属部長さ',
		('*', 'H Total Height'): 'H 全高',
		('*', 'H1 Bottom Space'): 'H1 下部スペース',
		('*', 'N Rail Side Width'): 'N レール脇幅',
		('*', 'l Depth'): 'l 深さ',
		('*', 'Screw Holes'): 'ネジ穴',
		('*', 'Horizontal Distance'): '水平距離',
		('*', '[B] Horizontal distance (perpendicular to the rail) between the screw holes'):
			'[B] ネジ穴の水平（レールと垂直）方向の距離',
		('*', 'Vertical Distance'): '垂直距離',
		('*', '[C] Vertical distance (parallel to the rail) between the screw holes'):
			'[C] ネジ穴の垂直（レールと並行）方向の距離',
		('*', 'Rail Height'): 'レール高',
		('*', '[HR] Height of the linear guide rail. Used to create indentations in the block'):
			'[HR] リニアガイドレールの高さ。ブロックのくぼみを作るために使用される',
		('*', 'Rail Clearance'): 'レールとブロック間の遊び',
		('*', 'Clearance between the block and linear guide rail. The height of indentation of the block will be the total of this value and Rail Height'):
			'ブロックとリニアガイドレール間の遊び。ブロックのくぼみの高さはこの値とレールの高さの合計になります',
		('*', 'End Seal Thickness'): 'エンドシールの厚み',
		('*', 'Thickness of the end seal (the red part on top and bottom)'): 'エンドシール（上下の赤い部分）の厚み',
		('*', 'Block Bevel Width'): 'ブロックのベベル幅',
		('*', 'Width of the block (perpendicular size to the rail)'):
			'ブロックの幅（レールと垂直方向の大きさ）',
		('*', 'Length of the block (parallel size to the rail)'):
			'ブロックの長さ（レールと平行方向の大きさ）',
		('*', 'Length of the middle metal part'): '中央の金属部の長さ',
		('*', 'Height to the block surface from the rail bottom'): 'レール底面からブロック表面までの高さ',
		('*', 'Height to the block bottom from the rail bottom'): 'レール底面からブロック底面までの高さ',
		('*', 'Width of the both sides part of the rail'): 'レールの両脇の部分の幅',
		('*', 'Depth of the screw holes'): 'ネジ穴の深さ',
		('*', "Thread screw holes if it's checked"): 'チェックすると、ネジ穴にねじ切り加工します',
		('*', 'Pitch of the screw threads'): 'ネジ穴のねじ切りのピッチ',
		('*', 'Depth of threads of screw holes'): 'ネジ穴のねじ切りの深さ',
		('*', 'Grease Holes'): 'グリース穴',
		('*', '[H2] Distance to the grease hole on the end seal (the red part) from the block surface'): '[H2] エンドシール（赤い部分）のグリース穴の中心までのブロック表面からの距離',
		('*', '[Gn] Diameter of the grease hole in the end seal (the red part)'): '[GN] エンドシール（赤い部分）のグリース穴の直径',
		('*', 'Set specs to MGN05C size'): '各寸法をMGN05Cサイズに設定します',
		('*', 'Set specs to MGN05H size'): '各寸法をMGN05Hサイズに設定します',
		('*', 'Set specs to MGN07C size'): '各寸法をMGN07Cサイズに設定します',
		('*', 'Set specs to MGN07H size'): '各寸法をMGN07Hサイズに設定します',
		('*', 'Set specs to MGN12C size'): '各寸法をMGN12Cサイズに設定します',
		('*', 'Set specs to MGN12H size'): '各寸法をMGN12Hサイズに設定します',
		('*', 'Set specs to MGN15C size'): '各寸法をMGN15Cサイズに設定します',
		('*', 'Set specs to MGN15H size'): '各寸法をMGN15Hサイズに設定します',
		('*', 'Set specs to MGW05C size'): '各寸法をMGW05Cサイズに設定します',
		('*', 'Set specs to MGW05CL size'): '各寸法をMGW05CLサイズに設定します',
		('*', 'Set specs to MGW07C size'): '各寸法をMGW07Cサイズに設定します',
		('*', 'Set specs to MGW07H size'): '各寸法をMGW07Hサイズに設定します',
		('*', 'Set specs to MGW12C size'): '各寸法をMGW12Cサイズに設定します',
		('*', 'Set specs to MGW12H size'): '各寸法をMGW12Hサイズに設定します',
		('*', 'Set specs to MGW15C size'): '各寸法をMGW15Cサイズに設定します',
		('*', 'Set specs to MGW15H size'): '各寸法をMGW15Hサイズに設定します',
		('*', 'Linear Guide Block'): 'リニアガイドブロック',

		# MARK: Add Coupling
		('*', 'Add Coupling'): 'カップリングを追加',
		('*', 'Construct a Coupling'): 'カップリングを作成',
		('*', '[D] The outer diameter of the Coupling'): '[D] カップリングの外径',
		('*', '[L] The length (height) of the Coupling'): '[L] カップリングの長さ（高さ）',
		('*', 'The inner diameter 1 of the Coupling'): 'カップリングの内径1',
		('*', 'The inner diameter 2 of the Coupling'): 'カップリングの内径2',
		('*', 'Set Screw Holes'): 'ネジ穴を作る',
		('*', 'Make set screw holes on the Coupling.'): 'カップリングに止めネジ穴を作成します',
		('*', 'The distance to the center of the set screw holes from both ends of the coupling'): 'カップリングの両端からネジ穴の中心までの距離',
		('*', 'Angle on the Z-axis between each pair of opposing set screws'): '対になる止めネジ同士のZ軸の角度',
		('*', 'Diameter of the set screw holes'): '止めネジ穴の直径',
		('*', 'Pitch of the set screw hole threads'): '止めネジ穴のねじ切りのピッチ',
		('*', 'Depth of the set screw hole threads'): '止めネジ穴のねじ切りの深さ',
		('*', 'Helical Slit'): '螺旋スリット',
		('*', 'Make helical slit on the coupling'): 'カップリングに螺旋スリットを作成する',
		('*', 'The width of the helical slit'): '螺旋スリットの幅',
		('*', 'The rotation count of the slit'): '螺旋スリットの回転数',
		('*', 'Distance traveled per rotation of the slit'): '螺旋スリットの回転あたりの移動距離',
		('*', 'The bevel offset width of the edge of the coupling'): 'カップリングの辺のベベルオフセット幅',
		('*', 'The number of segments of the coupling'): 'カップリングのセグメント数',
		('*', 'The number of segments of the set screw holes'): '止めネジ穴のセグメント数',
		('*', 'The number of segments of the slit'): '螺旋スリットのセグメント数',
		('*', 'Coupling'): 'カップリング',

		# MARK: Add Lead Nut
		('*', 'Add Lead Nut'): 'リードナットを追加',
		('*', 'Construct a Lead Nut'): 'リードナットを作成',
		('*', 'Bevel Width'): 'ベベル幅',
		('*', 'Flange'): '鍔',
		('*', "Specify the width of the flange when it is not circular. If it's a complete circle, set this value to zero"): 'プレート部分が円形ではない場合の幅を指定します。円形のプレートの場合は0にして下さい',
		('*', 'Shaft Length Above'): '芯の長さ（上部）',
		('*', 'Shaft Length Below'): '芯の長さ（下部）',
		('*', 'Total Length (Height): {value}'): '全体の長さ（高さ）: {value}',

		# Add Lead Screw
		('*', 'Add Lead Screw'): 'リードスクリューを追加',
		('*', 'Construct a Lead Screw'): 'リードスクリューを作成します',
		('*', 'The length of the lead screw'): 'リードスクリューの長さ',
		('*', 'Major Dia.'): '外径',
		('*', 'The outer diameter of the lead screw'): 'リードスクリューの外径',
		('*', 'Minor Dia.'): '谷径',
		('*', 'The thread valley diameter of the lead screw'): 'リードスクリューのねじ切りの谷部分の直径',
		('*', 'The pitch of the lead screw'): 'リードスクリューのピッチ',
		('*', 'Starts'): '多条',
		('*', 'The number of thread starts of the lead screw'): 'リードスクリューの多条数',
		('*', 'Thread Angle'): 'ねじ山の角度',
		('*', 'The angle of the thread'): 'リードスクリューのねじ山の角度',
		('*', 'Lead: {value}'): 'リード: {value}',

		# MARK: Add Compression Spring
		('*', 'Add Compression Spring'): '圧縮コイルばねを追加',
		('*', 'Construct a Compression Spring'): '圧縮コイルばねを作成します',
		('*', 'Wire Diameter'): '線径',
		('*', 'The diameter of the wire'): '線の直径',
		('*', 'Outer Diameter'): '外径',
		('*', 'The outer diameter of the spring'): 'ばねの外径',
		('*', 'The pitch of the spring'): 'ばねのピッチ',
		('*', 'Wire Segments'): '線のセグメント数',
		('*', 'The number of segments of the wire'): '線のセグメント数',
		('*', 'Dead Coils (Top)'): '座巻（上部）',
		('*', 'Dead Coils (Bottom)'): '座巻（下部）',
		('*', 'The number of dead coils at the top'): '上部の座巻数',
		('*', 'The number of dead coils at the bottom'): '下部の座巻数',
		('*', 'Coils'): '巻数',
		('*', 'Free Length'): '自由長',
		('*', 'Specify the free length of the spring'): '自由長を指定します',
		('*', 'Specify the number of coils to determine the spring length'): '巻数を指定して、ばねの長さを決定します',
		('*', 'The free length of the spring. This will be the total height of the spring'): 'ばねの自由長。これはばねの全高となります',
		('*', 'The number of active coils'): '有効巻数',
		('*', 'Outer Diameter Segments'): '外径に対するセグメント数',
		('*', 'The number of segments of the outer diameter'): '外径に対するセグメント数',
		('*', 'Right Hand Wind'): '右巻き',
		('*', 'Make the spring wind direction right hand wind (clockwise)'): 'ばね向きを右巻き（時計回り）にする',
		('*', 'Make the spring wind direction left hand wind (counter-clockwise)'): 'ばね向きを左巻き（反時計回り）にする',
		('*', 'Left Hand Wind'): '左巻き',
		('*', 'Ground Ends'): '端を研削',
		('*', 'Free Length: {value}'): '自由長: {value}',
		('*', 'Active Coils: {value}'): '有効巻数: {value}',

		# MARK: Add Pin Header
		('*', 'Add Pin Header'): 'ピンヘッダーを追加',
		('*', 'Construct a Pin Header'): 'ピンヘッダーを作成します',
		('*', 'Pin pitch of the pin header'): 'ピンヘッダーのピッチ',
		('*', 'Block Size'): 'ブロックサイズ',
		('*', 'Size of the pin header housing'): 'ハウジング部分のサイズ',
		('*', 'Pin Thickness'): 'ピンの太さ',
		('*', 'Pin Length (Above)'): 'ピンの長さ（上部）',
		('*', 'Pin Length (Below)'): 'ピンの長さ（下部）',
		('*', 'Block Concave Size'): 'ブロックの凹みのサイズ',
		('*', 'Size of the housing concave'): 'ハウジング部分の凹みのサイズ',
		('*', 'Number of Pins'): 'ピン数',
		('*', 'Rows'): '行',
		('*', 'Pin Total Length: {value}'): 'ピンの全長: {value}',
		('*', 'Pin Header {pitch}mm {rows}x{cols}'): 'ピンヘッダー {pitch}mm {rows}x{cols}',
		('*', 'Center Position Diameter'): '中心位置の直径',
		('*', 'The number of screw holes on one side. The total number of screw holes will be twice this value'): '片面のネジ穴の数。全ネジ穴の数はこの値の2倍になります',
		('*', 'The angle between each screw hole'): '各ネジ穴の間の角度',

		# Add Loadcell
		('*', 'Add Loadcell'): 'ロードセルを追加',
		('*', 'Construct a Loadcell'): 'ロードセルを作成します',
		('*', 'Screw Holes Distance'): 'ネジ穴間の距離',
		('*', 'Between Inner Holes'): '内側のネジ穴同士',
		('*', 'Between Front/Rear Holes'): '手前（後ろ）のネジ穴同士',
		('*', 'In the X Direction'): 'X軸方向',
		('*', 'Screw Hole Sizes'): 'ネジ穴のサイズ',
		('*', 'Front:'): '手前:',
		('*', 'Rear:'): '後ろ:',
		('*', 'Y-Origin'): '原点(Y軸)',
		('*', 'Z-Origin:'): '原点(Z軸)',
		('*', 'Front Screw Hole 1'): '手前のネジ穴1',
		('*', 'Front Screw Hole 2'): '手前のネジ穴2',
		('*', 'Front Screw Holes Center'): '手前のネジ穴の中央',
		('*', 'Rear Screw Hole 1'): '手前のネジ穴1',
		('*', 'Rear Screw Hole 2'): '手前のネジ穴2',
		('*', 'Rear Screw Holes Center'): '手前のネジ穴の中央',
		('*', 'Thin Part'): '細い部分',
		('*', 'Cutout'): '切り抜き',
		('*', 'Cutout Holes Diameter'): '切り抜きの穴の直径',
		('*', 'The diameter of the cutout holes'): '切り抜きの穴の直径',
		('*', 'Distance Between Cutout Holes'): '切り抜きの穴間の距離',
		('*', 'Cutout Bridge Height'): '切り抜きのブリッジ部の高さ',
		('*', 'Template:'): 'テンプレート:',
		('*', '5kg Size'): '5kgサイズ',
		('*', '1kg Size'): '1kgサイズ',
		('*', '500g Size'): '500gサイズ',
		('*', '100g Size'): '100gサイズ',
		('*', 'Width and length of the middle narrow part'): '中央の細い部分の幅と長さ',
		('*', 'Overall size of the loadcell'): 'ロードセルの全体の大きさ',
		('*', 'Y-axis distance between two cutout holes'): '切り抜きの穴のY軸方向の距離',
		('*', 'Z-axis height of the bridge between two cutout holes'): '2つの切り抜きの穴間のブリッジ部のZ軸方向の高さ',
		('*', 'The diameter of the center hole located between the two cutout holes'): '2つの切り抜きの穴の中央の穴の直径',
		('*', 'The distance between two innermost screw holes'): '内側の2つのネジ穴の間の距離',
		('*', 'The distance between two front/rear screw holes. Setting it to zero results in one screw hole at the front and one at the rear'): '手前（後ろ）の2つのネジ穴の間の距離。ゼロに設定すると、手前（後ろ）のネジ穴は一つになります',
		('*', 'The distance between each pair of horizontally aligned screw holes. Setting it to zero aligns the screw holes in a single row'): '水平に並んだネジ穴間の距離。ゼロに設定すると、ネジ穴は一列になります',
		('*', 'Size of the front screw holes'): '手前のネジ穴のサイズ',
		('*', 'Size of the rear screw holes'): '後ろのネジ穴のサイズ',
		('*', "Thread the front screw holes. You also need to check the 'Enable Threading'"): '手前のネジ穴をねじ切りします。『ねじ切りを有効にする』もチェックする必要があります',
		('*', "Thread the rear screw holes. You also need to check the 'Enable Threading'"): '後ろのネジ穴をねじ切りします。『ねじ切りを有効にする』もチェックする必要があります',
		('*', 'Cutout Hole Segments'): '切り抜きの穴のセグメント数',
		('*', 'The Y-axis origin position of the loadcell object'): 'ロードセルオブジェクトのY軸の原点位置',
		('*', 'The Z-axis origin position of the loadcell object'): 'ロードセルオブジェクトのZ軸の原点位置',
		('*', 'Checking this option enables threading settings for the front and rear screw holes'): 'チェックすると、前後のネジ穴のねじ切り設定が有効になります',
		('*', 'Enable Threading'): 'ねじ切りを有効にする',

		# Add Nut Hole
		('*', 'Add Nut Hole'): 'ナット穴を追加',
		('*', 'Construct a hole for a nut for 3D printing'): '3Dプリント用のナットの穴を作成します',
		('*', 'Create Method'): '作成方法',
		('*', 'Nut Hole'): 'ナット穴',
		('*', 'Surplus'): '余長',
		('*', 'Screw Hole Diameter'): 'ネジ穴の直径',
		('*', 'Screw Hole Length'): 'ネジ穴の長さ',
		('*', 'Only Tool Object'): 'ツールオブジェクトのみ',
		('*', 'Create a nut hole object for boolean modifier'):
			'ブーリアンモデファイア用のナット穴オブジェクトを作成します',
		('*', 'Create a nut hole for the selected object'):
			'選択されたオブジェクトにナットの穴を開けます',
		('*', 'Layer Thickness'): 'レイヤーの厚み',
		('*', 'Clearances'): '遊び',
		('*', 'Nut Diameter Clearance'): 'ナット外径の遊び',
		('*', 'Screw Hole Clearance'): 'ネジ穴の遊び',
		('*', 'Screw Hole Segments'): 'ネジ穴のセグメント数',
		('*', 'Seam Avoidance Slit'): 'シーム避けスリット',
		('*', 'Seam Avoidance Slit Depth'): 'シーム避けスリットの深さ',
		('*', 'Seam Avoidance Slit Thickness'): 'シーム避けスリットの厚み',
		('*', 'Seam Avoidance Slit Count'): 'シーム避けスリットの数',
		('*', 'Single Point'): '一箇所',
		('*', '6 Points'): '六箇所',
		('*', 'Sacrificial Layer'): '犠牲レイヤー',
		('*', 'Bridge Layer'): 'ブリッジ',

		# Select Edges on Fair Surface
		('*', 'Select Edges on Fair Surface'): '平面上にある辺を選択',
		('*', 'Select all edges on fair surface plane'): '平面上にある全ての辺を選択します',
		('*', 'Select edges when the angle between normals of the two surfaces sharing the edge is less than or equal to this value'):
			'辺を共有する2つの面の法線の角度が、この値以下になる時にその辺を選択します。',

		# Select Edges along Axis
		('*', 'Select Edges along Axis'): '軸に沿った辺を選択',
		('*', 'Select all edges along the axis'): '指定の軸に沿った全ての辺を選択します',

		# Add Constant Offset Array Modifier
		('*', 'Add Constant Offset Array Modifier'):
			'固定オフセットの配列モデファイアを追加',
		('*', 'Add an array modifier set to a constant offset'):
			'固定オフセットに設定された配列モデファイアを追加します',
		('*', 'Constant Offset Array'): '一定のオフセットの配列',

		# Add Weight Bevel Modifier
		('*', 'Add Weight Bevel Modifier'):
			'ウェイト制限のベベルモデファイアを追加',
		('*', 'Add a bevel modifier with its Limit Method set to Weight'):
			'制限方法をウェイトに設定したベベルモデファイアを追加します',
		('*', 'Weight Bevel'): 'ウェイト制限のベベル',

		# Clear Bevel Weight
		('*', 'Clear Bevel Weight'): 'ベベルウェイトをクリア',
		('*', 'Set the Bevel Weight of the all edges and vertices to zero'): '全ての辺と頂点のベベルウェイトを0にします',
		('*', 'Set the Bevel Weight of all edges to zero'): '全ての辺のベベルウェイトを0にします',
		('*', 'Set the Bevel Weight of all vertices to zero'): '全ての頂点のベベルウェイトを0にします',

		# Toggle Edges Bevel Weight
		('*', 'Toggle Edges Bevel Weight'): '辺のベベルウェイトをトグル',
		('*', "Toggle selected edges' bevel weight to 0 or 1"): '選択した辺のベベルウェイトを0または1に切り替えます',

		# Transform object aligning edge to axis
		('*', 'Rotate object aligning edge to axis'): '辺が軸に沿うようにオブジェクトを回転',
		('*', 'Rotate and translate the object to align the selected edge to the axis'): '選択した辺が軸に沿うようにオブジェクトを回転・移動します',
		('*', 'Rotate object to align selected edges to X-axis'): '選択した辺がZ軸に沿うようにオブジェクトを回転します',
		('*', 'Rotate object to align selected edges to Y-axis'): '選択した辺がZ軸に沿うようにオブジェクトを回転します',
		('*', 'Rotate object to align selected edges to Z-axis'): '選択した辺がZ軸に沿うようにオブジェクトを回転します',
		('*', 'Please select the object'): 'オブジェクトを選択して下さい',
		('*', 'Please select the edge'): '辺を選択して下さい',

		# Apply All Modifiers
		('*', 'Apply All Modifiers'): 'すべてのモデファイアを適用',
		('*', 'Apply all modifiers on the active object'):
			'アクティブなオブジェクトのすべてのモデファイアを適用します',
		('*', 'Please select the object to which the modifiers are to be applied'):
			'モデファイアを適用するオブジェクトを選択して下さい',
		('*', 'The object has no modifiers'):
			'オブジェクトにはモデファイアがありません',
		('*', '{count} modifiers were applied'): '{count}個のモデファイアを適用しました',

		# Toggle Viewport Display As
		('*', 'Toggle Viewport Display As'): 'ビューポート表示を切り替え',
		('*', 'Toggle Viewport Display As Wire/Textured'):
			'ビューポートでのオブジェクトの表示方法をテクスチャとワイヤーフレームで切り替えます',
		('*', 'Please select an object to operate'): '対象となるオブジェクトを選択して下さい',

		# Export as STL
		('*', 'Export Collection as STL'): 'コレクションをSTLファイルとしてエクスポート',
		('*', 'Export all meshes in this collection as an STL file. The sub collections that were excluded from the layer view will be excluded.'): 'このコレクションのすべてのメッシュをSTLファイルとして出力します。レイヤビューから除外されたブコレクションは含まれません',
		('*', 'Please save the active file first'): '先に編集中のファイルを保存して下さい',
		('*', 'The collection {collection} is exported to: {filename}'): 'コレクション {collection} を {filename} にエクスポートしました',
		('*', 'Export Selection as STL'): '選択項目をSTLファイルとしてエクスポート',
		('*', 'Export the selected objects as an STL file'): '選択されたオブジェクトをSTLファイルとしてエクスポートします',
		('*', 'The selection is exported to: {filename}'): '選択されているオブジェクトを {filename} にエクスポートしました',

		# Mil Size Panel
		('*', 'Mil Size'): 'Milサイズ',
		('*', 'Toggle Unit mm/mil(thou)'): 'mm/mil(thou) 単位切替',
		('*', 'Distance Between 2 Verts'): '2つの頂点間の距離',
		('*', 'Minimum Distance Between 2 Edges'): '2つの辺間の最小距離',

		# language_panel
		('*', 'Set blender language to specified language'): 'blenderを指定された言語に設定します',
		('*', 'The language was set to {language}'): '言語が {language} に設定されました',

		# Reload and Run Script
		('*', 'Reload and Run Script'): '再読み込みして実行',
		('*', 'Reload active script from disk and run'): 'アクティブスクリプトをディスクから再読み込みして実行します'
	},










	'fr_FR': {
		# ルーローの多角形
		('*', 'Add Reuleaux Polygon'): 'Ajouter Polygone de Reuleaux',
		('*', 'Reuleaux Triangle'): 'Triangle de Reuleaux',
		('*', 'Reuleaux-ish Square'): 'Carré de Reuleauxâtre',
		('*', 'Reuleaux Pentagon'): 'Pentagone de Reuleaux',
		('*', 'Reuleaux-ish Hexagon'): 'Hexagone de Reuleauxâtre',
		('*', 'Reuleaux Heptagon'): 'Heptagone de Reuleaux',
		('*', 'Reuleaux-ish Octagon'): 'Octogone de Reuleauxâtre',
		('*', 'Reuleaux Nonagon'): 'Ennéagone de Reuleaux',
		('*', 'Reuleaux-ish Decagon'): 'Décagone de Reuleauxâtre',
		('*', 'Reuleaux Hendecagon'): 'Hendécagone de Reuleaux',
		('*', 'Reuleaux-ish Dodecagon'): 'Dodécagone de Reuleauxâtre',
		('*', 'Reuleaux Tridecagon'): 'Triskaidecagone de Reuleaux',
		('*', 'Reuleaux-ish Tetradecagon'): 'Tetrakaidecagone de Reuleauxâtre',
		('*', 'Reuleaux Pentadecagon'): 'Pentakaidecagone de Reuleaux',
		('*', 'Reuleaux-ish Hexadecagon'): 'Hexakaidecagone de Reuleauxâtre',
		('*', 'Reuleaux Heptadecagon'): 'Heptakaidecagone de Reuleaux',
		('*', 'Reuleaux-ish Octadecagon'): 'Octakaidecagone de Reuleauxâtre',
		('*', 'Reuleaux Enneadecagon'): 'Ennéadécagone de Reuleaux',
		('*', 'Reuleaux-ish Icosagon'): 'Icosagone de Reuleauxâtre',

		# ルーローの四面体関連
		('*', 'Add Reuleaux Tetrahedron'): 'Ajouter Tétraèdre de Reuleaux',
		('*', 'Regular Tetrahedron'): 'Tétraèdre Régulier',
		('*', 'Reuleaux Tetrahedron'): 'Tétraèdre de Reuleaux',

		# オロイド関連
		('*', 'Add Oloid'): 'Ajouter Oloïde',
		('*', 'Oloid'): 'Oloïde',
		('*', 'Anti-Oloid'): 'Anti-Oloïde',

		# クロソイド曲線関連
		('*', 'Thickness'): 'Épaisseur',

		# ねじ関連
		('*', 'Add JIS Screw'): 'Ajouter vis JIS',
		('*', 'Screw'): 'Vis',

		# ナット
		('*', 'Add JIS Nut'): 'Ajouter écrou JIS',
		('*', 'Nut'): 'Écrou',

		# Add Coupling
		('*', 'Add Coupling'): 'Ajouter Accouplement',
		('*', 'Coupling'): 'Accouplement',

		# Add Lead Nut
		('*', 'Add Lead Nut'): 'Ajouter Écrou à vis mère',
		('*', 'Flange'): 'Bride',

		# Add Loadcell
		('*', 'Add Loadcell'): 'Ajouter Cellule de Charge',

		# language_panel
		('*', 'Set blender language to specified language'): 'Régler la langue du blender sur la langue spécifiée',
		('*', 'The language was set to {language}'): 'La langue a été réglée sur le {language}',

		# Reload and Run Script
		('*', 'Reload and Run Script'): 'Recharger et Exécuter le Script',
	},










	'de_DE': {
		('*', 'Pitch'): 'Steigung',

		# Add Loadcell
		('*', 'Add Loadcell'): 'Ebene Lastzelle',
	},
}