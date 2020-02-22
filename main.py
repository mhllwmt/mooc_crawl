from MOOC.spiders.mooc_spider import Moocspider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Craw(object):
    def merge(self):
        shell_str = 'ffmpeg -i {}.m3u8 -vcodec copy -acodec copy {}.mp4'
        now = os.getcwd()
        for root, dirs, files in os.walk("..\\data"):
            for file in files:
                name = file[:-5]
                if '.m3u8' in file and '{}.mp4'.format(name) not in files:
                    os.chdir(root)
                    s = shell_str.format(name, name)
                    # print(s)
                    os.system(s)
                    os.chdir(now)

    def f(self, urls, _video=None):
        process = CrawlerProcess(get_project_settings())
        process.crawl(Moocspider, urls=urls, video=_video)
        process.start(stop_after_crawl=True)
        process.stop()


if __name__ == '__main__':
    # USTB-299003,ZJU-93001,PKU-1003479006，BIT-268001
    urls = ['BIT-268001']
    # urls = input("输入课程资源id: ").split(',')
    # print(urls)
    mt = Craw()
    mt.f(urls, 0)
    s = input("是否合并视频: (y/n)")
    if s == 'y':
        mt.merge()
