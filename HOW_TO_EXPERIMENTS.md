# How to reproduce the experiments

## Info

- Each `append...` script builds the application and appends run configurations to the `./run_experiments.sh` script.

## Deterministic - FJSSP-W (new way)
### Each optimisation run on a different core, with nohup
```bash
# It will build the application with Release build type and ask you to pass the path to the executable
./append_deterministic_experiments_multicore_nohup.sh

# Second run of the script will prepare another script meant for running the experiments
./append_deterministic_experiments_multicore_nohup.sh 30 <path/to/exec>

# Run experiments with a throttle of N processes at once
nohup bash -c 'cat run_experiments.sh | sed "s/&\s*$//" | xargs -P <N> -I {} bash -c "{}"' > manager.log 2>&1 &
```

### Each instance (N runs) on a diffent core, with nohup
```bash
# It will build the application with Release build type and ask you to pass the path to the executable
./append_deterministic_experiments_nohup.sh

# Second run of the script will prepare another script meant for running the experiments
./append_deterministic_experiments_nohup.sh 30 <path/to/exec>

# Then to run experiments
./run_experiments.sh
```

### All instances on a single core
```bash
# It will build the application with Release build type and ask you to pass the path to the executable
./append_deterministic_experiments.sh

# Second run of the script will prepare another script meant for running the experiments
./append_deterministic_experiments.sh 30 <path/to/exec>

# Then to run experiments
./run_experiments.sh
```

## Deterministic - FJSSP-W (old way)

```bash
# Create the configurations and output directory + build the application
make experiments

# Create the bash script that runs all experiments with correct configs
make experiments EXEC=<path/to/the/built/executable>

# Alternatively if you want to run experiments in parallel on Linux system add -nohup
make experiments-nohup EXEC=<path/to/the/built/executable>

# Make the run script executable
chmod u+x run_experiments.sh

# Run experiments
./run_experiments.sh
```

## Undeterministic - FJSSP-WU

### Each optimisation run on a different core, with nohup
```bash
# It will build the application with Release build type and ask you to pass the path to the executable
./append_uncertainty_experiments_multicore_nohup.sh

# Second run of the script will prepare another script meant for running the experiments
./append_uncertainty_experiments_multicore_nohup.sh 30 <path/to/exec>

# Run experiments with a throttle of N processes at once
nohup bash -c 'cat run_experiments.sh | sed "s/&\s*$//" | xargs -P <N> -I {} bash -c "{}"' > manager.log 2>&1 &
```

### Each instance (N runs) on a diffent core, with nohup
```bash
# It will build the application with Release build type and ask you to pass the path to the executable
./append_uncertainty_experiments_nohup.sh

# Second run of the script will prepare another script meant for running the experiments
./append_uncertainty_experiments_nohup.sh 30 <path/to/exec>

# Then to run experiments
./run_experiments.sh
```

### All instances on a single core
```bash
# It will build the application with Release build type and ask you to pass the path to the executable
./append_uncertainty_experiments.sh

# Second run of the script will prepare another script meant for running the experiments
./append_uncertainty_experiments.sh 30 <path/to/exec>

# Then to run experiments
./run_experiments.sh
```

# Outputs

All outputs will be available under `out/logs/<deterministic/uncertainty-factorX>/`

When running with `nohup` there will be another output directory with all stdout and stderr outputs from all instances under `nohup-out/<instance>.out`

## Structure

- `./<instance>` - directory with all logs related to `<instance>`
- `./<instance>/run_x` - x-th run of the instance
- `./<instance>/run_x/evolution.log` - saved log of the optimization, includes columns: `generation`,`worst`,`avg`,`best`,`best_so_far`,`evals`
- `./<instance>/run_x/best.out` - best found solution; fields, separated with new lines: `fitness`, `sequence`, `machines`, `workers`, `start_times`, `end_times`
- `./<instance>/config.cfg` - configuration file used to run the instance
- `./<instance>/results.csv` - final csv with all neccessary info for the competition; includes fields: `Instance`,`Fitness`,`FunctionEvaluations`,`StartTimes`,`MachineAssignments`,`WorkerAssignments`