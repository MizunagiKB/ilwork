PYTHON = python3
PYUIC = pyuic5
PYRCC = pyrcc5

SRCS = src/ui/frm_main.ui src/ui/frm_potrace.ui src/ui/frm_watershed.ui src/ui/frm_check.ui src/ui/frm_x_test.ui src/resource.qrc
UIDSTS = $(SRCS:%.ui=%.py)
RCDSTS = $(SRCS:%.qrc=%.py)

%.py: %.ui
	$(PYUIC) --resource-suffix="" $< -o $@

%.py: %.qrc
	$(PYRCC) $< -o $@

.PHONY: all
all: $(UIDSTS) $(RCDSTS)

.PHONY: clean
clean:
	rm src/ui/frm_main.py
	rm src/resource.py

.PHONY: run
run: all
	$(PYTHON) src/ilwork.py

# required py2app
# alias mode only
.PHONY: build
build: all
	pushd src && python setup_mac.py py2app --alias && popd
