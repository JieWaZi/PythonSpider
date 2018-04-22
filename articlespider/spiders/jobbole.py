# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        # 首先获取该页面的所有文章链接
        article_nodes = response.css("#archive .post-thumb a")
        for node in article_nodes:
            article_url = node.css("::attr('href')").extract_first()
            image_url = node.css("img::attr('src')").extract_first()
            yield Request(parse.urljoin(response.url, article_url), meta={"image_url": image_url},
                          callback=self.parse_aritcle_url)
        # 请求下一页
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(next_url, callback=self.parse)

        pass

    def parse_aritcle_url(self, response):

        # article_item = ArticleItem()
        # image_url = response.meta.get("image_url", "")
        # title = response.css(".entry-header  h1::text").extract_first()
        # create_time = self.default_time(response.css('.entry-meta p::text').extract_first().replace("·", "").strip())
        # praise_nums = self.default_nums(response.css(".vote-post-up h10::text").extract_first())
        # fav_nums = self.default_nums(response.css(".bookmark-btn::text").extract_first())
        # comment_nums = self.default_nums(response.css("a[href='#article-comment'] span::text").extract_first())
        # content = response.css("div.entry").extract_first()
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tag = ",".join(tag_list)
        #
        # article_item["url"] = response.url
        # article_item["id"] = self.get_md5(response.url)
        # article_item["image_url"] = [image_url]
        # article_item["title"] = title
        # article_item["create_time"] = create_time
        # article_item["praise_nums"] = praise_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["content"] = content
        # article_item["tag"] = tag

        # 通过item loader加载item
        image_url = response.meta.get("image_url", "")  # 文章封面图
        item_loader = ArticleItemLoader(item=ArticleItem(), response=response)

        item_loader.add_value("url", response.url)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("id", response.url)
        item_loader.add_css("create_time", ".entry-meta p::text")
        item_loader.add_value("image_url", [image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tag", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        # 调用这个方法来对规则进行解析生成item对象
        article_item = item_loader.load_item()

        yield article_item
