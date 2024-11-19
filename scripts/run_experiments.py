import argparse
import itertools
import subprocess
from pathlib import Path
from typing import Dict, List, Union, cast

import yaml


def load_config(config_path: str) -> Dict[str, Union[str, Dict[str, List[Union[int, str]]]]]:
    file_path = Path(__file__).resolve().parents[1].joinpath(config_path)
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
        if not isinstance(config, dict):
            raise ValueError("Invalid configuration format")
        return cast(Dict[str, Union[str, Dict[str, List[Union[int, str]]]]], config)


def generate_hyperparameter_combinations(
    hyperparameters: Dict[str, List[Union[int, str]]]
) -> List[Dict[str, Union[int, str]]]:
    keys, values = zip(*hyperparameters.items())
    combinations = [dict(zip(keys, combination)) for combination in itertools.product(*values)]
    return combinations


def run_experiment(
    model: str,
    hyperparameters: Dict[str, Union[int, str]],
    dataset_path: str,
    experiment_name: str,
) -> None:
    hyperparameters_str = " ".join([f"--{key} {value}" for key, value in hyperparameters.items()])

    command = (
        f"docker run --rm --env-file .container_env -e MODEL={model} "
        f"train_model --dataset-path {dataset_path} --experiment-name {experiment_name} {hyperparameters_str}"
    )

    subprocess.run(command, shell=True)


def run_experiments(config_path: str, dataset_path: str) -> None:
    config = load_config(config_path)

    model_name = str(config.get("model", ""))
    if not model_name:
        raise ValueError("Model name is not specified in the configuration")
    
    hyperparameters = config.get("hyperparameters", {})
    if not isinstance(hyperparameters, dict):
        raise ValueError("Invalid hyperparameters format in config")
    
    hyperparameter_combinations = generate_hyperparameter_combinations(hyperparameters)

    for idx, combination in enumerate(hyperparameter_combinations):
        experiment_name = f"{model_name}_experiment_{idx+1}"
        print(f"Start experiment: {experiment_name} with hyperparameters {combination}")
        run_experiment(model_name, combination, dataset_path, experiment_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start experiment with hyperparameters")
    parser.add_argument("--config-path", type=str, required=True, help="Path to config file")
    parser.add_argument(
        "--dataset-path", type=str, required=True, help="Path to s3 dataset <bucket>/<dataset>"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_experiments(args.config_path, args.dataset_path)
