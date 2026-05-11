import os

from argparse import Namespace
from pathlib import Path

from .common import add_nohup, add_arguments_common, prepare_experiments_common
from .configs import config_file_name


def deterministic_parser(subparsers):
    parser = subparsers.add_parser("deterministic", aliases=["d"])
    add_arguments_common(parser)
    parser.add_argument("--executable", "-e", help="Path to executable", type=Path, required=True)
    parser.set_defaults(func=prepare_experiments_deterministic)
    
    
def prepare_experiments_deterministic(args: Namespace):
    executable = args.executable
    output_root = args.output
    runs = args.runs
    instances_root = args.instances
    bash_output = args.bash_output
    
    prepare_experiments_common(instances_root, output_root, runs)
    prepare_bash_deterministic(instances_root, output_root, bash_output, executable, runs, args.nohup)


def prepare_bash_deterministic(instances_root: Path, output_root: Path, bash_output: Path, executable: Path, runs: int, nohup: bool = False):
    def opener(path, flags):
        return os.open(path, flags, 0o744)
        
    with open(bash_output, mode='w+', encoding='utf-8', opener=opener) as handle:
        for instance_logs in output_root.iterdir():
            config_path = instance_logs / config_file_name
            cmd = f"{executable.as_posix()} {instances_root.as_posix()} {config_path.as_posix()} {runs}"
            if nohup:
                cmd = add_nohup(cmd, instance_logs.stem)
            print(cmd, file=handle)
