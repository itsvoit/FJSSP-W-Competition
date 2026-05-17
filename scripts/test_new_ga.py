import os
import sys
from pathlib import Path

from fjsspw_solver.genetic_algorithm import MethodParams

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from pathlib import Path

from fjsspw_solver import GeneticAlgorithm, Individual, Encoding, GAParams
from fjsspw_solver.plotting import plot_fjsspw_gantt, plot_learning_progress

from util.benchmark_parser import WorkerBenchmarkParser

from constants import *

from pprint import pprint
from time import perf_counter


def print_pop(ga):
    sequences, machines, workers, sts, ets = ga.population.representations
    fit = ga.population.fitnesses
    for i in range(len(sequences)):
        print(f" ---\nIndv {i}: {fit[i]}")
        print(sequences[i])
        print(machines[i])
        print(workers[i])
        print(sts[i])
        print(ets[i])
        # plot_fjsspw_gantt(
        #     sequences[i],
        #     machines[i],
        #     workers[i],
        #     sts[i],
        #     ets[i],
        #     encoding
        # )
    print(f" --- ")

parser = WorkerBenchmarkParser()
instance_name = 'Fattahi20'
instance_path = INSTANCE_FJSSPW_PATH / f'{instance_name}.fjs'
encoding = parser.parse_benchmark(str(instance_path))

encoding = Encoding(encoding.durations().tolist(), encoding.job_sequence())

print("-" * 20)
print("Encoding info")
print("n_operations:", encoding.n_operations())
print("n_machines:", encoding.n_machines())
print("n_workers:", encoding.n_workers())
print("n_jobs:", encoding.n_jobs())
print("-" * 20)

log_file = "method_py.log"
generations = 100
population_size = 100
selection_size = 100
crossover_prob = 0.0
mutation_prob = 0.00
remove_clones = False

params = GAParams(
    log_file,
    generations,
    population_size,
    selection_size,
    crossover_prob,
    mutation_prob,
    remove_clones,
)

plotting_params = MethodParams()
plotting_params.instance_name = instance_name
plotting_params.bounds_file = "./instances/InstanceData/FJSSP-W/best_known.csv"

ga = GeneticAlgorithm(params, encoding, True)


start = perf_counter()
ga.run_optimization()
end = perf_counter()

print(f"Optimization took {end-start:.4f} seconds")

best = ga.get_all_time_best_indv()
print(best)

plot_learning_progress(log_file, plotting_params, zoom=False, show_title=False)