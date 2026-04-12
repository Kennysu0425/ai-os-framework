PYTHON ?= python3

.PHONY: bootstrap demo validate images serve clean

bootstrap:
	bash scripts/bootstrap.sh

demo:
	$(PYTHON) scripts/build_demo_war_room_snapshot.py
	@echo "Open demo/war_room/index.html"

validate:
	$(PYTHON) scripts/validate_contracts.py

images:
	$(PYTHON) scripts/generate_demo_hero.py
	$(PYTHON) scripts/generate_showcase_assets.py

serve:
	@echo "Serving at http://localhost:8000"
	$(PYTHON) -m http.server 8000

clean:
	rm -rf output
