from scrapy import log, signals


class FinalStats(object):
    """Outputs average speed at the end of crawling."""

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider):
        item_count = self.stats.get_value('item_scraped_count', spider=spider)
        response_count = self.stats.get_value(
            'response_received_count', spider=spider)
        start = self.stats.get_value('start_time', spider=spider)
        end = self.stats.get_value('finish_time', spider=spider)

        seconds = (end - start).seconds

        log.msg(
            ('Average processing speed: '
                '{0} items per second, {1} requests per second').format(
                    float(item_count) / seconds,
                    float(response_count) / seconds,
                ),
            spider=spider
        )
