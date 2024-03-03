from pydub import AudioSegment
import os

# 入力フォルダと出力フォルダのパス
input_folder_path = "パワポ用実験"
output_folder_path = "パワポ用実験"

# フォルダ内のすべてのファイルを処理
for file_name in os.listdir(input_folder_path):
    if file_name.endswith(".wav"):
        # 入力ファイルのパス
        input_file_path = os.path.join(input_folder_path, file_name)

        # 出力ファイルのパス
        output_file_path = os.path.join(output_folder_path, f"trimmed_{file_name}")

        # WAV ファイルを読み込み
        audio = AudioSegment.from_wav(input_file_path)

        # 切り取りたい部分の長さを指定（単位はミリ秒）
        cut_duration = 1 # 0.001 秒

        # 最初の0.001秒を切り取って残りの音声を取得
        trimmed_audio = audio[cut_duration:]

        # 切り取られた音声を保存
        trimmed_audio.export(output_file_path, format="wav")

print("処理が完了しました。")
