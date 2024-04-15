import os
import argparse
import fnmatch
from pathlib import Path
from typing import List
import importlib.util

# send2trash モジュールはオプション
try:
	from send2trash import send2trash
except ImportError:
	pass










def is_module_installed(module_name: str) -> bool:
	"""
	指定したモジュールがインストールされているか確認する。

	Parameters
	----------
	module_name : str
		チェックするモジュールの名前。

	Returns
	-------
	bool
		モジュールがインストールされていればTrue、そうでなければFalse。
	"""
	return importlib.util.find_spec(module_name) is not None










def find_files(base_path: str, extension: str) -> List[str]:
	"""
	指定された拡張子を持つファイルを、指定されたディレクトリから再帰的に検索する関数。

	Parameters
	----------
	base_path : str
		検索を開始するディレクトリ。
	extension : str
		検索対象のファイル拡張子。

	Returns
	-------
	found_files : List[str]
		見つかったファイルのパスのリスト。
	"""
	found_files = []
	for root, dirs, files in os.walk(base_path):
		dirs[:] = [d for d in dirs if not d.startswith('.')] # 隠しディレクトリをスキップ
		for file in fnmatch.filter(files, f'*.{extension}'):
			found_files.append(os.path.join(root, file))
	return found_files










def main(start_directory: str, delete_permanently: bool) -> None:
	"""
	指定されたディレクトリから開始して、再帰的に*.blend1ファイルを検索し、
	ユーザーに削除の確認を求めるメイン関数。

	Parameters
	----------
	start_directory : str
		検索を開始するディレクトリ。
	"""
	if not os.path.exists(start_directory):
		print("指定されたディレクトリが存在しません。")
		return

	print("*.blend1ファイルを検索中...")
	blend1_files = find_files(start_directory, 'blend1')
	if not blend1_files:
		print("*.blend1ファイルが見つかりませんでした。")
		return

	print("見つかった*.blend1ファイルのリスト:")
	for file_path in blend1_files:
		print(file_path)

	if delete_permanently:
		user_input = input("これらのファイルを完全に削除してもよろしいですか？ [y/N] ")
	else:
		user_input = input("これらのファイルをゴミ箱に移動してもよろしいですか？ [y/N] ")

	if user_input.lower() == 'y':
		for file_path in blend1_files:
			if delete_permanently:
				os.remove(file_path)  # 完全に削除
			else:
				send2trash(file_path)  # ゴミ箱に移動
		print("*.blend1ファイルを処理しました。")
	else:
		print("操作をキャンセルしました。")










if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="*.blend1ファイルを検索して削除またはゴミ箱に移動するスクリプト")
	parser.add_argument("start_directory", help="検索を開始するディレクトリ")
	parser.add_argument("-d", "--delete", action="store_true", help="ファイルを完全に削除する場合に指定")
	args = parser.parse_args()

	# モジュールがインストールされているか確認
	trash_available = is_module_installed('send2trash')
	if not trash_available:
		print('send2trash モジュールをインストールすると、ファイルを削除せずゴミ箱に移動することも出来るようになります。')

	main(args.start_directory, True if not trash_available else args.delete)