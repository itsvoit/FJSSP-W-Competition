import os

from pathlib import Path
from argparse import ArgumentParser, Namespace

from .configs import instance_to_config_map, config_file_name


def add_arguments_common(parser: ArgumentParser):
    parser.add_argument("--output", "-o", help="Path to the output directory", type=Path, required=True)
    parser.add_argument("--runs", "-n", help="How many times to execute each instance", type=int, default=10)
    parser.add_argument("--instances", "-i", help="Root directory for instances", type=Path, default=Path("instances/fjssp-w"))
    parser.add_argument("--bash_output", help="Output file of the bash script", type=Path, default=Path("run_experiments.sh"))
    parser.add_argument("--nohup", help="Add nohup wrapper to run all experiments concurently", action='store_true')


def add_nohup(cmd: str, instance: str) -> str:
    out_cmd = f"nohup {cmd} > nohup-out/{instance}.out 2>&1 &"
    return out_cmd


def prepare_experiments_common(instances_root: Path, output_root: Path, runs: int) -> None:
    prepare_configs(instances_root, output_root)
    prepare_log_dir(output_root, runs)


def prepare_configs(instances_root: Path, output_root: Path):
    for instance_path in instances_root.iterdir():
        instance_name = instance_path.stem
        config = instance_to_config_map.get(instance_name, None)
        instance_output = output_root / instance_name
        if config:
            os.makedirs(instance_output, exist_ok=True)
            config.to_file(instance_name, str(instance_output.resolve()), instance_output / config_file_name)
            
            
def prepare_log_dir(output_root: Path, repetitions: int):
    for instance in output_root.iterdir():
        for i in range(repetitions):
            os.makedirs(instance / f"run_{i}", exist_ok=True)
