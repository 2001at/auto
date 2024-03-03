from pydub import AudioSegment
import os

# 入力フォルダと出力フォルダのパス
input_folder_path = "パワポ用実験/all_sample.wav"
output_folder_path = "パワポ用実験"

# フォルダ内のすべてのファイルを処理
for file_name in os.listdir(input_folder_path):
    if file_name.endswith(".wav"):
        # 入力ファイルのパス
        input_file_path = os.path.join(input_folder_path, file_name)

        # 出力ファイルのパス
        output_file_path = os.path.join(output_folder_path, f"with_silence_{file_name}")

        # WAV ファイルを読み込み
        audio = AudioSegment.from_wav(input_file_path)

        # 追加したい無音区間の長さを指定（単位はミリ秒）
        silence_duration = 10 # 1秒

        # 無音区間を作成
        silence = AudioSegment.silent(duration=silence_duration)

        # 無音区間を音声の先頭に追加
        audio_with_silence = silence + audio

        # 無音区間が追加された音声を保存
        audio_with_silence.export(output_file_path, format="wav")

print("処理が完了しました。")
