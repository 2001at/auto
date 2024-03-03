import os
import subprocess
import pandas as pd

def run_command(input_file, reference_file):
    command = f"python new_wer.py {input_file} {reference_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def save_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=["File Pair", "WER Result"])
    df.to_excel(output_file, index=False)

def main():
    #正解文
    input_directory ="d"
    #比較文
    reference_directory ="use_new_julius/old(noEng)"
    file_extension = ".txt"

    input_files = [file for file in os.listdir(input_directory) if file.endswith(file_extension)]
    reference_files = [file for file in os.listdir(reference_directory) if file.endswith(file_extension)]

    result_data = []

    for input_file, reference_file in zip(input_files, reference_files):
        result = run_command(os.path.join(input_directory, input_file), os.path.join(reference_directory, reference_file))
        result_data.append([input_file, result])

    output_excel = "wer_results.xlsx"
    save_to_excel(result_data, output_excel)
    print(f"Results saved to {output_excel}")

if __name__ == "__main__":
    main()
