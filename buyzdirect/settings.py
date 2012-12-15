# http://doc.scrapy.org/topics/settings.html

BOT_NAME = 'buyzdirect'

SPIDER_MODULES = ['buyzdirect.spiders']
NEWSPIDER_MODULE = 'buyzdirect.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.83 Safari/535.11'

ITEM_PIPELINES = [
    'buyzdirect.pipeline.ValidateFields',
    'buyzdirect.pipeline.SaveToDB',
]

CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = CONCURRENT_REQUESTS
HTTPCACHE_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy_proxynova.middleware.HttpProxyMiddleware': 543,
}

PROXY_SERVER_COUNTRY = 'us'
PROXY_SERVER_LIMIT = 100

EXTENSIONS = {
    'buyzdirect.extensions.FinalStats': 500,
}
