from __future__ import absolute_import

import os.path
import json
import w3lib.html

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ..items import AmazonItem


class AmazonSpider(BaseSpider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    process_drops = False

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

        def get_text(selector, default=None):
            value = hxs.select(selector)
            if value:
                return value[0].extract()
            return default

        def get_json(selector, default=None):
            value = get_text(selector)
            if value:
                return json.loads(value)
            return default

        def find(text, context=40):
            body = response.body
            found = body.find(text)

            while found >= 0:
                print body[found - context:found + len(text) + context]
                found = body.find(text, found + 1)

        item_data = get_json('//*[@id="fbt_item_data"]/text()')
        if item_data:
            for data in item_data['itemData']:
                if data.get('priceBreaksMAP') is not None:
                    buying_price = data['buyingPrice']
                    break
        else:
            buying_price = None

        description = u'<br>'.join(
            hxs.select('//div[@class="productDescriptionWrapper"]').extract()
        )
        description = w3lib.html.remove_tags(
            description,
            keep=('br', 'ul', 'ol', 'li', 'table', 'tr', 'td')
        )

        item = AmazonItem(
            response=response,  # Useful for debugging
            title=(
                get_text('//*[@id="btAsinTitle"]/text()') or
                get_text('//*[@id="title"]/text()')
            ),
            price=(
                get_text('//*[@id="actualPriceValue"]/b/text()') or
                get_text('//table[@id="price"]/tbody/tr/td[2]/span/text()') or
                get_text('//*[@class="availRed"]/text()') or
                buying_price
            ),
            image=(
                get_text('//img[@id="main-image"]/@src') or
                get_text('//*[@id="prodImageCell"]//img/@src')
            ),
            description=description,
            in_stock=None,
        )
        avail_green = hxs.select('//*[@class="availGreen"]')
        availability = get_text('//*[@id="availability"]/div/text()', '')

        if avail_green:
            if 'Available from' in ''.join(avail_green.extract()):
                item['in_stock'] = False
            else:
                item['in_stock'] = True
        elif hxs.select('//*[@class="availRed"]') or \
                hxs.select('//*[@class="availOrange"]'):
            item['in_stock'] = False
        elif 'In Stock' in availability or 'left in stock' in availability:
            item['in_stock'] = True

        if not item['in_stock'] and item['price'] is None:
            # we aren't interested in price of items that out os stock, right?
            item['price'] = 0

        if self.process_drops:
            # This is debug mode, so we will investigate every problem item
            import pdb
            pdb.set_trace()

        yield item
