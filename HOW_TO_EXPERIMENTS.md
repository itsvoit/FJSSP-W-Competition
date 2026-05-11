# How to reproduce the experiments

## Deterministic - FJSSP-W

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

```bash
# Craete a virtual environment of your choice (here: venv)
python -m venv venv

# Active the virtual env
source venv/bin/activate

# Build the application and install the python package
make experiments-python

# Alternatively if you want to run experiments in parallel on Linux system add -nohup
make experiments-python-nohup

# Make the run script executable
chmod u+x run_experiments.sh

# Run experiments
./run_experiments.sh
```

# Outputs

All outputs will be available under `out/logs/<deterministic/uncertainty>/`

## Structure

- `./<instance>` - directory with all logs related to `<instance>`
- `./<instance>/run_x` - x-th run of the instance
- `./<instance>/run_x/evolution.log` - saved log of the optimization, includes columns: `generation`,`worst`,`avg`,`best`,`best_so_far`,`evals`
- `./<instance>/run_x/best.out` - best found solution; fields, separated with new lines: `fitness`, `sequence`, `machines`, `workers`, `start_times`, `end_times`
- `./<instance>/config.cfg` - configuration file used to run the instance
- `./<instance>/results.csv` - final csv with all neccessary info for the competition; includes fields: `Instance`,`Fitness`,`FunctionEvaluations`,`StartTimes`,`MachineAssignments`,`WorkerAssignments`