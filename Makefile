.PHONY: help
help: ## Lists the available commands. Add a comment with '##' to describe a command.
	@grep -E '^[a-zA-Z_-].+:.*?## .*$$' $(MAKEFILE_LIST)\
		| sort\
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Setup extension in ~/.local/share/ulauncher/extensions/
	ln -sf $(shell pwd) ~/.local/share/ulauncher/extensions/
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

.PHONY: start
start: ## Attemps to kill current ulauncher process and starts a new one.
	ps aux | grep ulauncher | grep -v grep | awk '{print $$2}' | xargs kill -9
	ulauncher --dev -v > ulauncher.log 2>&1 &
