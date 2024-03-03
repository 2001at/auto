import os
from pydub import AudioSegment

# FFmpegのパスを設定
# FFmpegのバイナリファイルはダウンロードしておいてください
ffmpeg_path = "C:/Users/飯田/Desktop/ffmpeg-6.1"
AudioSegment.converter = ffmpeg_path


def adjust_audio_length(audio1, audio2):
    length_audio1 = len(audio1)
    length_audio2 = len(audio2)

    if length_audio1 < length_audio2:
        repeated_audio1 = audio1 * ((length_audio2 // length_audio1) + 1)
        adjusted_audio1 = repeated_audio1[:length_audio2]
        adjusted_audio2 = audio2
    elif length_audio2 < length_audio1:
        adjusted_audio1 = audio1[:length_audio2]
        adjusted_audio2 = audio2
    else:
        adjusted_audio1 = audio1
        adjusted_audio2 = audio2

    return adjusted_audio1, adjusted_audio2

def process_and_save(audio1_path, audio2_path, output_path):
    # 音声ファイルを読み込む
    audio1 = AudioSegment.from_file(audio1_path)
    audio2 = AudioSegment.from_file(audio2_path)

    # 自動で音声の長さを調整
    adjusted_audio1, adjusted_audio2 = adjust_audio_length(audio1, audio2)

    # 音声を混ぜる
    mixed_audio = adjusted_audio1.overlay(adjusted_audio2)

    # 出力ファイルに保存
    mixed_audio.export(output_path, format="wav")

# 音声1のパスを指定
audio1_path = "white_noize.wav"

# 音声2のディレクトリパスを指定
audio2_directory = "パワポ用実験"

# 出力ディレクトリのパスを指定
output_directory = "パワポ用実験"

# ディレクトリ内の全てのファイルに対して処理を行う
for audio2_filename in os.listdir(audio2_directory):
    if audio2_filename.endswith(".wav"):
        audio2_path = os.path.join(audio2_directory, audio2_filename)
        output_path = os.path.join(output_directory, f"mixed_{audio2_filename}")
        
        # 音声1を使用して処理を行う
        process_and_save(audio1_path, audio2_path, output_path)
