from flask import Flask
from MOOC.spiders.mooc_spider import Moocspider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

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

@app.route("/test", methods=["GET"])
def test():
    return "hello world"


if __name__ == "__main__":
    app.run(host="localhost", port=8081, debug=True)