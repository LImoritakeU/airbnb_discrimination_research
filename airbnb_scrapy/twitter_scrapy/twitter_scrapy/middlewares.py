# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from time import sleep
from random import randint

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=None):
        self.timeout = timeout
        self.driver = webdriver.Firefox(service_args)

    def __del__(self):
        self.driver.quit

    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
            for x in scroll_down(self.driver):
                sleep(randint(2, 4))

            return HtmlResponse(
                url=request.url, body=self.driver.page_source,
                request=request, encoding='utf-8', status=200
            )
        except TimeoutException:
            return HtmlResponse(
                url=request.url, status=500, request=request
            )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
            service_args=crawler.settings.get('SELENIUM_DRIVER_SERVICE_ARGS')
        )


def scroll_down(driver):
    """ Scroll down to bottom, then calculate new scroll height and compare
    with last scroll height
    """
    js_return_scrollHeight = "return document.body.scrollHeight"
    js_scrollTo_buttom = "window.scrollTo(0, (document.body.scrollHeight));"

    last_height = driver.execute_script(js_return_scrollHeight)
    new_height = 0
    while last_height != new_height:
        last_height = new_height
        driver.execute_script(js_scrollTo_buttom)
        new_height = driver.execute_script(js_return_scrollHeight)
        yield

    else:
        print("No more content")


class TwitterScrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TwitterScrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



