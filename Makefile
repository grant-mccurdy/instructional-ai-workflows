.PHONY: all demo precalculus-demo

PYTHON ?= python3

all: demo

demo: precalculus-demo

precalculus-demo:
	$(PYTHON) demos/precalculus_frq/run_demo.py
