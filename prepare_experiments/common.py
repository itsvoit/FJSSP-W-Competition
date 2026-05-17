import os

from pathlib import Path
from argparse import ArgumentParser
from typing import Dict, Optional

from .configs import Config
from .uncertainty_utils import create_uncertainty_vector_from_instance, write_uncerainty_to_file
from .constants import config_file_name, worker_uncertainties_file_name


def add_arguments_common(parser: ArgumentParser):
    parser.add_argument("--executable", "-e", help="Path to executable", type=Path, required=True)
    parser.add_argument("--output", "-o", help="Path to the output directory", type=Path, required=True)
    parser.add_argument("--runs", "-n", help="How many times to execute each instance", type=int, default=10)
    parser.add_argument("--instances", "-i", help="Root directory for instances", type=Path, default=Path("instances/fjssp-w"))
    parser.add_argument("--bash_output", help="Output file of the bash script", type=Path, default=Path("run_experiments.sh"))
    parser.add_argument("--nohup", help="Add nohup wrapper to run all experiments concurently", action='store_true')
    parser.add_argument("--append", "-a", help="Append the new run commands into the existing run script", action='store_true')
    parser.add_argument("--split", "-s", help="Split runs into separate application instances - especially"
                        "useful with --nohup to run every single optimisation on a separate core", action='store_true')
    parser.add_argument("--suppress", "-S", help="Suppress evolution logs. Useful for running a "
                        "lot of simulations at once to save storage", action='store_true')


def add_nohup(cmd: str, instance: str, output_root: str) -> str:
    output_path = Path(f"nohup-out/{output_root}/{instance}.out")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out_cmd = f"nohup {cmd} > {output_path.as_posix()} 2>&1 &"
    return out_cmd


def prepare_configs(instances_root: Path, output_root: Path, instances_map: Dict[str, Optional[Config]], split: bool = False, factor: Optional[float] = None):
    for instance_path in instances_root.iterdir():
        instance_name = instance_path.stem
        config = instances_map.get(instance_name, None)
        
        instance_output = output_root / instance_name
        if config:
            # Add uncertainties
            if (factor):
                worker_uncertainties = create_uncertainty_vector_from_instance(instance_path, factor)
                uncertainty_params_path = instance_output / worker_uncertainties_file_name
                write_uncerainty_to_file(worker_uncertainties, uncertainty_params_path)
                config.uncertainty_params_path = uncertainty_params_path
            if split:
                for instance_run in instance_output.iterdir():
                    if not instance_run.is_dir():
                        continue
                    prepare_config(config, instance_name, str(instance_run.resolve()), instance_run / config_file_name)
            else:
                prepare_config(config, instance_name, str(instance_output.resolve()), instance_output / config_file_name)


def prepare_config(config: Config, instance_name: str, log_directory: str, config_output: Path):
    config.to_file(instance_name, log_directory, config_output)


def prepare_bash(instances_root: Path, output_root: Path, bash_output: Path, executable: Path, runs: int, nohup: bool = False, append: bool = False, split: bool = False, suppress: bool = False):
    def opener(path, flags):
        return os.open(path, flags, 0o744)
    
    mode = 'a' if append else 'w'
    with open(bash_output, mode=mode, encoding='utf-8', opener=opener) as handle:
        for instance_logs in output_root.iterdir():
            if split:
                for instance_run in instance_logs.iterdir():
                    if instance_run.is_file():
                        continue
                    config_path = instance_run / config_file_name
                    print_cmd_to_handle(handle, executable, instances_root, f"{instance_logs.stem}_{instance_run.stem}", output_root, config_path, 1, nohup, suppress)
            else:
                config_path = instance_logs / config_file_name
                print_cmd_to_handle(handle, executable, instances_root, instance_logs.stem, output_root, config_path, runs, nohup, suppress)


def print_cmd_to_handle(handle, executable, instances_root, log_name, output_root, config_path, runs, nohup, suppress):
    supp_flag = "" if suppress else " 1"
    cmd = f"{executable.as_posix()} {instances_root.as_posix()} {config_path.as_posix()} {runs}{supp_flag}"
    if nohup:
        cmd = add_nohup(cmd, log_name, output_root.stem)
    print(cmd, file=handle)

            
def prepare_log_dirs(instances_root: Path, output_root: Path, instances_map: Dict[str, Optional[Config]], runs: int):
    for instance_path in instances_root.iterdir():
        instance_name = instance_path.stem
        instance_output = output_root / instance_name
        config = instances_map.get(instance_name, None)
        if config:
            os.makedirs(instance_output, exist_ok=True)
            for instance in output_root.iterdir():
                for i in range(runs):
                    (instance / f"run_{i}").mkdir(exist_ok=True, parents=True)
