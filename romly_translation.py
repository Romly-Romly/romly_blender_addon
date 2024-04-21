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

		# クロソイド曲線関連
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
		('*', 'Threading'): 'ねじ切り',
		('*', 'Thread Pitch'): 'ピッチ',
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

		# Select Edges on Fair Surface
		('*', 'Select Edges on Fair Surface'): '平面上にある辺を選択',
		('*', 'Select all edges on fair surface plane'): '平面上にある全ての辺を選択します',
		('*', 'Select edges when the angle between normals of the two surfaces sharing the edge is less than or equal to this value'):
			'辺を共有する2つの面の法線の角度が、この値以下になる時にその辺を選択します。',

		# Add Constant Offset Array Modifier
		('*', 'Add Constant Offset Array Modifier'):
			'固定オフセットの配列モデファイアを追加',
		('*', 'Add an array modifier set to a constant offset'):
			'固定オフセットに設定された配列モデファイアを追加します',

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

		# language_panel
		('*', 'Set blender language to specified language'):
			'blenderを指定された言語に設定します',
		('*', 'The language was set to {language}'): '言語が {language} に設定されました',

		# Reload and Run Script
		('*', 'Reload and Run Script'): '再読み込みして実行',
		('*', 'Reload active script from disk and run'): 'アクティブスクリプトをディスクから再読み込みして実行します'
	},

	'fr_FR': {
		('*', 'Add Oloid'): 'Ajouter Oloïde',
		('*', 'Oloid'): 'Oloïde',
		('*', 'Anti-Oloid'): 'Anti-Oloïde',
		('*', 'The language was set to {language}'): 'La langue a été réglée sur le {language}',
	},
}
