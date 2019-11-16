from flask import Flask
from MOOC.spiders.mooc_spider import Moocspider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from flask_cors import *

app = Flask(__name__, static_folder='frontend')
CORS(app, supports_credentials=True)


def run_spider(course):
    process = CrawlerProcess(get_project_settings())
    process.crawl(Moocspider, urls=[course], video=0)
    process.start()


@app.route("/course/<course>", methods=['GET'])
def spider(course):
    p = Process(target=run_spider, args=(course, ))
    p.start()
    p.join()
    return f"Spider is crawling: {course}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True) 
