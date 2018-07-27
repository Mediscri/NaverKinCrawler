from crawl_naver import *
import pandas as pd


def run_single_row(keyword, category):
    crawling = Crawling(keyword, category, save_file)

    print('##################', 'keyword:', keyword, '##################')
    if crawling.open_driver():
        crawling.get_questions()
    crawling.quit_driver()
    print()


PRODUCTION = 'PRODUCTION'
DEVELOPMENT = 'DEVELOPMENT'

# option 1
current_mode = DEVELOPMENT
# option 2
save_file = 'result.csv'

init_koala_nlp()
if current_mode == DEVELOPMENT:
    run_single_row("감기", "CC")

elif current_mode == PRODUCTION:
    keywords = pd.read_csv('keyword.csv')
    for _, row in keywords.iterrows():
        run_single_row(row['keyword'], row['category'])
