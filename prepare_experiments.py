from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
import os

from argparse import ArgumentParser, Namespace


config_file_name: str = "config.cfg"
small = True
medium = True
large = True
very_large = True

MAX_BUDGET = 5_000_000


@dataclass
class Config:
    generations: int
    population_size: int
    selection_size: int
    crossover_prob: float
    mutation_prob: float
    mutation: str
    crossover: str
    neigh_cnt: int = 6
    clear_weights_interval: int = 0
    min_neigh_prob: float = 0.05
    
    def to_file(self, instance: str, log_directory: str, output: Path):
        with open(output, mode='w', encoding='utf-8') as handle:
            print(f"INSTANCE {instance}", file=handle)
            print(f"LOG_DIRECTORY {log_directory}", file=handle)
            print(f"GENERATIONS {self.generations}", file=handle)
            print(f"POPULATION_SIZE {self.population_size}", file=handle)
            print(f"SELECTION_SIZE {self.selection_size}", file=handle)
            print(f"CROSSOVER_PROB {self.crossover_prob}", file=handle)
            print(f"MUTATION_PROB {self.mutation_prob}", file=handle)
            print(f"MUTATION {self.mutation}", file=handle)
            print(f"CROSSOVER {self.crossover}", file=handle)
            print(f"NEIGH_CNT {self.neigh_cnt}", file=handle)
            print(f"CLEAR_WEIGHTS_INTERVAL {self.clear_weights_interval}", file=handle)
            print(f"MIN_NEIGH_PROB {self.min_neigh_prob}", file=handle)


# Small
small_instance_config = Config(
    generations = 124999,
    # generations = 50,
    population_size = 40,
    selection_size = 5,
    crossover_prob = 0.1,
    mutation_prob = 0.035,
    mutation = "MIXED",
    crossover = "MOX",
) if small else None

# Medium
medium_rigid_instance_config = Config(
    generations = 99999,
    # generations = 2999,
    population_size = 50,
    selection_size = 5,
    crossover_prob = 0.2,
    mutation_prob = 0.025,
    mutation = "MIXED",
    crossover = "MOX",
) if medium else None

medium_flexible_instance_config = Config(
    generations = 99999,
    # generations = 2999,
    population_size = 50,
    selection_size = 5,
    crossover_prob = 0.2,
    mutation_prob = 0.005,
    mutation = "MIXED",
    crossover = "MOX",
) if medium else None

# Large
large_instance_config = Config(
    generations = 99999,
    population_size = 50,
    selection_size = 5,
    crossover_prob = 0.2,
    mutation_prob = 0.005,
    mutation = "MIXED",
    crossover = "MOX",
) if large else None

# Very large
very_large_instance_config = Config(
    generations = 99999,
    # generations = 999,
    population_size = 50,
    selection_size = 5,
    crossover_prob = 0.2,
    mutation_prob = 0.0025,
    mutation = "MIXED",
    crossover = "MOX",
) if very_large else None

