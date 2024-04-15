# romly_blender_addon

個人的に作成、使用している[Blender](https://www.blender.org/)用のスクリプトいろいろをアドオンにまとめたもの。<br>
動作確認したBlenderのバージョンは4.0です。<br>

## 含まれる機能

- メッシュ作成
	- 原点位置を設定可能な立方体([Add Box](#Add-Box))
	- 中空構造のシリンダー([Add Donut Cylinder](#add-donut-cylinder))
	- 十字架を掃引した形状([Add Cross Extrusion](#add-cross-extrusion))
	- ルーローの多角形([Add Reuleaux Polygon](#add-reuleaux-polygon))
	- ルーローの四面体([Add Reuleaux Tetrahedron](#add-reuleaux-tetrahedron))
	- スフェリコン([Add Sphericon](#add-sphericon))
	- オロイド／アンチオロイド([Add Oloid](#add-oloid))
	- アルミフレーム([Add Aluminum Extrusion](#add-aluminum-extrusion))
	- ピンヘッダー([Add Pin Header](#add-pin-header))
- すべてのモデファイアを適用([Apply All Modifiers](#apply-all-modifiers))
- 固定距離のArrayモデファイアを追加([Add Fixed Count Array Modifier](#add-fixed-count-array-modifier))
- オブジェクト／コレクションをSTL形式で簡単にエクスポート([Export Selection as STL](#export-selection-as-stl), [Export Collection as STL](#export-collection-as-stl))
- 平面上にある辺（溶解可能な辺）を選択([Select edges on Fair Surface](#select-edges-on-fair-surface))
- 言語設定を切り替えられるパネル([Language Panel](#language-panel))
- 【おまけ】blend1ファイルを再帰的に削除するPythonスクリプト([blend1_cleaner.py](#blend1_cleanerpy))

![romly_blender_addonで作成可能なオブジェクトの一部](images/support_objects.jpg)
作成可能なオブジェクトの一部





## インストール方法

1. Githubの**コード**ボタンからzipファイルをダウンロード
2. Blenderの**環境設定** → **Add-ons** → **Install** でダウンロードしたzipファイルを指定
3. インストール成功するとアドオンが表示されるので、有効化

## 使い方

### Add Box

*Add Menu*(<kbd>Shift+A</kbd>) → *Romly*

オブジェクトの原点位置を指定可能な直方体を追加します。Blenderで立方体を追加するのと同じですが、標準機能だと常に原点位置が立方体中心です。<br>
自分は原点を角や底面の中心などに修正してから使うことが多いのでスクリプトにまとめました。<br>
UVマップは無いのでご注意下さい。<br>

-----

### Add Donut Cylinder

*Add Menu*(<kbd>Shift+A</kbd>) → *Romly*

中空になっている円柱を追加します。直径／内径の指定の他、直径または内径と肉厚での指定もできます。さらにオブジェクトの原点を最初から底辺や上辺にできるので長さ指定も楽ちん。セグメント数は外側と内側で別々に設定できるので、六角形の円柱に丸い穴というような形状も作れます。<br>
これは[#軸の秤](https://twitter.com/search?q=%23%E8%BB%B8%E3%81%AE%E7%A7%A4&f=live)みたいもののケースをBlenderで作っていると、ネジ穴周りの設計で非常によく使う形状なのでスクリプトにまとめました。

-----

### Add Cross Extrusion

*Add Menu*(<kbd>Shift+A</kbd>) → *Romly*

![Add Cross Extrusion](images/add_cross_extrusion.png)

XY平面に描いた十字をZ方向に掃引した形状を作成します。十字は横方向、縦方向それぞれの棒の太さと長さを個別に設定できます。

こんな形何に使うんだって感じですが、昔Cherry MX対応のキーキャップを3Dプリントで作る時に、ソケット部分を削る形状を作るのに使ってました。

-----

### Add Reuleaux Polygon

*Add Menu(<kbd>Shift+A</kbd>) → *Romly*

![Add Reuleaux Polygon](images/add_reuleaux_polygon.jpg)

XY平面にルーローの多角形を作成します。正しくルーローの多角形になるのは辺の数が奇数の場合のみで、偶数の正多角形の時は反対側の辺の中点を中心とする円弧でそれっぽい形にしているだけです。

円弧部のセグメント数を指定でき、1にすると円弧無しの正多角形になります。

-----

### Add Reuleaux Tetrahedron

*Add Menu(<kbd>Shift+A</kbd>) → *Romly*

![Add Reuleaux Tetrahedron](images/add_reuleaux_tetrahedron.jpg)

ルーローの四面体を作成します。UV球またはICO球の共通部分を使って作成する方法と、頂点を計算して作成する方法を選択できます。前者の場合、メッシュの分割数が少ないと四面体の角が出ず形状が破綻してしまいます。
いずれの作成方法でも、分割数を最小にすれば通常の正四面体を作れます。

-----

### Add Sphericon

*Add Menu(<kbd>Shift+A</kbd>) → *Romly*

![Add Sphericon](images/add_sphericon.jpg)

スフェリコン形状のメッシュを作成します。一般的な正方形の回転体から作るスフェリコンの他、任意の多角形から作成することが可能で、左右のずらし量も指定できます。

-----

### Add Oloid

*Add Menu(<kbd>Shift+A</kbd>) → *Romly*

![Add Oloid](images/add_oloid.jpg)

オロイドまたはアンチオロイド形状のメッシュを作成します。円部分の頂点数を指定できますが、一部はオロイドを構築する際に削除されるため、実際の頂点数は指定した数より少なくなります。オロイドのみ、UVマップ展開済みです。

-----

### Add Aluminum Extrusion

*Add Menu(<kbd>Shift+A</kbd>) → *Romly*

![Add Aluminum Extrusion](images/add_aluminum_extrusion.jpg)

アルミフレーム形状のメッシュを作成します。パラメーターをいろいろ変更できるので存在しないアルミフレームの形状も作れてしまいますが、UI上に表示されている2020, 2040, 2060, 3030, 3060, 3090, 6090は比較的正確な大きさになると思います。CADのような正確な形状ではなく、ケース作成時などにあたりを取るためのオブジェクトという目的なのでご了承下さい。

-----

### Add Pin Header

*Add Menu*(<kbd>Shift+A</kbd>) → *Romly*

![Add Pin Header](images/add_pinheader.png)

ピンヘッダーを追加します。ピン数とピンのピッチを2.54mm、2.00mm、1.27mmから選択できます。ピン数はArrayモデファイアになっています。オブジェクトの原点は1番ピンの中心、PCBと接する点になっています。<br>
ピンの具体的な長さやブロック部分の大きさは一般的なものになっていると思いますが、必要に応じて生成時に調整可能です。マテリアルは未設定ですが、ピン部分とブロック部分は繋がっていないので塗り分けは簡単かと。

L型のも作れるといいんだけどとりあえずストレートのみです。

これも軸の秤でケースを設計している時にやたら使うのでスクリプトにまとめました。ピンヘッダー自体は単純な形状なのでキューブを2つ組み合わせればすぐできるのですが、サイズ指定とかいちいち手間だったものがスクリプトにすると一発で作れて楽ちんです。

-----

### Apply All Modifiers

*Object Context Menu*（オブジェクトを右クリック） → *Romly Tools*

すべてのモデファイアをまとめて適用します。そのまま。<br>
なんで標準機能にないんだろう？

-----

### Add Fixed Count Array Modifier

*Object Context Menu*（オブジェクトを右クリック） → *Romly Tools*

Relative OffsetではなくConstant Offsetを設定した状態のArrayモデファイアを追加します。<br>
自分の用途的にはRelative Offsetを指定することは極めて稀で、毎回毎回Constant Offsetにチェックを入れ直してオフセット距離を指定するのが面倒なのでスクリプトにまとめました。

-----

### Export Collection as STL

*Collection Menu*（コレクションを右クリック） → *Romly Tools*

コレクション内のメッシュをSTLファイルとして出力します。出力されるファイル名は `(blenderファイル名) - (コレクション名).stl` で、blenderファイルと同じフォルダに保存されます。このため、**編集中のファイルが保存されていないと（ファイル名が無いと）エラーになります。また、ファイル名に使えない文字をコレクション名に使っていたりするとエラーになるかもしれません。**<br>
サブコレクションも出力されますが、レイヤービューから除外されているコレクションは含まれません。

これは3Dプリントする時にスライサーに持っていくSTLファイルを出力するのに使っています。blenderで機械的な3Dプリント品を作る場合、CADソフトと違って複数のオブジェクトを組み合わせて形作ることが多いかと思います。自分の場合は出力するパーツごとにコレクションを作って、その中にそのパーツを構成するメッシュを格納しておき、このスクリプトでSTLを出力、スライサーに持っていくという流れで印刷してます。<br>
いちいちSTLファイルに含めるメッシュを選択する必要が無く、STLをエクスポートするときのダイアログも飛ばせるのでそれなりに便利です。<br>
また、レイヤービューから除外されているコレクションは対象外になるので、出力したくないメッシュ（ブーリアンモデファイアの演算対象など）は子コレクション内に格納し、出力時は*レイヤービューから除外*のチェックをしておくと出力には含まれず、また3Dビュー上でもブーリアンの結果のみ確認できるので便利です。

-----

### Export Selection as STL

*Object Menu*（アウトライナー上でオブジェクトを右クリック） → *Romly Tools*

選択されているオブジェクトをSTLファイルとして出力します。出力されるファイル名は `(blenderファイル名) - (アクティブなオブジェクト名).stl` で、blenderファイルと同じフォルダに保存されます。このため、 *Export Collection as STL* と同様、**編集中のファイルが保存されていないと（ファイル名が無いと）エラーになります。**<br>
*Export Collection as STL* とほとんど同じですが、単体オブジェクトや、選択範囲をサクッとSTLファイルにエクスポートしたい時のために作りました。

-----

### Select Edges on Fair Surface

**平面上にある辺を選択**

*Edge Menu*（編集モード）
*Edit Mesh Context Menu*（編集モード・辺選択時に右クリック）

編集中のメッシュの、平面上にある辺、つまり溶解しても影響がない辺をまとめて選択できます。STLファイルなどをインポートした時に、無駄な辺を整理するのに使えると思います。blenderの標準機能でありそうなのですが、見つけられないので作っちゃいました。

-----

### Language Panel

![Language Panel](images/language_panel.jpg)

サイドパネルのViewタブに『言語』というパネルが追加され、日本語、英語、フランス語、スペイン語、アラビア語、簡体字（4.1以降のみ）をボタン一つで切り替えられるようになります。また、言語設定の影響範囲を設定するチェックボックスも表示されます。

アドオンを英語対応するにあたって、デバッグで頻繁に言語設定を切り替える必要に迫られたのと、4.1から設定画面の言語ドロップダウンが1列になってしまい、非常に選択しづらくなったので作りました。日本語と英語以外の選択に関しては特に何も考えてなくて、デバッグ用に大きく変わりそうな言語をテキトーに選んだだけです。

おまけでblenderのバージョンと編集中のファイルのバージョンを表示します。





-----





## blend1_cleaner.py

【おまけ】blend1ファイルを再帰的に削除するPythonスクリプト

`extra/blend1_cleaner.py`

指定されたディレクトリ以下にある`*.blend1`ファイルを再帰的に検索し、一括で削除するPythonスクリプトです。[Send2Trash](https://pypi.org/project/Send2Trash/)モジュールがインストールされている環境であれば、削除せずにゴミ箱に移動することもできます。

**ファイルを削除する機能を持つスクリプトです。バグのために予期せぬファイルを削除してしまうことがあるかもしれません。当方は一切責任を負いかねます。了承の上自己責任でご利用下さい。**



### 使い方

```
python blend1_cleaner.py "(検索を開始するディレクトリ)" [-d] [-h]
```

#### オプション

##### `-d, --delete`

ファイルをゴミ箱に移動せず、完全に削除する場合に指定します。Send2Trashモジュールがインストールされていない環境では常に完全に削除（`-d`を指定した状態）しかできません。

##### `-h, --help`

ヘルプを表示します。



### 【オプション】send2trashのインストール

```
pip install Send2Trash
```