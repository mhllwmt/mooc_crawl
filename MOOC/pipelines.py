# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from MOOC.items import MoocItem, MlItem, TsItem
nolaw = '<>/\\|:*\'\"' #命名不合法的字符 ‘#’替代
import codecs, json, scrapy

class MoocPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        # FilesPepeline 根据file_urls指定的url进行爬取，该方法为每个url生成一个Request后 Return
        if isinstance(item, MoocItem):
            for file_url in item['file_urls']:
                if file_url!='':
                    yield scrapy.Request(file_url, meta={'name':item['file_name'], 'type':item['file_type'] })

    def file_path(self, request, response=None, info=None):
        for it in nolaw:
            request.meta['name'][-1] = request.meta['name'][-1].replace(it, '#')
        if request.meta['type'] == 'pdf':
            filename = '{}/{}/{}/{}.pdf'.format(*request.meta['name'])
        elif request.meta['type'] == 'video':
            filename = '{}/{}/{}/{}.mp4'.format(*request.meta['name'])
        else:
            filename = '{}/{}/{}/{}.srt'.format(*request.meta['name'])
        return filename


class MlPipeline(object):
    def __init__(self):
        self.file = codecs.open('../data/ml.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        if isinstance(item,MlItem):
            lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(lines)
            return item

    def spider_closed(self, spider):
        self.file.close()


class TsPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, TsItem):
            for file_url in item['file_urls']:
                if file_url != '':
                    yield scrapy.Request(file_url, meta={'name':item['file_name']})

    def file_path(self, request, response=None, info=None):
        for it in nolaw:
            request.meta['name'][-1] = request.meta['name'][-1].replace(it, '#')
        # input(request.meta['name'][-1])
        filename = '{}/{}/{}/{}.ts'.format(*request.meta['name'])
        return filename