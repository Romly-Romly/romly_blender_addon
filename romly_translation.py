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

		# Toggle Viewport Display As
		('*', 'Toggle Viewport Display As'): 'ビューポート表示を切り替え',
		('*', 'Toggle Viewport Display As Wire/Textured'):
			'ビューポートでのオブジェクトの表示方法をテクスチャとワイヤーフレームで切り替えます',
		('*', 'Please select an object to operate'): '対象となるオブジェクトを選択して下さい',

		# language_panel
		('*', 'Set blender language to specified language'):
			'blenderを指定された言語に設定します',

		# Reload and Run Script
		('*', 'Reload and Run Script'): '再読み込みして実行',
		('*', 'Reload active script from disk and run'): 'アクティブスクリプトをディスクから再読み込みして実行します'
	},

	'fr_FR': {
		('*', 'Add Oloid'): 'Ajouter Oloïde',
		('*', 'Oloid'): 'Oloïde',
		('*', 'Anti-Oloid'): 'Anti-Oloïde',
	},
}
