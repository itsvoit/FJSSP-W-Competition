from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


small = True
medium = True
large = True
very_large = True



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
    uncertainty_params_path: Optional[Path] = None
    evaluations: int = 3
    
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
            if self.mutation.upper() == 'ADAPTIVE':
                print(f"NEIGH_CNT {self.neigh_cnt}", file=handle)
                print(f"CLEAR_WEIGHTS_INTERVAL {self.clear_weights_interval}", file=handle)
                print(f"MIN_NEIGH_PROB {self.min_neigh_prob}", file=handle)
            if self.uncertainty_params_path:
                print(f"UNCERTAINTY_PARAMS_PATH {self.uncertainty_params_path}", file=handle)
                print(f"EVALUATIONS {self.evaluations}", file=handle)


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

deterministic_instance_to_config_map: Dict[str, Optional[Config]] = {
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


# Small
small_instance_config = Config(
    # generations = 124999//3,
    generations = 10000,
    population_size = 40,
    selection_size = 5,
    crossover_prob = 0.01,
    mutation_prob = 0.01,
    mutation = "MIXED",
    crossover = "MOX",
    evaluations=4,
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


uncertainty_instance_to_config_map: Dict[str, Optional[Config]] = {
    # "0_BehnkeGeiger_42_workers": small_instance_config,
    # "0_BehnkeGeiger_46_workers": medium_rigid_instance_config,
    # "0_BehnkeGeiger_60_workers": very_large_instance_config,
    # "1_Brandimarte_12_workers": large_instance_config,
    # "1_Brandimarte_14_workers": large_instance_config,
    # "1_Brandimarte_7_workers": medium_flexible_instance_config,
    # "2a_Hurink_sdata_1_workers": small_instance_config,
    # "2a_Hurink_sdata_18_workers": medium_flexible_instance_config,
    # "2a_Hurink_sdata_38_workers": very_large_instance_config,
    # "2a_Hurink_sdata_40_workers": large_instance_config,
    # "2a_Hurink_sdata_54_workers": medium_rigid_instance_config,
    # "2a_Hurink_sdata_61_workers": medium_flexible_instance_config,
    # "2a_Hurink_sdata_63_workers": medium_rigid_instance_config,
    # "2b_Hurink_edata_1_workers": small_instance_config,
    # "2b_Hurink_edata_6_workers": small_instance_config,
    # "2c_Hurink_rdata_28_workers": large_instance_config,
    # "2c_Hurink_rdata_38_workers": very_large_instance_config,
    # "2c_Hurink_rdata_50_workers": small_instance_config,
    # "2d_Hurink_vdata_18_workers": medium_flexible_instance_config,
    # "2d_Hurink_vdata_30_workers": large_instance_config,
    # "2d_Hurink_vdata_5_workers": small_instance_config,
    # "3_DPpaulli_15_workers": very_large_instance_config,
    # "3_DPpaulli_18_workers": very_large_instance_config,
    # "3_DPpaulli_1_workers": large_instance_config,
    # "3_DPpaulli_9_workers": large_instance_config,
    # "4_ChambersBarnes_10_workers": large_instance_config,
    # "5_Kacem_3_workers": small_instance_config,
    # "5_Kacem_4_workers": small_instance_config,
    # "6_Fattahi_14_workers": small_instance_config,
    "6_Fattahi_20_workers": small_instance_config,
}