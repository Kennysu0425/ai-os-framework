PYTHON ?= python3

.PHONY: bootstrap demo validate clean

bootstrap:
	bash scripts/bootstrap.sh

demo:
	$(PYTHON) scripts/build_demo_war_room_snapshot.py
	@echo "Open demo/war_room/index.html"

validate:
	$(PYTHON) scripts/validate_contracts.py

clean:
	rm -rf output
