from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('/Users/jiwoonwon/Downloads/chromedriver')
driver.implicitly_wait(3)

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
query = '담배'

url = base_url + '&query=' + query

# open chrome browser
driver.get(url)

# get result_count
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
result_info = soup.select_one(
    '#main_pack > div.kinn.section._kinBase > div > span').text.split(' / ')
result_count = result_info[1][:-1]
result_count = int(result_count.replace(',', ''))

# calculate page_count
page_count = result_count // 10 + 1
