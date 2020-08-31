.PHONY: init test install

init:
	pip install -r requirements.txt

test:
	pytest tests --cov twitter_scrapper --cov-report term-missing -s -p no:warnings --log-cli-level error

install:
	python setup.py install
