SHELL := /bin/bash

# .PHONY ensures these targets run even if files with these names exist
.PHONY: build rebuild test retest clean uninstall

build: uninstall
	pip install --no-build-isolation --check-build-dependencies -ve ./solver -Ccmake.define.CMAKE_EXPORT_COMPILE_COMMANDS=1 -Cbuild-dir=build

rebuild: clean build

clean:
	rm -rf solver/build

uninstall:
	pip uninstall fjsspw-solver -y

test:
	pytest solver/tests

retest: build test
