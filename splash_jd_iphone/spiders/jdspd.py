# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from scrapy_splash import SplashRequest
from splash_jd_iphone.items import SplashJdIphoneItem
# from pyquery import PyQuery as pq

script = '''
function main(splash)                     
  splash:go(splash.args.url)        --打开页面
  splash:wait(2)                    --等待加载
  splash:runjs("document.getElementsByClassName('page clearfix')[0].scrollIntoView(true)") --运行js代码
  splash:wait(2)                    --等待加载
  return splash:html()              --返回页面数据
end
'''


class JdspdSpider(scrapy.Spider):
    name = 'jdspd'
    allowed_domains = ['jd.com']
    # start_urls = ['http://jd.com/']
    base_url = 'https://search.jd.com/Search?keyword='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for i in range(1, self.settings.get('MAX_PAGE') + 1):
            # for i in range(1, 2):

                url = self.base_url + quote(keyword) + '&enc=utf-8&page={}'.format(2 * i + 1)
                yield SplashRequest(url,
                                    callback=self.parse,
                                    dont_filter=True,
                                    endpoint='execute',
                                    args={'lua_source': script},
                                    cache_args=['lua_source']
                                    )

    def parse(self, response):
        # print(response.request.headers['User-Agent'])

        # for node in response.xpath('//ul[@class="gl-warp clearfix"]/li[@class="gl-item"]|//ul[@class="gl-warp clearfix"]/li[@class="gl-item gl-item-presell"]'):
        for node in response.xpath('//ul[@class="gl-warp clearfix"]/li[@class="gl-item"]'):
            item = SplashJdIphoneItem()
            # item['title'] = ''.join(node.xpath('.//div[contains(@class,"p-name p-name-type-2")]//text()').extract()).strip()
            item['title'] = node.xpath('normalize-space(.//div[contains(@class,"p-name p-name-type-2")])').extract_first()
            item['price'] = ''.join(node.xpath('.//div[contains(@class,"p-price")]//text()').extract()).strip()
            item['shop'] = ''.join(node.xpath('.//div[contains(@class,"p-shop")]//a//text()').extract()).strip()
            item['commit'] = '' .join(node.xpath('.//div[contains(@class,"p-commit")]//text()').extract()).strip()
            item['href'] = 'https://' + (''.join(node.xpath('.//div[contains(@class,"p-img")]/a/@href').extract()).strip()).split('//', 1)[1]

            yield item
            # print(item)