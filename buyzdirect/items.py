from scrapy.item import Item, Field


class AmazonItem(Item):
    response = Field()
    title = Field()
    image = Field()
    price = Field()
