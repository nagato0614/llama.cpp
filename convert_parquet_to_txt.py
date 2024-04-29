import os

import pandas as pd
from datetime import datetime


def main():
    # パスの指定
    parquet_path = '/Volumes/SSPA-USC/train_parquet/train_wiki/'
    txt_path = '/Volumes/SSPA-USC/train_txt/'

    # 対象のディレクトリいかにあるparquetファイル一覧を取得
    parquet_files = []
    for root, dirs, files in os.walk(parquet_path):
        for file in files:
            if file.endswith(".parquet"):
                parquet_files.append(os.path.join(root, file))

    # ファイル名に ._ がついているものを除外する
    parquet_files = [parquet_file for parquet_file in parquet_files if '._' not in parquet_file]
    print(parquet_files)

    # 一つずつparquetファイルを読み込んで、それぞれをtxtファイルに変換
    for parquet_file in parquet_files:
        print(f'## {parquet_file}')
        # parquetファイルを読み込む
        df = pd.read_parquet(parquet_file)

        # 書き込むファイル名を作成
        txt_file = parquet_file.replace(parquet_path, txt_path).replace('.parquet', '.txt')
        print(f'## {txt_file}')

        # ファイルを開く
        with open(txt_file, 'w') as f:
            # テキストファイルに追記
            for i in range(len(df)):
                f.write(df.iloc[i]['text'] + '\n')

if __name__ == '__main__':
    main()
