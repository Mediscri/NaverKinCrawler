from crawl_naver import Crawling
import pandas as pd


def run_single_row(keyword, category):
    crawling = Crawling(keyword, category, save_file)

    print('##################', 'keyword:', keyword, '##################')
    if crawling.open_driver():
        crawling.get_questions()
    crawling.quit_driver()
    print()


MODE = {'PRODUCTION': 'PRODUCTION', 'DEVELOPMENT': 'DEVELOPMENT'}

# option 1
current_mode = MODE['PRODUCTION']
# option 2
save_file = 'result.csv'

if current_mode == MODE['DEVELOPMENT']:
    run_single_row("감기", "CC")

elif current_mode == MODE['PRODUCTION']:
    keywords = pd.read_csv('keyword.csv')
    for _, row in keywords.iterrows():
        run_single_row(row['keyword'], row['category'])
