import os
from pathlib import Path
from typing import Union

import boto3


class S3Manager:
    def __init__(self, bucket_name: str):
        self.bucket_name: str = bucket_name
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def create_bucket(self) -> None:
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' created successfully")
        except (
            self.s3_client.exceptions.BucketAlreadyExists,
            self.s3_client.exceptions.BucketAlreadyOwnedByYou,
        ):
            print(f"Bucket '{self.bucket_name}' already exists")
        except Exception as e:
            print(f"Failed to create bucket '{self.bucket_name}': {e}")

    def upload(self, file_name: Union[str, Path], object_name: Union[str, Path]) -> None:
        try:
            print(f"Uploading '{file_name}' to '{object_name}'")
            self.s3_client.upload_file(file_name, self.bucket_name, object_name)
            print(f"'{file_name}' uploaded to '{self.bucket_name}/{object_name}'")
        except Exception as e:
            print(f"Failed to upload '{file_name}': {e}")

    def download(self, object_name: Union[str, Path], file_name: Union[str, Path]) -> None:
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_name)
            print(f"'{object_name}' downloaded from '{self.bucket_name}' to '{file_name}'")
        except Exception as e:
            print(f"Failed to download '{object_name}': {e}")
