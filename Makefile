# Detect the current shell environment so we can use the right lookup command.
ifeq ($(findstring cmd.exe,$(SHELL)),cmd.exe)
    DEVNUL := NUL
    WHICH := where
else
    DEVNUL := /dev/null
    WHICH := command -v
endif

PYTHON ?= python3
VENV ?= .venv

# Fail immediately if the required runtime is missing.
ifeq ($(shell $(WHICH) $(PYTHON) 2>$(DEVNUL)),)
    $(error "$(PYTHON) is not in your system PATH. Install Python 3 or set PYTHON to a valid interpreter.")
endif

.PHONY: test install

install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && python -m pip install --upgrade pip -r requirements.txt

test:
	. $(VENV)/bin/activate && python -m unittest discover -s tests -p 'test_*.py' -v
