from selenium import webdriver
from bs4 import BeautifulSoup

"""
self.driver
self.base_url
self.url
self.soup
self.page_count
"""


class Crawling:
    def __init__(self, base_url):
        driver = webdriver.Chrome('/Users/jiwoonwon/Downloads/chromedriver')
        driver.implicitly_wait(2)
        self.driver = driver
        self.base_url = base_url

    def set_url(self, query, page=1):
        self.url = self.base_url + "&query=" + query
        if page > 1:
            self.url += "&kin_start=" + str(page) + "1"

    def open_driver(self):
        self.driver.get(self.url)

    def close_driver(self):
        self.driver.close()

    def set_soup(self):
        self.open_driver()
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_page_count(self):
        self.set_soup()

        result_info = self.soup.select_one(
            '#main_pack > div.kinn.section._kinBase > div > span').text.split(' / ')
        result_count = result_info[1][:-1]
        result_count = int(result_count.replace(',', ''))
        # calculate page_count
        page_count = result_count // 10 + 1

        print('pages:', page_count)
        self.page_count = page_count
