from __future__ import absolute_import

import os.path

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ..items import AmazonItem


class AmazonSpider(BaseSpider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    process_drops = True

    def start_requests(self):
        if self.process_drops:
            if not os.path.exists('drops.txt'):
                raise RuntimeError(
                    'Please, first run spider with process_drops = False'
                )
            filename = 'drops.txt'
        else:
            filename = 'urls.txt'

        with open(filename) as f:
            for url in f:
                url = url.strip()
                yield self.make_requests_from_url(url.strip())

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        def get_text(selector):
            value = hxs.select(selector)
            if value:
                return value[0].extract()

        def find(text, context=40):
            body = response.body
            found = body.find(text)

            while found >= 0:
                print body[found - context:found + len(text) + context]
                found = body.find(text, found + 1)

        item = AmazonItem(
            response=response,  # Useful for debugging
            title=(
                get_text('//*[@id="btAsinTitle"]/text()') or
                get_text('//*[@id="title"]/text()')
            ),
            price=(
                get_text('//*[@id="actualPriceValue"]/b/text()') or
                get_text('//table[@id="price"]/tbody/tr/td[2]/span/text()') or
                get_text('//*[@class="availRed"]/text()')
            ),
            #get_text('//*[@id="price_feature_div"]/text()'),
        )
        if self.process_drops:
            # This is debug mode, so we will investigate every problem item
            import pdb
            pdb.set_trace()

        yield item
