# romly_blender_addon

個人的に作成、使用している[Blender](https://www.blender.org/)用のスクリプトいろいろ。<br>
動作確認したBlenderのバージョンは3.5です。<br>

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

### Apply All Modifiers

*Object Context Menu*（オブジェクトを右クリック） → *Romly Tools*

すべてのモデファイアをまとめて適用します。そのまま。<br>
なんで標準機能にないんだろう？

### Add Fixed Count Array Modifier

*Object Context Menu*（オブジェクトを右クリック） → *Romly Tools*

Relative OffsetではなくConstant Offsetを設定した状態のArrayモデファイアを追加します。<br>
自分の用途的にはRelative Offsetを指定することは極めて稀で、毎回毎回Constant Offsetにチェックを入れ直してオフセット距離を指定するのが面倒なのでスクリプトにまとめました。

### Export Collection as STL

**Collection Menu*（コレクションを右クリック） → *Romly Tools*

コレクション内のメッシュをSTLファイルとして出力します。出力されるファイル名は`(blenderファイル名) - (コレクション名).stl`で、blenderファイルと同じフォルダに保存されます。このため、**編集中のファイルが保存されていないと（ファイル名が無いと）エラーになります。また、ファイル名に使えない文字をコレクション名に使っていたりするとエラーになるかもしれません。**<br>
サブコレクションも出力されますが、レイヤービューから除外されているコレクションは含まれません。

これは3Dプリントする時にスライサーに持っていくSTLファイルを出力するのに使っています。blenderで機械的な3Dプリント品を作る場合、CADソフトと違って複数のオブジェクトを組み合わせて形作ることが多いかと思います。自分の場合は出力するパーツごとにコレクションを作って、その中にそのパーツを構成するメッシュを格納しておき、このスクリプトでSTLを出力、スライサーに持っていくという流れで印刷してます。<br>
いちいちSTLファイルに含めるメッシュを選択する必要が無く、STLをエクスポートするときのダイアログも飛ばせるのでそれなりに便利です。<br>
また、レイヤービューから除外されているコレクションは対象外になるので、出力したくないメッシュ（ブーリアンモデファイアの演算対象など）は子コレクション内に格納し、出力時は*レイヤービューから除外*のチェックをしておくと出力には含まれず、また3Dビュー上でもブーリアンの結果のみ確認できるので便利です。