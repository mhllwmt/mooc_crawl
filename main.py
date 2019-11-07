from MOOC.spiders.mooc_spider import Moocspider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


# USTB-299003,ZJU-93001,PKU-1003479006，BIT-268001
urls = ['BIT-268001']
# urls = input("输入课程资源id:  ").split(',')
print(urls)
video = None
process = CrawlerProcess(get_project_settings())
process.crawl(Moocspider, urls=urls, video=0)
process.start()

shell_str = 'ffmpeg -i {}.m3u8 -vcodec copy -acodec copy {}.mp4'
now = os.getcwd()
for root, dir, files in os.walk("..\\data"):
    for file in files:
        if '.m3u8' in file:
            name = file.strip('.m3u8')
            os.chdir(root)
            s = shell_str.format(name, name)
            print(s)
            os.system(s)
            os.chdir(now)



