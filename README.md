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