instance_to_config_map: Dict[str, Optional[Config]] = {
    "0_BehnkeGeiger_42_workers": small_instance_config,
    "0_BehnkeGeiger_46_workers": medium_rigid_instance_config,
    "0_BehnkeGeiger_60_workers": very_large_instance_config,
    "1_Brandimarte_12_workers": large_instance_config,
    "1_Brandimarte_14_workers": large_instance_config,
    "1_Brandimarte_7_workers": medium_flexible_instance_config,
    "2a_Hurink_sdata_1_workers": small_instance_config,
    "2a_Hurink_sdata_18_workers": medium_flexible_instance_config,
    "2a_Hurink_sdata_38_workers": very_large_instance_config,
    "2a_Hurink_sdata_40_workers": large_instance_config,
    "2a_Hurink_sdata_54_workers": medium_rigid_instance_config,
    "2a_Hurink_sdata_61_workers": medium_flexible_instance_config,
    "2a_Hurink_sdata_63_workers": medium_rigid_instance_config,
    "2b_Hurink_edata_1_workers": small_instance_config,
    "2b_Hurink_edata_6_workers": small_instance_config,
    "2c_Hurink_rdata_28_workers": large_instance_config,
    "2c_Hurink_rdata_38_workers": very_large_instance_config,
    "2c_Hurink_rdata_50_workers": small_instance_config,
    "2d_Hurink_vdata_18_workers": medium_flexible_instance_config,
    "2d_Hurink_vdata_30_workers": large_instance_config,
    "2d_Hurink_vdata_5_workers": small_instance_config,
    "3_DPpaulli_15_workers": very_large_instance_config,
    "3_DPpaulli_18_workers": very_large_instance_config,
    "3_DPpaulli_1_workers": large_instance_config,
    "3_DPpaulli_9_workers": large_instance_config,
    "4_ChambersBarnes_10_workers": large_instance_config,
    "5_Kacem_3_workers": small_instance_config,
    "5_Kacem_4_workers": small_instance_config,
    "6_Fattahi_14_workers": small_instance_config,
    "6_Fattahi_20_workers": small_instance_config,
}


def prepare_configs(instances_root: Path, output_root: Path):
    for instance_path in instances_root.iterdir():
        instance_name = instance_path.stem
        config = instance_to_config_map.get(instance_name, None)
        instance_output = output_root / instance_name
        if config:
            os.makedirs(instance_output, exist_ok=True)
            config.to_file(instance_name, str(instance_output.resolve()), instance_output / config_file_name)


def add_nohup(cmd: str, instance: str) -> str:
    out_cmd = f"nohup {cmd} > nohup-out/{instance}.out 2>&1 &"
    return out_cmd


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


def prepare_log_dir(output_root: Path, repetitions: int):
    for instance in output_root.iterdir():
        for i in range(repetitions):
            os.makedirs(instance / f"run_{i}", exist_ok=True)


def add_arguments_common(parser: ArgumentParser):
    parser.add_argument("--output", "-o", help="Path to the output directory", type=Path, required=True)
    parser.add_argument("--runs", "-n", help="How many times to execute each instance", type=int, default=10)
    parser.add_argument("--instances", "-i", help="Root directory for instances", type=Path, default=Path("instances/fjssp-w"))
    parser.add_argument("--bash_output", help="Output file of the bash script", type=Path, default=Path("run_experiments.sh"))
    parser.add_argument("--nohup", help="Add nohup wrapper to run all experiments concurently", action='store_true')


def uncertainty_parser(subparsers):
    parser = subparsers.add_parser("uncertainty", aliases=["u"])
    add_arguments_common(parser)
    parser.set_defaults(func=prepare_experiments_uncertainty)


def deterministic_parser(subparsers):
    parser = subparsers.add_parser("deterministic", aliases=["d"])
    add_arguments_common(parser)
    parser.add_argument("--executable", "-e", help="Path to executable", type=Path, required=True)
    parser.set_defaults(func=prepare_experiments_deterministic)
    

def parse_args():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    
    deterministic_parser(subparsers)
    uncertainty_parser(subparsers)
    
    return parser.parse_args()


def prepare_experiments_common(instances_root: Path, output_root: Path, runs: int) -> None:
    prepare_configs(instances_root, output_root)
    prepare_log_dir(output_root, runs)
    

def prepare_experiments_deterministic(args: Namespace):
    executable = args.executable
    output_root = args.output
    runs = args.runs
    instances_root = args.instances
    bash_output = args.bash_output
    
    prepare_experiments_common(instances_root, output_root, runs)
    prepare_bash_deterministic(instances_root, output_root, bash_output, executable, runs, args.nohup)


def prepare_experiments_uncertainty(args: Namespace):
    output_root = args.output
    runs = args.runs
    instances_root = args.instances
    bash_output = args.bash_output
    
    prepare_experiments_common(instances_root, output_root, runs)
    prepare_bash_uncertainty(instances_root, output_root, bash_output, runs, args.nohup)


def main():
    args = parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    exit(main())