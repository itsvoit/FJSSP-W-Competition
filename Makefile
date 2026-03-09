SHELL := /bin/bash

# .PHONY ensures these targets run even if files with these names exist
.PHONY: build test clean uninstall

build: uninstall
	pip install --no-build-isolation --check-build-dependencies -ve ./solver -Ccmake.define.CMAKE_EXPORT_COMPILE_COMMANDS=1 -Cbuild-dir=build

clean:
	rm -rf solver/build

uninstall:
	pip uninstall fjsspw-solver -y

retest: build
	pytest solver/tests

test:
	pytest solver/tests
