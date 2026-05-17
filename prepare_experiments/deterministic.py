from argparse import Namespace

from .common import add_arguments_common, prepare_log_dirs, prepare_bash, prepare_configs
from .configs import deterministic_instance_to_config_map


def deterministic_parser(subparsers):
    parser = subparsers.add_parser("deterministic", aliases=["d"])
    add_arguments_common(parser)
    parser.set_defaults(func=prepare_experiments_deterministic)
    
    
def prepare_experiments_deterministic(args: Namespace):
    executable = args.executable
    output_root = args.output
    runs = args.runs
    instances_root = args.instances
    bash_output = args.bash_output
    nohup = args.nohup
    append = args.append
    split = args.split

    prepare_log_dirs(
        instances_root=instances_root,
        output_root=output_root,
        instances_map=deterministic_instance_to_config_map,
        runs=runs,
    )
    prepare_configs(
        instances_root=instances_root,
        output_root=output_root,
        instances_map=deterministic_instance_to_config_map,
        split=split,
    ) 
    prepare_bash(
        instances_root=instances_root,
        output_root=output_root,
        bash_output=bash_output,
        executable=executable,
        runs=runs,
        nohup=nohup,
        append=append,
        split=split,
    )
