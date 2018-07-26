from crawl_naver import Crawling
import pandas as pd

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
keywords = pd.read_csv('keyword.csv')

for idx, keyword in keywords.iterrows():
    query = keyword["Keyword"]

    # Basic
    crawling = Crawling(base_url)
    crawling.set_url(query)
    crawling.get_page_count()

    crawling.close_driver()
