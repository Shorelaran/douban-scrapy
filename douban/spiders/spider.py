# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from douban.items import DoubanItem


class Douban(CrawlSpider):
	name = 'douban'
	start_urls = ['https://movie.douban.com/top250']

	def parse(self, response):
		item = DoubanItem()
		movies = response.xpath('//div[@class="info"]')
		for eachmovie in movies:
			all_title =eachmovie.xpath('div[@class="hd"]/a/span/text()').extract()
			title = ''
			for each in all_title:
				title += str(each).strip().replace('\xa0', '')
			infos = eachmovie.xpath('div[@class="bd"]/p/text()').extract()
			info = []
			for each in infos:
				info.append(str(each).replace('\xa0', ' ').replace('\n', '').strip())
			star = eachmovie.xpath('div[@class="bd"]/div[@class="star"]/span/text()').extract()
			quote = eachmovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
			#quote可能为空
			if quote:
				quote = quote[0]
			else:
				quote = ''
			item['title'] = title
			item['info'] = ';'.join(info)
			item['star'] = star[0]
			item['content'] = star[1]
			item['quote'] = quote
			yield item  #提交生成csv文件

		nextlink = response.xpath('//span[@class="next"]/link/@href').extract()
		#判断最后一页
		if nextlink:
			nextlink = nextlink[0]
			#递归爬取下一页
			yield scrapy.Request(self.start_urls[0] + nextlink, callback= self.parse)




