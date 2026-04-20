
from typing import List, Tuple, Optional

from util.graph import Graph
from util.uncertainty import create_uncertainty_vector

from fjsspw_solver import (
    Individual,
    Encoding,
)
from fjsspw_solver.genetic_algorithm import (
    MethodParams
)
from fjsspw_solver.plotting import (
    plot_single_instance_single_run,
    plot_multiple_instance_runs,
)

import logging
logger = logging.getLogger(__name__)


def make_uncertain_eval_function(uncertainty_parameters: List[Tuple[float, float, float]]):
    def uncertain_eval_function(indv: Individual, iters: int = 1) -> List | float:
        encoding = indv.encoding
        _, machines, workers, start_times, end_times = indv.get_representation()
        logger.debug(f"machines={machines}"
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
    return uncertain_eval_function


def make_evaluation_function(method_class, uncertain_eval_function):
    def evaluate_custom_method_with_params(params: MethodParams, encoding: Encoding, gantt: bool = False):
        method = method_class(params, encoding, uncertain_eval_function)
        best_indv = method.solve()
        print(best_indv.get_representation())
        plot_single_instance_single_run(method, gantt)
    return evaluate_custom_method_with_params


def make_repeated_evaluation_function(method_class, uncertain_eval_function):
    def evaluate_method_with_params_for_stats(params: MethodParams, encoding: Encoding, n: int, runs: Optional[list] = None):
        method = None
        if not runs:
            runs = []
            for i in range(n):
                method = method_class(
                    params, encoding, uncertain_eval_function)
                best_indv = method.solve()

                c = best_indv.get_internal_fitness()
                robust_c = uncertain_eval_function(best_indv)
                runs.append((c, robust_c, method.get_log_file_path()))
        plot_multiple_instance_runs(params, runs)
        return runs
    return evaluate_method_with_params_for_stats
