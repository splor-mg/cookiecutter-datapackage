.PHONY: all extract validate transform build check publish clean notify

include config.mk

EXT = txt

RESOURCE_NAMES := $(shell $(PYTHON) main.py resources)
OUTPUT_FILES := $(addsuffix .csv,$(addprefix data/,$(RESOURCE_NAMES)))

all: extract validate transform build check

extract:
	$(foreach resource_name, $(RESOURCE_NAMES),$(PYTHON) main.py extract $(resource_name) &&) true

validate:
	frictionless validate datapackage.yaml

transform: $(OUTPUT_FILES)

$(OUTPUT_FILES): data/%.csv: data-raw/%.$(EXT) schemas/%.yaml scripts/transform.py datapackage.yaml
	$(PYTHON) main.py transform $*

build: transform datapackage.json

datapackage.json: $(OUTPUT_FILES) scripts/build.py datapackage.yaml
	$(PYTHON) main.py build

check:
	frictionless validate datapackage.json

notify: 
	Rscript	scripts/notify.R

publish:
	git add -Af datapackage.json data/*.csv data-raw/*.$(EXT)
	git commit --author="Automated <actions@users.noreply.github.com>" -m "Update data package at: $$(date +%Y-%m-%dT%H:%M:%SZ)" || exit 0
	git push

clean:
	rm -f datapackage.json data/*.csv
