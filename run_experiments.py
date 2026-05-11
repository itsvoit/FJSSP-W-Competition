import logging

logging.basicConfig(
    level=logging.WARNING,
    # level=logging.INFO,
    # level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s(): %(message)s"
)
logger = logging.getLogger(__name__)


from argparse import ArgumentParser
from pathlib import Path
from typing import List
from tqdm import tqdm

from fjsspw_solver import Encoding, GAParams
from fjsspw_solver.genetic_algorithm import Method, MethodParams

from src.util.benchmark_parser import WorkerBenchmarkParser
from src.util.graph import Graph
from src.util.uncertainty import create_uncertainty_vector


def run_ga(instances_root: Path, ga_params: GAParams) -> int:
    instance = ga_params.instance
    parser = WorkerBenchmarkParser()
    encoding_py = parser.parse_benchmark(str(instances_root / f"{instance}.fjs"))
    uncertainty_parameters = create_uncertainty_vector(encoding_py.n_operations(), factor=10.0, offset=1.0)

    def uncertain_eval_function(sequence, machines, workers, start_times, end_times, iters: int = 1) -> List|float:
        logger.debug(
                    f"sequence={sequence}"
                    f", machines={machines}"
                    f", workers={workers}"
                    f", job_sequence={encoding_py.job_sequence()}"
                    f", start_times={start_times}"
                    f", end_times={end_times}")
        fitnesses = [0] * iters
        for i in range(iters):
            g = Graph(start_times, end_times, machines, workers, encoding_py.job_sequence())
            g.simulate(encoding_py.durations(), uncertainty_parameters, processing_times=True)
            fitnesses[i] = max(g.e)
        return fitnesses

    params = MethodParams(
        ga_params = ga_params,
        fitness_fun_evals = 5_000_000,
        fitness_fun_evals_per_indv = 3, 
    )
    
    encoding = Encoding(encoding_py.durations().tolist(), encoding_py.job_sequence())
    ga = Method(params, encoding, uncertain_eval_function)
    
    fitness = ga.solve()
    
    return fitness


def repeated_experiment(instances_root: Path, config: Path, runs: int):
    ga_params = GAParams.load(config)
    root_log_dir = Path(ga_params.log_directory)
    for i in tqdm(range(runs), desc="Running GA experiments"):
        run_dir = root_log_dir / f"run_{i}"
        run_dir.mkdir(parents=True, exist_ok=True)
        ga_params.log_directory = str(run_dir)
        run_ga(instances_root, ga_params)
    
    for run in root_log_dir.iterdir():
        if run.is_file():
            continue
        


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--instances", "-i", help="Root directory for instances", type=Path, default=Path("instances/fjssp-w"))
    parser.add_argument("--config", "-c", help="Path to the configuration file for GA", type=Path, required=True)
    parser.add_argument("--runs", "-n", help="How many times to execute each instance", type=int, default=10)
    return parser.parse_args()


def main():
    args = parse_args()
    instances_root = args.instances
    
    repeated_experiment(instances_root, args.config, args.runs)


if __name__ == "__main__":
    main()