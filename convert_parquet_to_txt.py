import os

import pandas as pd
from datetime import datetime


def main():
    # パスの指定
    parquet_path = '/Volumes/SSPA-USC/train_parquet/'
    txt_path = '/Volumes/SSPA-USC/train_txt/train.txt'

    # 対象のディレクトリいかにあるparquetファイル一覧を取得
    parquet_files = []
    for root, dirs, files in os.walk(parquet_path):
        for file in files:
            if file.endswith(".parquet"):
                parquet_files.append(os.path.join(root, file))

    # ファイル名に ._ がついているものを除外する
    parquet_files = [parquet_file for parquet_file in parquet_files if '._' not in parquet_file]
    print(parquet_files)



    with open(txt_path, 'w') as f:
        for parquet_file in parquet_files:
            print(f'## {parquet_file}')
            # Parquet からロード
            df = pd.read_parquet(parquet_file)

            # 各行の改行文字を削除
            df = df.replace('\n', '', regex=True)

            # テキストファイルに追記
            for i in range(len(df)):
                f.write(df.iloc[i]['text'] + '\n')

            break




if __name__ == '__main__':
    main()
