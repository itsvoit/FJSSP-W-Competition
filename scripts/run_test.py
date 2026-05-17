import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

# append source to path

from constants import *
from util.graph import Graph
from util.uncertainty import create_uncertainty_vector
from util.benchmark_parser import WorkerBenchmarkParser
from fjsspw_solver.plotting import (
    plot_fjsspw_gantt,
    plot_learning_progress,
    boxplots_from_experiment_results,
    plot_single_instance_single_run,
    plot_multiple_instance_runs,
)
from fjsspw_solver.operators import (
    Selections,
    Crossovers,
    Mutations,
    CrossoverParams,
    SelectionParams,
    MutationParams,
)
from fjsspw_solver.genetic_algorithm import (
    Method,
    MethodParams,
    ClonesRemoval,
)
from fjsspw_solver import (
    Individual,
    Encoding,
)
import time
from copy import copy
from pprint import pprint
from pathlib import Path
from typing import Optional, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

logging.basicConfig(
    level=logging.WARNING,
    # level=logging.INFO,
    # level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s(): %(message)s"
)
logger = logging.getLogger(__name__)

PROD = False


base_method_params = MethodParams.from_file(ROOT / 'config/method.cfg')

parser = WorkerBenchmarkParser()
instance_name = base_method_params.instance_name

encoding = parser.parse_benchmark(INSTANCE_FJSSPW_PATH / f'{instance_name}')
np_durations = encoding.durations()
encoding = Encoding(np_durations.tolist(), encoding.job_sequence())

uncertainty_parameters = create_uncertainty_vector(
    encoding.n_operations(), factor=10.0, offset=1.0)


def deterministic_eval_function(indv: Individual, iters: int = 1) -> float:
    return indv.get_internal_fitness()


def uncertain_eval_function(indv: Individual, iters: int = 1) -> List | float:
    logger.debug(f"Enter uncertain eval function: indv={indv.to_string()}")
    sequence, machines, workers, start_times, end_times = indv.get_representation()
    logger.debug(
        f"sequence={sequence}"
        f", machines={machines}"
        f", workers={workers}"
        f", job_sequence={encoding.get_job_sequence()}"
        f", start_times={start_times}"
        f", end_times={end_times}")
    fitnesses = [0] * iters
    for i in range(iters):
        g = Graph(start_times, end_times, machines,
                  workers, encoding.get_job_sequence())
        g.simulate(encoding.get_durations(),
                   uncertainty_parameters, processing_times=True)
        fitnesses[i] = max(g.e)
    return fitnesses if iters > 1 else fitnesses[0]


def evaluate_custom_method_with_params(method_class, params: MethodParams, encoding: Encoding, gantt: bool = False, zoom: bool = False):
    method = method_class(params, encoding, deterministic_eval_function)
    best_indv = method.solve()
    print(best_indv.get_representation())
    plot_single_instance_single_run(method, gantt)
    if zoom:
        c = best_indv.get_internal_fitness()
        robust_c = method.fitness_fun(best_indv)
        plot_learning_progress(method.get_log_file_path(),
                               params, c=c, robust_c=robust_c, zoom=zoom)
    return best_indv


def evaluate_method_with_params(params: MethodParams, encoding: Encoding, gantt: bool = False, zoom: bool = False):
    return evaluate_custom_method_with_params(Method, params, encoding, gantt, zoom)


def evaluate_method_with_params_for_stats(params: MethodParams, encoding: Encoding, n: int, runs: Optional[list] = None):
    method = None
    if not runs:
        runs = []
        for i in range(n):
            method = Method(params, encoding, deterministic_eval_function)
            best_indv = method.solve()

            c = best_indv.get_internal_fitness()
            robust_c = deterministic_eval_function(best_indv)
            runs.append((c, robust_c, method.get_log_file_path()))
    plot_multiple_instance_runs(params, runs)
    return runs


pprint(base_method_params)


logger.info("Init method")
method = Method(base_method_params, encoding, deterministic_eval_function)
logger.info("Finish init method")


best_indv = method.solve()
