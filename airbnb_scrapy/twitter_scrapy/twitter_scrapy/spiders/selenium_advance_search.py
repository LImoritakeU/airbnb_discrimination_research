# -*- coding: utf-8 -*-
from time import sleep

import scrapy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions as EC

FIREFOX_DRIVER = '/home/shihhao/testing/geckodriver'


# Search Form
ands_xpath = "//input[@name='ands']"
phrase_xpath = "//input[@name='phrase']"
ors_xpath = "//input[@name='ors']"
nots_xpath = "//input[@name='nots']"
tag_xpath = "//input[@name='tag']"
from_xpath = "//input[@name='from']"
to_xpath = "//input[@name='to']"
ref_xpath = "//input[@name='ref']"
near_xpath = "//input[@name='near']"
button_xpath = "//div[@class='main']//form//button[@type='submit']"
lang_xpath = "//select[@id='lang']"
# time format yyyy-mm-dd
since_xpath = "//input[@id='since']"
until_xpath = "//input[@id='until']"

form_submit = {
    ands_xpath: None,
    phrase_xpath: None,
    ors_xpath: None,
    nots_xpath: None,
    tag_xpath: None,
    from_xpath: None,
    to_xpath: None,
    ref_xpath: None,
    near_xpath: None,
    lang_xpath: "en",
    since_xpath: None,
    until_xpath: None,
}


class SeleniumAdvanceSearchSpider(scrapy.Spider):
    name = 'selenium_advance_search'
    allowed_domains = ['twitter.com/search-advanced']
    start_urls = ['https://twitter.com/search-advanced/']
    driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER)



    def parse(self, response):
        pass

    def advance_search_by_selenium(self):
        self.driver.get(self.start_urls)

        for key, value in form_submit.items():
            self.driver.find_element_by_xpath(key).send_keys(value)

        button = self.driver.find_element_by_xpath(button_xpath)
        action_chain = ActionChains(self.driver)
        action_chain.double_click(button).perform()

        ui.WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "SearchNavigation"))
        )

        # quality filter off
        url = self.driver.current_url + '&qf=off'
        self.driver.get(url)
        ui.WebDriverWait(self.driver, 10, 0.5).until(
            (lambda driver: '&qf=off' in driver.current_url)
        )
