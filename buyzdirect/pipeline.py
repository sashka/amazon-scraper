from scrapy.exceptions import DropItem


class SaveToDB(object):
    def process_item(self, item, spider):
        """TODO: write item to db."""
        return item


class ValidateFields(object):
    def __init__(self):
        self.drops = None

    def process_item(self, item, spider):
        for key, value in item.items():
            if value is None:
                url = item['response'].url

                if not spider.process_drops:
                    # if drops are not processed, then
                    # write them to a file

                    if self.drops is None:
                        self.drops = open('drops.txt', 'w')
                    self.drops.write(url + '\n')

                raise DropItem(
                    'Missing fields for {0}'.format(url)
                )

        return item
