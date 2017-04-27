# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random


class SampleSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxies = [
            'http://158.69.73.115:3128',
            'http://144.217.253.103:3128',
            'http://88.99.149.188:31288',
            'http://198.61.232.231:80',
            'http://190.114.255.247:3128',
            'http://177.67.83.175:3128',
            'http://80.241.209.166:3128',
            'http://96.239.193.243:8080',
            'http://138.68.15.45:3128',
            'http://54.245.201.80:3128',
            'http://94.177.242.85:3128',
            'http://54.187.32.200:3128',
            'http://95.85.28.192:3128',
            'http://35.166.37.29:3128',
            'http://189.1.164.190:3128',
            'http://46.101.83.107:3128',
            'http://94.177.234.22:3128',
            'http://139.59.60.181:3128',
            'http://40.121.201.165:3128',
            'http://158.69.31.45:3128'
        ]
        request.meta['proxy'] = random.choice(proxies)
