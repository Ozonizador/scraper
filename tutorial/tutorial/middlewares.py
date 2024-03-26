import logging
from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

logger = logging.getLogger(__name__)

class SmartproxyMiddleware(HttpProxyMiddleware):
    def __init__(self, proxy_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy_url = proxy_url

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        proxy_url = settings.get('SMARTPROXY_URL')
        return cls(proxy_url)

    def process_request(self, request, spider):
        logger.debug("Processing request with SmartproxyMiddleware: %s", request)
        request.meta['proxy'] = self.proxy_url
        request.headers['Proxy-Authorization'] = self._basic_auth_header()
        return None

    def _basic_auth_header(self):
        user_pass = f"{self.proxy_url.username}:{self.proxy_url.password}"
        return f"Basic {user_pass.encode('base64').strip()}"
