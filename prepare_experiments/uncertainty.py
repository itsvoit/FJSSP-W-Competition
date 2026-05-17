from argparse import Namespace

from .common import add_arguments_common, prepare_log_dirs, prepare_bash, prepare_configs
from .configs import uncertainty_instance_to_config_map, deterministic_instance_to_config_map
            
            
def uncertainty_parser(subparsers):
    parser = subparsers.add_parser("uncertainty", aliases=["u"])
    add_arguments_common(parser)
    parser.add_argument("--factor", "-f", help="Uncertainty factor, used like: alpha = random, beta = factor*alpha", type=float, default=10.0)
    parser.set_defaults(func=prepare_experiments_uncertainty)
    

def prepare_experiments_uncertainty(args: Namespace):
    executable = args.executable
    output_root = args.output
    runs = args.runs
    instances_root = args.instances
    bash_output = args.bash_output
    nohup = args.nohup
    append = args.append
    split = args.split
    factor = args.factor
    
    config_map = deterministic_instance_to_config_map
    
    prepare_log_dirs(
        instances_root=instances_root,
        output_root=output_root,
        instances_map=config_map,
        runs=runs,
    )
    prepare_configs(
        instances_root=instances_root,
        output_root=output_root,
        instances_map=config_map,
        factor=factor,
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
