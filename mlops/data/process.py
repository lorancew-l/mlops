import argparse
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from mlops.data.s3_manager import S3Manager


def process(in_file, out_file):
    df = pd.read_csv(in_file)
    passenger_counts = df["Pclass"].value_counts().sort_index()

    passenger_counts_df = passenger_counts.reset_index()
    passenger_counts_df.columns = ["Pclass", "PassengerCount"]

    passenger_counts_df.to_csv(out_file, index=False)


def main(args):
    load_dotenv()

    data_folder = Path(__file__).resolve().parents[2].joinpath("data")
    download_file_path = data_folder.joinpath("raw", args.in_object)
    processed_file_path = data_folder.joinpath("processed", args.in_object)

    manager = S3Manager(args.bucket)

    # Загрузка файла из S3
    manager.download(args.in_object, download_file_path)

    # Обработка локального файла
    process(download_file_path, processed_file_path)

    # Выгрузка обработанного файла в S3
    manager.upload(processed_file_path, args.out_object)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S3 Data Processing Script")
    parser.add_argument("--bucket", required=True, help="S3 bucket name to download")
    parser.add_argument("--in-object", required=True, help="S3 object name to download")
    parser.add_argument("--out-object", required=True, help="S3 object name to upload")

    args = parser.parse_args()
    main(args)
