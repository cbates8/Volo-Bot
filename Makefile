# https://opensource.com/article/18/8/what-how-makefile

#############
# Variables #
#############

# ?= -> Only set if var doesn't have a value
WORK_DIR ?= $(shell pwd)


##################
# Docker-Compose #
##################

down:
	@docker compose down ${APP}

up:
	@docker compose up -d ${APP}

bounce: down up

stop:
	@docker compose stop ${APP}

start:
	@docker compose start ${APP}

restart:
	@docker compose restart ${APP}

build:
	@docker compose build ${APP}

rebuild: down build up

build-nc:
	@docker compose build ${APP} --no-cache

rebuild-nc: down build-nc up

logs:
	@docker compose logs volobot


#################
# General Utils #
#################


# Install requirements.txt to venv
install:
	@. .venv/bin/activate; \
	pip install -r requirements.txt; \


###############
# Code Health #
###############

# Format code body, DIR=[file or directory]
black: needs-dir
	@echo
	@echo "Checking format for $(DIR)"
	@find $(WORK_DIR)/$(DIR) -name "*.py" | xargs -I{} pre-commit run black --hook-stage manual --files {}

# Format imports, DIR=[file or directory]
isort: needs-dir
	@find $(WORK_DIR)/$(DIR) -name "*.py" | xargs -I{} pre-commit run isort --hook-stage manual --files {}

# Format code using black (body) + isort (imports), DIR=[file or directory]
format: needs-dir black isort

# Lint, DIR=[file or directory]
lint: needs-dir
	@echo
	@echo "Checking lint for $(DIR)"
	@find $(WORK_DIR)/$(DIR) -name "*.py" | xargs -I{} pre-commit run ruff --hook-stage manual --files {}

# Format, lint, typecheck (TDOD), DIR=[file or directory]
healthy: needs-dir format lint


###################
# Ensure env Vars #
###################

needs-dir:
ifeq ($(strip $(DIR)),)
	@echo "DIR not set!"
	@exit 1
endif
