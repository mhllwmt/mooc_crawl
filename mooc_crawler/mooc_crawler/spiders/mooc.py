# -*- coding: utf-8 -*-
import scrapy


class MoocSpider(scrapy.Spider):
    name = 'mooc'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'DOWNLOAD_TIMEOUT': 25,
    }

    username = 'zyvenzhao@163.com'
    password = 'i8AqzObVMz2zt7KwivRK//yH/Fwc5N2vY7rBNb70D69B3oXpnRgENVleuT5APRPwNWsGji8QuxdNcLClUclwqm3hoJheubfSzuVWm/b741iTCicPal9sNWot2K5QlMTsZeY1TY+DXG0FhH/DVxuQLeSWI6DHHRmCQPOeqYXckXE='

    header = {
        "Referer": "https://www.icourse163.org",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }

    allowed_domains = ['https://www.icourse163.org/']
    start_urls = ['http://https://www.icourse163.org//']

    def start_requests(self):
        print("Start mooc crawler")
        login_url = "https://www.icourse163.org/member/login.htm"
        login_index_req = scrapy.Request(
            url=login_url,
            headers=self.header,
            callback=self.parse_login_page,
            dont_filter=True
        )
        yield login_index_req

    def parse_login_page(self, response):
        print(f"parse_login_page: url = {response.url}")
        form_post_url = "https://reg.icourse163.org/dl/l"
        yield scrapy.FormRequest(
            url=form_post_url,
            headers=self.header,
            method="POST",
            formdata={
                "un": self.username,
                "pw": self.password,
                "channel": 0,
                "d": 10,
                "l": 1,
                "pd": "imooc",
                "pkid": "cjJVGQM",
                "pwdKeyUp": 1,
                "topUTL": "https://www.icourse163.org/home.htm?userId=1027740131#/home/course",
                "domains": "",
                "rtid": "",
                "t": "",
                "tk": ""
            },
            callback=self.parse_login_res,
            dont_filter=True,
        )

    def parse_login_res(self, response):
        print(f"parse_login_res: url = {response.url}")
        personal_url = "https://www.icourse163.org/user/setting/personInfoEdit.htm#/setting"
        yield scrapy.Request(
            url=personal_url,
            headers=self.header,
            meta={
                "dont_redirect": True,
            },
            callback=self.parse_login_status,
            dont_filter=True,
        )

    def parse_login_status(self, response):
        print(f"parse_login_status: url = {response.url}")
        yield scrapy.Request(
            url="https://www.icourse163.org/category/all",
            headers=self.header,
        )

    def parse(self, response):
        print(f"parse: url = {response.url}, meta = {response.meta}")
