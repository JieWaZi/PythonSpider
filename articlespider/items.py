# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import hashlib
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class AritclespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

def default_time(value):
    try:
        return datetime.datetime.strftime(value, "%Y/%m/%d").date()
    except Exception as e:
        return datetime.datetime.now().date()

def default_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        return match_re.group(1)
    else:
        return 0

def get_md5(url):
    # str就是unicode了
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def remove_comment_value(value):
    if "评论" in value:
        return ""
    else:
        return value

def return_value(value):
    return value


class ArticleItem(scrapy.Item):

    id = scrapy.Field(
        input_processor=MapCompose(get_md5)
    )
    url = scrapy.Field()
    title = scrapy.Field()
    create_time = scrapy.Field(
        # 当值传入进来时进行相关处理
        input_processor=MapCompose(default_time)
    )
    image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    image_path = scrapy.Field()
    fav_nums = scrapy.Field(
        input_processor=MapCompose(default_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(default_nums)
    )
    praise_nums = scrapy.Field(
        input_processor=MapCompose(default_nums)
    )
    content = scrapy.Field()
    tag = scrapy.Field(
        input_processor=MapCompose(remove_comment_value),
        output_processor=Join(",")
    )






