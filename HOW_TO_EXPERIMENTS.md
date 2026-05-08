# How to reproduce the experiments

```bash
# Create the configurations and output directory + build the application
make experiments

# Create the bash script that runs all experiments with correct configs
make experiments EXEC=<path/to/the/built/executable>

# Make the run script executable
chmod u+x run_experiments.sh

# Run experiments
./run_experiments.sh
```