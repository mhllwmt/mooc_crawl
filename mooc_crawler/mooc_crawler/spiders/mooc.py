# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


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

    allowed_domains = ['https://www.icourse163.org']
    start_urls = ['https://www.icourse163.org']

    def __init__(self, category=None, username=None, password=None, *args, **kwargs):
        super(MoocSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Firefox(firefox_options=Options().add_argument('--headless'))
        self.start_urls = [self.start_urls[0] + f'/category/{category}']
        self.username = username
        self.password = password

    # do login
    def start_requests(self):
        print("Start mooc crawler")
        login_url = "https://www.icourse163.org/member/login.htm#/webLoginIndex"
        self.driver.get(login_url)

        try:
            self.driver.find_element_by_css_selector("ul.ux-tabs-underline_hd li:nth-of-type(2)").click()
            print("Mail login method selected")
        except NoSuchElementException:
            print("Cannot select mail login method")
        time.sleep(3)

        iframe = self.driver.find_element_by_css_selector("div#j-ursContainer-0 iframe")
        self.driver.switch_to.frame(iframe)

        try:
            username = self.driver.find_element_by_css_selector("div.u-input input.dlemail")
            password = self.driver.find_element_by_css_selector("input.dlpwd")
            login_btn = self.driver.find_element_by_css_selector("div.loginbox a#dologin")

            username.send_keys(self.username)
            password.send_keys(self.password)
            login_btn.click()
        except NoSuchElementException:
            print("login failed")

        if self.driver.current_url == login_url:
            yield scrapy.Request(login_url)

        yield scrapy.Request("https://www.icourse163.org/category/computer")

    def parse(self, response):
        print(f"parse: url = {response.url}, meta = {response.meta}")
