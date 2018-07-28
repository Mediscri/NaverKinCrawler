import pandas as pd
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from koalanlp import *


'''
base_url = 'https://search.naver.com/search.naver'
sm = 'tab_pge'
ie = 'utf8'
where: string => 지식in: 'kin'
answer: int => 의사: 2
kin_sort: int => default: 0
kin_display: int => default: 10
kin_start: int
query: string
'''

base_url = 'https://search.naver.com/search.naver?where=kin&kin_sort=0&kin_display=10&answer=2&ie=utf8&sm=tab_pge'


def init_koala_nlp():
    initialize(packages=[API.HANNANUM])


class Crawling:
    def __init__(self, query, category, save_file):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        # Headless 탐지 막기
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.driver = webdriver.Chrome(
            './chromedriver', chrome_options=options)

        self.splitter = SentenceSplitter(splitter_type=API.HANNANUM)

        self.question_bundle_id = 'elThumbnailResultArea'
        self.single_question_css = '#contents_layer_0 > div.end_content._endContents > div'
        self.page = 1

        self.query = query
        self.category = category
        self.url = base_url + "&query=" + self.query

        if os.path.isfile(save_file):
            os.remove(save_file)
        self.save_file = save_file

    def set_soup(self):
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')

    def open_driver(self):
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, self.question_bundle_id)))
            return True
        except TimeoutException as e:
            print("There's no result on this keyword")
            return False

    def close_driver(self):
        # 포커스가 설정된 브라우저 창을 닫음
        self.driver.close()

    def quit_driver(self):
        # 모든 브라우저를 닫고 webdriver 세션을 종료
        self.driver.quit()

    def get_questions(self):
        print("current page:", self.page)
        question_bundle = self.driver.find_element_by_id(
            self.question_bundle_id)
        for question in question_bundle.find_elements_by_xpath('.//li/dl/dt/a'):
            question.click()
            # 포커스 화면 전환
            self.switch_window(True)
            # 텍스트 가져와서 저장하기
            sentences = self.get_sentences_from_question()
            self.write_sentences_to_csv(sentences)
            # 브라우저 창 닫기
            self.close_driver()
            self.switch_window()

        # 다음 페이지 버튼 있으면 넘어가기
        self.click_next_page()

    def switch_window(self, isNew=False):
        window = 1 if isNew else 0
        self.driver.switch_to_window(self.driver.window_handles[window])
        if isNew:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.single_question_css)))
        else:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, self.question_bundle_id)))

    def get_sentences_from_question(self):
        self.set_soup()
        question = self.soup.select_one(self.single_question_css).text
        paragraph = question.strip()
        # 반복되는 특수문자 처리
        paragraph = re.sub(r'([\s.,?!~=-]){2,}', r'\1', paragraph)
        # 불필요한 문자 제거
        paragraph = re.sub(
            '[^가-힣0-9\s.,!?~=-]+|[안녕|도와|감사][가-힣]+[.]*', '', paragraph)
        # 문장 end-point rule-based로 표시
        paragraph = re.sub(
            r'([가-힣]*[가구까나내네도대돼데만서세아어이파해])[.]\s*', r'\1 ', paragraph)
        paragraph = re.sub(
            r'([가-힣]*[가구까나내네도대돼데만서세아어이파해]요|[가-힣]+니다)[~.?!]*\s*', r'\1. ', paragraph)
        # 문장 분리
        sentences = self.splitter.sentences(paragraph)

        re_sentences = []  # 정제된 문장
        for text in sentences:
            # 앞뒤 공백 제거
            re_text = text.strip()
            # 정규화 > . ? 앞의 공백 제거
            re_text = re.sub(r'\s*([.?])$', r'\1', re_text)
            re_sentences.append(re_text)
        return re_sentences

    def write_sentences_to_csv(self, sentences):
        sentence_len = len(sentences)
        raw_data = {'keyword': [self.query for _ in range(sentence_len)],
                    'category': [self.category for _ in range(sentence_len)],
                    'sentence': sentences}
        data = pd.DataFrame(raw_data)

        if not os.path.isfile(self.save_file):
            data.to_csv(self.save_file, header='column_names', index=False)
        else:
            data.to_csv(self.save_file, mode='a', header=False, index=False)

    def click_next_page(self):
        self.set_soup()
        paging_section = self.soup.select_one('#main_pack > div.paging')
        next_button = paging_section.find("a", class_="next")

        if next_button is not None:
            self.page += 1
            # click button
            self.driver.find_element_by_css_selector('a.next').click()
            self.switch_window()
            self.get_questions()
