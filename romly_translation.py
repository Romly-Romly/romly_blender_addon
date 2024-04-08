# 翻訳辞書
TRANSLATION_DICT = {
	'ja_JP': {
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
		('*', 'Construct an Oloid mesh'): 'オロイドのメッシュを作成します',
		('*', "The circles radius that construct the Oloid"): 'オロイドを構成する円の半径',
		('*', 'The number of vertices in each circle that construct the Oloid. The actual number will be much fewer because some of them are deleted during construction'): 'オロイドを構成する円の頂点数。一部は構築中に削除されるため、実際の数はより少なくなります',
	}
}
