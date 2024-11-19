import argparse
from pathlib import Path
from typing import Union

import pandas as pd
from dotenv import load_dotenv

from mlops.data.s3_manager import S3Manager


def process(in_file: Union[str, Path], out_file: Union[str, Path]) -> None:
    df = pd.read_csv(in_file)

    df["Age"].fillna(df["Age"].mean(), inplace=True)
    df["Fare"].fillna(df["Fare"].mean(), inplace=True)
    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    df["Embarked"] = df["Embarked"].map({"C": 0, "Q": 1, "S": 2}).fillna(2)
    df = df[["Pclass", "Sex", "Age", "Fare", "Embarked", "Survived"]]

    df.to_csv(out_file, index=False)


def main(args: argparse.Namespace) -> None:
    load_dotenv()

    data_folder = Path(__file__).resolve().parents[2].joinpath("data")

    download_folder_path = data_folder.joinpath("raw")
    processed_folder_path = data_folder.joinpath("processed")

    download_file_path = data_folder.joinpath(download_folder_path, args.in_object)
    processed_file_path = data_folder.joinpath(processed_folder_path, args.in_object)

    Path(download_folder_path).mkdir(parents=True, exist_ok=True)
    Path(processed_folder_path).mkdir(parents=True, exist_ok=True)

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
