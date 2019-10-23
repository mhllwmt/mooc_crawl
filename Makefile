PROGRAM=mooc crawler
TAG=1.0

env:
	virtualenv venv
	. venv/bin/activate
	pip install -r requirements.txt

run:
	scrapy runspider mooc_crawler/mooc_crawler/spiders/mooc.py -a category=$(CATEGORY) -a username=$(USERNAME) -a password=$(PASSWORD)