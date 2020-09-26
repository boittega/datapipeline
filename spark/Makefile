.PHONY: init test run

init:
	pip install -r requirements.txt

test:
	pytest tests --cov twitter_search --cov-report term-missing -s -p no:warnings --log-cli-level error

run:
	python -m twitter_search.transformation --src $(src) --dest $(dest)
