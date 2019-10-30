# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from MOOC.items import MoocItem, MlItem
import codecs, json, scrapy
import pymongo
from MOOC.settings import mongo_host, mongo_port, mongo_db_name, mongo_db_collection

class MoocPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        # FilesPepeline 根据file_urls指定的url进行爬取，该方法为每个url生成一个Request后 Return
        if isinstance(item, MoocItem):
            for file_url in item['file_urls']:
                yield scrapy.Request(file_url, meta={'name':item['file_name'], 'type':item['file_type'] })

    def file_path(self, request, response=None, info=None):
        if request.meta['type'] == 'pdf':
            filename = '{}/{}/{}/{}.pdf'.format(*request.meta['name'])
        else:
            filename = '{}/{}/{}/{}.mp4'.format(*request.meta['name'])
        return filename


class MlPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        sheetname = mongo_db_collection
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]
        # self.file = codecs.open('./data/ml.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
        # if isinstance(item,MlItem):
        #     lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #     self.file.write(lines)
        #     return item

    # def spider_closed(self, spider):
    #     self.file.close()