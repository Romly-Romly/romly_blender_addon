import bpy
from bl_i18n_utils import settings
from bpy.props import *



from . import romly_utils










def get_language_label(language: str) -> str:
	"""
	指定された言語コードに対応する言語のラベル（インターフェースでの表示名）を返す。

	Parameters
	----------
	language_code : str
		検索する言語コード。en_USとかja_JPとか。

	Returns
	-------
	str
		対応する言語のラベル。該当する言語が見つからなかったら空文字を返す。

	Notes
	-----
		Ex) `get_language_label('ja_JP')` -> "Japanese (日本語)"
	"""
	# settings.LANGUAGES は blender/release/scripts/modules/bl_i18n_utils/settings.py にある言語設定のリスト。(ID, UI english label, ISO code)のタプルのリストになってる
	for lang in settings.LANGUAGES:
		if lang[2] == language:
			return lang[1]
	return ''










class ROMLYADDON_OT_change_language(bpy.types.Operator):
	"""
	Blenderの言語を設定するオペレーター。
	languageプロパティに設定したい言語のISOコード(例えば'ja_JP')を渡す。
	"""
	bl_idname = "romlyaddon.change_language"
	bl_label = "Set Language"
	bl_description = 'Set blender language to specified language'
	bl_options = {'REGISTER', 'UNDO'}

	language: StringProperty(default='DEFAULT')

	def execute(self, context):
		bpy.context.preferences.view.language = self.language
		romly_utils.report(self, 'INFO', msg_key='The language was set to {language}', params={'language': get_language_label(bpy.context.preferences.view.language)})
		return {'FINISHED'}





class ROMLYADDON_PT_language_panel(bpy.types.Panel):
	bl_label = "Language"
	bl_idname = 'ROMLYADDON_PT_language_panel'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "View"	# 既存のViewタブに追加



	def draw(self, context):
		layout = self.layout
		layout.prop(context.scene, "romly_language", text="Language")

		col = layout.column(align=True)
		LANGS = [
			('DEFAULT', ''),
			('ja_JP', ''),
			('en_US', ''),
			('fr_FR', ''),
			('es', ''),
			('ar_EG', ''),
		]

		# 4.1以上なら簡体字も追加
		if romly_utils.is_blender_version_at_least(4, 1):
			LANGS.append(('zh_HANS', ''))

		for l in LANGS:
			text = bpy.app.translations.pgettext_iface(get_language_label(l[0]))
			op = col.operator(ROMLYADDON_OT_change_language.bl_idname, text=text)
			op.language = l[0]

		prefs = context.preferences
		view = prefs.view
		col = layout.column(align=True)
		col.prop(view, 'use_translate_tooltips', text='Tooltips')
		col.prop(view, 'use_translate_interface', text='Interface')
		col.prop(view, 'use_translate_new_dataname', text='New Data')

		# use_translate_reportsは4.1以上のみ
		if romly_utils.is_blender_version_at_least(4, 1):
			col.prop(view, 'use_translate_reports', text='Reports')

		# おまけのblenderバージョン表示
		col = layout.column(align=True)
		def format_version(v: tuple[int, int, int]) -> str:
			return f"{str(v[0])}.{str(v[1]).zfill(2)}.{str(v[2]).zfill(2)}"
		col.label(text=f"Blender {bpy.app.translations.pgettext_iface('Version')}: {format_version(bpy.app.version)}")
		col.label(text=f"{bpy.app.translations.pgettext_iface('Data')} {bpy.app.translations.pgettext_iface('Version')}: {format_version(bpy.data.version)}")




	def draw_header(self, context):
		layout = self.layout
		layout.label(text="", icon='WORLD')





classes = [
	ROMLYADDON_PT_language_panel,
	ROMLYADDON_OT_change_language,
]




def register():
	# クラスと翻訳辞書の登録
	romly_utils.register_classes_and_translations(classes)





def unregister():
	# クラスと翻訳辞書の登録解除
	romly_utils.unregister_classes_and_translations(classes)





if __name__ == '__main__':
	register()