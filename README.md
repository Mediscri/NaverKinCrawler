# 네이버 지식인 전문가 답변 크롤러

### Purpose

- 병원 데이터 확보 전 딥러닝 모델 학습을 위한 임시 데이터 확보

### Dataset

- 사전에 분류한 카테고리에 따라 검색된 결과물을 문장별로 저장

  ```
  data = [
      {
          keyword: '급성복통',
          category: 'CC',
          sentence: '갑자기 배가 너무 아팠어요'
      },
      ...
  ]
  ```

### Dependency

- Selenium
- Kkma
- BeautifulSoup
- Pandas

### Steps

1.  install chromedriver on root folder [download](https://chromedriver.storage.googleapis.com/index.html?path=2.40/)
2.  install all dependencies
3.  run main.py
