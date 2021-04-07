import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CcitizensbankofkansasItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class CcitizensbankofkansasSpider(scrapy.Spider):
	name = 'citizensbankofkansas'
	start_urls = ['https://www.citizensbankofkansas.com/About/News/']

	def parse(self, response):
		yield response.follow(response.url, self.parse_post, dont_filter=True)

	def parse_post(self, response):

		articles = response.xpath('//div[@class="item"]')
		items = []
		for article in articles:

			date = "In article"
			title = article.xpath('.//div[@class="itemTitle"]/span/text()').get()
			content = article.xpath('.//div[@class="itemArticleDescription"]//text()').getall()
			content = [p.strip() for p in content if p.strip()]
			content = re.sub(pattern, "",' '.join(content))

			item = ItemLoader(item=CcitizensbankofkansasItem(), response=response)
			item.default_output_processor = TakeFirst()

			item.add_value('title', title)
			item.add_value('link', response.url)
			item.add_value('content', content)
			item.add_value('date', date)
			items.append(item.load_item())

		return items
