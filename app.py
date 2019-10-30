from flask import Flask
from MOOC.spiders.mooc_spider import Moocspider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

app = Flask(__name__)

def run_spider(course):
    video = None
    process = CrawlerProcess(get_project_settings())
    process.crawl(Moocspider, urls=course, video=video)
    process.start()

@app.route("/course/<course>", methods=['GET'])
def spider(course):
    p = Process(target=run_spider, args=(course, ))
    p.start()
    p.join()
    return f"Spider is crawling: {course}"


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)