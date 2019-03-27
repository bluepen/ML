# -*- coding: utf-8 -*-
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AlibabaPipeline(object):

    def __init__(self):
        self.file = open("alibaba_job.json","w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(content)
        return item

    def close_item(self,spider):
        self.file.close()