VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

UNAME := $(shell uname -s 2>/dev/null || echo unknown)

IS_LINUX := $(filter Linux,$(UNAME))
IS_WINDOWS := $(findstring MINGW,$(UNAME))$(findstring MSYS,$(UNAME))$(findstring CYGWIN,$(UNAME))


install:
	@echo "Creating virtual environment..."

	ifeq ($(IS_LINUX), Linux)
		@python3 -m venv $(VENV)
	else
		@python -m venv $(VENV)
	endif

	@echo "Installing requirements..."
	@$(PIP) install -r requirements.txt
	@echo "Done"

run:
	@echo "Running app..."
	@$(PYTHON) api.py
 @$(PYTHON) web_ui_server.py

clean:
	@echo "Cleaning virtual environment..."
	@rm -rf $(VENV)
	@echo "Done"

test:
	@echo "run tests"
	@$(VENV)/bin/python test/api_test_user.py
	@$(VENV)/bin/python test/api_test_chat.py
	@$(VENV)/bin/python test/api_test_media.py

.PHONY: install run clean
