# -*- coding: utf-8 -*-
import os
import json
from lkmlspider.items import LkmlEmailItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
archive_dir = "archive/"

class LkmlspiderPipeline(object):
    def process_item(self, item, spider):
    	filename = archive_dir + "lkml." + item['year'] + "." + item['month'] + "." + item['day'] + "." + item['number'] + ".email.json"
    	#self.filename = archive_dir + "lkml." + str(item['date']) + ".email.json"
    	self.file = open(filename, 'w')
    	line = json.dumps(dict(item))
    	# this does not use item exporters as these seem to be made to output to one file
    	self.file.write(line)
    	# this log here would neet importing # self.log("This is the pipeline")
    	self.file.close()
    	return item