from os import PathLike
import random
from typing import List, Tuple


def create_uncertainty_vector_from_instance(instance_path: PathLike, factor: float):
    with open(instance_path, mode='r', encoding='utf-8') as handle:
        line = handle.readline().split()
        jobs, machines, workers = line[0], line[1], line[2]
        jobs, machines, workers = int(jobs), int(machines), int(workers)
    
    return create_uncertainty_vector(workers, factor)

def create_uncertainty_vector(n_workers, factor : float = 10.0):
    uncertainty_parameters = []
    for _ in range(n_workers):
        alpha = random.random()
        beta = factor * alpha
        uncertainty_parameters.append([alpha, beta])
    return uncertainty_parameters


def write_uncerainty_to_file(uncertainties: List[Tuple[float, float]], file: PathLike):
    with open(file, mode='w', encoding='utf-8') as handle:
        print(len(uncertainties), file=handle)
        for alpha, beta in uncertainties:
            print(f"{alpha} {beta}", file=handle)