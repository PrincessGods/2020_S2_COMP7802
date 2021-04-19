from scrapy.spiders import Spider
from scrapy.selector import Selector
from crawler.items import PentestItem
from scrapy.http import Request
from scrapy import FormRequest
import re

class MySpider(Spider):
	# Usage: scrapy crawl crawler --nolog -t json -O temp/spider.json

	name = "crawler"

	def __init__(self, *args, **kwargs):
		super(MySpider, self).__init__(*args, **kwargs)
		self.start_urls = [kwargs.get('start_urls')]
		self.allowed_domains = [kwargs.get('allowed_domains')]

		if self.start_urls[0] == None:
			print("\n[Info] Please enter the start URLs of crawling. (URLs split be ' - ')")
			print("[Info] It is recommended to start with the login page if you would like to login first!")
			print("[Info] Example: http://www.google.com - http://www.packtpub.com")
			self.start_urls = input().split(" - ")

		if self.allowed_domains[0] == None:
			print("\n[Info] Please enter the allowed domains of crawling. (Domains split be ' - ')")
			print("[Info] Example: localhost - WebGoat.net - packtpub.com")
			self.allowed_domains = input().split(" - ")

	def parse(self, response):
		sele = Selector(response)
		forms = sele.xpath('//form').extract()

		for form in forms:
			formInfo = PentestItem()
			method = None
			action = None
			name = list()
			data = form.split(" ")

			for f in data:
				if "method=" in f:
					method = str(f.split(">")[0].split("=")[1])[1:-1]
				if "action=" in f:
					action = str(f.split(">")[0].split("=")[1])[1:-1]
				if "name=" in f:
					name.append(str(f.split(">")[0].split("=")[1])[1:-1])

			formInfo["form"] = action
			formInfo["method"] = method
			formInfo["name"] = name
			formInfo["location_url"] = response.url

			yield formInfo

		visited_links = []
		links = sele.xpath('//a/@href').extract()
		link_validator = re.compile(
			"^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

		for link in links:
			if link_validator.match(link) and not link in visited_links:
				visited_links.append(link)
				yield Request(link, self.parse)
			else:
				full_url = response.urljoin(link)
				visited_links.append(full_url)
				yield Request(full_url, self.parse)
