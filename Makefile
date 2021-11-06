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
	pushd src && $(PYTHON) ilwork.py && popd

.PHONY: build
build: all
	lupdate -pro ilwork.pro -ts src/lang/ilwork_ja-JP.ts
	pushd src && python setup.py build && popd
	pushd src && python setup_post.py && popd
