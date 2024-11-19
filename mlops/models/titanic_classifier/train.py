import argparse
import os
from pathlib import Path
from typing import Any, Dict, Union

import mlflow
import mlflow.sklearn
import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from mlops.data.s3_manager import S3Manager


def train_and_log_model(
    data_path: Union[str, Path], params: Dict[str, Any], experiment_name: str
) -> None:
    df = pd.read_csv(data_path)
    X = df.drop("Survived", axis=1)
    y = df["Survived"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    artifact_bucket = os.getenv("ARTIFACT_BUCKET")
    if artifact_bucket is None:
        raise ValueError("Environment variable 'ARTIFACT_BUCKET' is not set")

    mlflow.set_experiment(experiment_name)
    with mlflow.start_run():
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        mlflow.log_params(params)
        mlflow.log_metric("accuracy", accuracy)

        s3manager = S3Manager(artifact_bucket)
        s3manager.create_bucket()
        mlflow.sklearn.log_model(model, f"{artifact_bucket}/{experiment_name}")


def parse_args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-path", required=True, help="Path of input bucket <bucket>/<dataset>"
    )
    parser.add_argument("--experiment-name", required=True, help="MLFlow experiment name")
    parser.add_argument("--max_depth", required=True)
    parser.add_argument(
        "--max_features",
        required=True,
    )
    parser.add_argument("--n_estimators", required=True)

    args = parser.parse_args()

    data_path_splitted = args.dataset_path.split("/")
    if len(data_path_splitted) != 2:
        raise Exception(
            f"Incorrect dataset_path, should be <bucket>/<dataset>, got ${args.dataset_path}"
        )

    data_bucket, data_file = data_path_splitted

    return {
        "data_bucket": data_bucket,
        "data_file": data_file,
        "experiment_name": args.experiment_name,
        "params": {
            "max_depth": int(args.max_depth),
            "max_features": args.max_features,
            "n_estimators": int(args.n_estimators),
        },
    }


if __name__ == "__main__":
    load_dotenv()

    args = parse_args()

    download_folder_path = Path(__file__).resolve().parents[3].joinpath("data", "processed")
    Path(download_folder_path).mkdir(parents=True, exist_ok=True)

    processed_file_path = Path(download_folder_path).joinpath(args["data_file"])

    manager = S3Manager(args["data_bucket"])
    manager.download(args["data_file"], processed_file_path)

    train_and_log_model(processed_file_path, args["params"], args["experiment_name"])
