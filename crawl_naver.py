from selenium import webdriver
from bs4 import BeautifulSoup

"""
self.driver
self.base_url
self.query
self.url
self.soup
"""


class Crawling:
    def __init__(self, base_url):
        driver = webdriver.Chrome('/Users/jiwoonwon/Downloads/chromedriver')
        driver.implicitly_wait(3)
        self.driver = driver
        self.base_url = base_url

    def set_query(self, query, page=1):
        self.query = query
        self.url = self.base_url + "&query=" + self.query
        if page > 1:
            self.url += "&kin_start=" + str(page) + "1"

    def open_driver(self):
        self.driver.get(self.url)

    def close_driver(self):
        # 포커스가 설정된 브라우저 창을 닫음
        self.driver.close()

    def quit_driver(self):
        # 모든 브라우저를 닫고 webdriver 세션을 종료
        self.driver.quit()

    def switch_window(self, isNew=False):
        window = 1 if isNew else 0
        self.driver.switch_to_window(self.driver.window_handles[window])
        self.driver.implicitly_wait(3)

    def get_questions(self):
        question_area = self.driver.find_element_by_id('elThumbnailResultArea')
        for question in question_area.find_elements_by_xpath('.//li/dl/dt/a'):
            question.click()
            # 클릭 후 액션
            self.switch_window(True)
            # 텍스트 가져오기
            self.get_sentences_from_question()
            # 브라우저 창 닫기
            self.close_driver()
            self.switch_window()

        # 다음 페이지 버튼 있으면 넘어가기
        self.is_next_exist()

    def get_sentences_from_question(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        question = soup.select_one(
            '#contents_layer_0 > div.end_content._endContents > div').text
        print(question)

    def is_next_exist(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        paging_section = soup.select_one('#main_pack > div.paging')
        next_button = paging_section.find("a", class_="next")

        if next_button is not None:
            # click button
            self.driver.find_element_by_css_selector('a.next').click()
            self.switch_window()
            self.get_questions()
