PROGRAM=mooc crawler
TAG=1.0
URLS='USTB-299003'
VIDEO=0
export DB_HOST=localhost
export DB_PORT=27017
export DB_NAME=mooc
export DB_COLLECTION=mooc

env:
	virtualenv venv

vir: env
	. venv/bin/activate

require: vir
	pip install -r requirements.txt

run:
	scrapy runspider MOOC/spiders/mooc_spider.py -a urls=$(URLS) -a video=$(VIDEO)

app:
	python app.py