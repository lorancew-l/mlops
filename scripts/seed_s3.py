import argparse
from pathlib import Path

from dotenv import load_dotenv

from mlops.data.s3_manager import S3Manager


def main(args):
    load_dotenv()

    file_path = Path(__file__).resolve().parent.joinpath(args.dataset)

    manager = S3Manager(args.bucket)
    manager.create_bucket()
    manager.upload(
        file_path,
        args.object,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S3 Data Processing Script")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--object", required=True, help="S3 object name")
    parser.add_argument(
        "--dataset", required=False, help="dataset file name", default="titanic_dataset.csv"
    )

    args = parser.parse_args()
    main(args)
