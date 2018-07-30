from crawl_naver import *
import os
import pandas as pd


def run_single_row(keyword, category):
    crawling = Crawling(keyword, category, save_file)

    print('##################', 'keyword:', keyword, '##################')
    if crawling.open_driver():
        crawling.get_questions()
    crawling.quit_driver()
    print()


DEVELOPMENT = 'DEVELOPMENT'
PRODUCTION = 'PRODUCTION'

# option 1
current_mode = PRODUCTION
# option 2
save_file = 'result.csv'

# INITIALIZE
init_koala_nlp()
if os.path.isfile(save_file):
    os.remove(save_file)

# RUN CODE
if current_mode == DEVELOPMENT:
    run_single_row("감기", "CC")
elif current_mode == PRODUCTION:
    keywords = pd.read_csv('keyword.csv')
    for _, row in keywords.iterrows():
        run_single_row(row['keyword'], row['category'])
