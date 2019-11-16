PROGRAM = mooc spider
VERSION = 1.0

URLS = ${urls}
VIDEO = ${video}

deploy:
	docker-compose up -d

build:
	docker-compose build

run:
	scrapy crawl mooc -a urls="${URLS}" -a video=${VIDEO}