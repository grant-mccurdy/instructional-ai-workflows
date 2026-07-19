.PHONY: all check demo pages precalculus-demo validate visual-smoke

PYTHON ?= python3

all: check

check: demo validate pages visual-smoke

demo: precalculus-demo

precalculus-demo:
	$(PYTHON) demos/precalculus_frq/run_demo.py

validate:
	$(PYTHON) scripts/validate_demo.py

pages:
	$(PYTHON) scripts/build_pages.py

visual-smoke:
	node scripts/visual_smoke.mjs
