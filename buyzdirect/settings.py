# http://doc.scrapy.org/topics/settings.html

BOT_NAME = 'buyzdirect'

SPIDER_MODULES = ['buyzdirect.spiders']
NEWSPIDER_MODULE = 'buyzdirect.spiders'

ITEM_PIPELINES = [
    'buyzdirect.pipeline.ValidateFields',
    'buyzdirect.pipeline.SaveToDB',
]

CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = CONCURRENT_REQUESTS
HTTPCACHE_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    # we'll turn off standart user agent middleware
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,

    'scrapy_proxynova.middleware.HttpProxyMiddleware': 755,
    'scrapy_useragents.middleware.UserAgentsMiddleware': 400,
}

PROXY_SERVER_COUNTRY = 'us'
PROXY_SERVER_LIMIT = 100

EXTENSIONS = {
    'buyzdirect.extensions.FinalStats': 500,
}
