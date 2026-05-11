import os

from argparse import Namespace
from pathlib import Path

from .common import add_nohup, add_arguments_common, prepare_experiments_common
from .configs import config_file_name
            
            
def uncertainty_parser(subparsers):
    parser = subparsers.add_parser("uncertainty", aliases=["u"])
    add_arguments_common(parser)
    parser.set_defaults(func=prepare_experiments_uncertainty)
    

def prepare_experiments_uncertainty(args: Namespace):
    output_root = args.output
    runs = args.runs
    instances_root = args.instances
    bash_output = args.bash_output
    
    prepare_experiments_common(instances_root, output_root, runs)
    prepare_bash_uncertainty(instances_root, output_root, bash_output, runs, args.nohup)


def prepare_bash_uncertainty(instances_root: Path, output_root: Path, bash_output: Path, runs: int, nohup: bool = False):
    def opener(path, flags):
        return os.open(path, flags, 0o744)
    
    with open(bash_output, mode='w+', encoding='utf-8', opener=opener) as handle:
        for instance_logs in output_root.iterdir():
            config_path = instance_logs / config_file_name
            cmd = f"python run_experiments.py --instances {instances_root.as_posix()} --config {config_path.as_posix()} --runs {runs}"
            if nohup:
                cmd = add_nohup(cmd, instance_logs.stem)
            print(cmd, file=handle)
