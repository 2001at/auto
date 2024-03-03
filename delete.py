import os
import re

def remove_special_characters(text):
    # 正規表現を使っても超す文字を指定(漢字かなカナ数字残し)
    #cleaned_text = re.sub('[^\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF0-9]', '', text)
    # 正規表現を使って消す文字の指定
    cleaned_text = re.sub('[、。？！!?\s/❌⭕️🙅‍♀️:「…」¿¥¤]', '', text)
    return cleaned_text

def process_directory(input_directory, output_directory):
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 入力ディレクトリ内の全てのファイルに対して処理を行う
    for filename in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, filename)

        # ファイルのみを対象にする
        if os.path.isfile(input_file_path):
            output_file_path = os.path.join(output_directory, filename)

            # ファイルからテキストを読み込む
            with open(input_file_path, 'r', encoding='utf-8') as file:
                input_text = file.read()

            # テキストを処理
            processed_text = remove_special_characters(input_text)

            # 処理したテキストを別のファイルに書き込む
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(processed_text)

# 入力ディレクトリと出力ディレクトリのパス
input_directory_path = 'c_new_julius_res/old'
output_directory_path = 'use_new_julius/old'

# ディレクトリ内のファイルを一括で処理
process_directory(input_directory_path, output_directory_path)

print("処理が完了しました。")
