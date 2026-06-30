VENV   := ../.venv
PYTHON := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip

.PHONY: all install run

all: run

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r ../requirements.txt

run: install
	$(PYTHON) ../tts.py --dir .
