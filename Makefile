.PHONY: demo precalculus-demo

PYTHON ?= python3

demo: precalculus-demo

precalculus-demo:
	$(PYTHON) demos/precalculus_frq/run_demo.py
