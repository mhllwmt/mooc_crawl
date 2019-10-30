from MOOC.spiders.mooc_spider import Moocspider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# USTB-299003,ZJU-93001
# urls = ['USTB-299003', 'ZJU-93001', 'NUDT-9004']
urls = input("输入课程资源id:  ").split(',')
print(urls)
video = None
process = CrawlerProcess(get_project_settings())
process.crawl(Moocspider, urls=urls, video=None)
process.start()
