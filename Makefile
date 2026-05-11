SHELL := /bin/bash
EXEC := echo
RUNS := 10

# .PHONY ensures these targets run even if files with these names exist
.PHONY: build-prod rebuild test retest clean uninstall experiments

# Native application targets
# 	Production build
build-prod:
	cmake -S ./solver -B ./solver/build-prod/ -DCMAKE_BUILD_TYPE=Release -DBUILD_PYTHON=OFF
	cmake --build ./solver/build-prod/ --target fjsspw_solver_cpp --config Release

run-prod: build-prod
	./solver/build-prod/Release/fjsspw_solver_cpp.exe "solver/config/ga.cfg" "instances/Example_Instances_FJSSP-WF"

# 	Debug build
build-debug:
	cmake -S ./solver -B ./solver/build-debug/ -DCMAKE_BUILD_TYPE=Debug -DBUILD_PYTHON=OFF
	cmake --build ./solver/build-debug/ --target fjsspw_solver_cpp

build-profile:
	cmake -S ./solver -B ./solver/build-profile/ -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_PYTHON=OFF
	cmake --build ./solver/build-profile/ --target fjsspw_solver_cpp --config RelWithDebInfo

run-debug: build-debug
	./solver/build-debug/Debug/fjsspw_solver_cpp.exe "solver/config/ga.cfg" "instances/Example_Instances_FJSSP-WF"

# 	Remove all builds
clean: clean-py
	rm -rf solver/build-debug
	rm -rf solver/build-prod

# Python bindings
build-py: uninstall
	pip install --no-build-isolation --check-build-dependencies -ve ./solver -Ccmake.define.CMAKE_EXPORT_COMPILE_COMMANDS=1 -Cbuild-dir=build-python

clean-py:
	rm -rf solver/build-python

uninstall:
	pip uninstall fjsspw-solver -y

test:
	pytest solver/tests

retest: build-py test

experiments: build-prod
	python -m prepare_experiments deterministic -e $(EXEC) -n $(RUNS)
	chmod u+x run_experiments.sh
	@echo "=========================================================================="
	@echo "  Replace all 'echo' calls in 'run_experiments.sh' with the actual built  "
	@echo "  executable to finish preparing the experiments.                         "
	@echo "  Or simply add 'EXEC=<path/to/exec>' when running this target, like:     "
	@echo "  'make experiments EXEC=<path>'                                          "
	@echo "                                                                          "
	@echo "  Execute all experiments:                                                "
	@echo "    ./run_experiments.sh                                                  "
	@echo "=========================================================================="

clean-experiments:
	rm -rf out/logs

run-experiments: clean-experiments experiments
	./run_experiments.sh

# Python experiments (uncertain fitness evaluation function)
experiments-python: build-py
	python -m prepare_experiments uncertainty --output out/logs/uncertainty --run $(RUNS)

experiments-python-nohup: build-py
	python -m prepare_experiments uncertainty --output out/logs/uncertainty --run $(RUNS) --nohup

run-experiments-python: experiments-python
	./run_experiments.sh

run-experiments-python-nohup: experiments-python-nohup
	./run_experiments.sh
