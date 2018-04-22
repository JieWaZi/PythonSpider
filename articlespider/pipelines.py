# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb.cursors
from twisted.enterprise import adbapi


class AritclespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 自定义下载图片
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for key, value in results:
            image_path = value["path"]
        item["image_path"] = image_path

        return item


# 数据库操作
class MySQLPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.hand_error, item, spider)

    def do_insert(self, cursor, item):
        insert_sql = "insert into article values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_sql, (
            item["id"], item["title"], item["url"], item["create_time"], item["image_url"], item["image_path"],
            item["fav_nums"], item["comment_nums"], item["praise_nums"], item["content"], item["tag"])
                       )

    def hand_error(self, failure, item, spider):
        print(failure)
