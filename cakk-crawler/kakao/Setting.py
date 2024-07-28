import time
from selenium.webdriver.common.by import By
from selenium import webdriver


def setting_with_keyword(keyword):
    # Driver & BeautifulSoup
    driver = webdriver.Chrome()

    # 크롤링할 url을 설정
    org_crawling_url = "https://map.kakao.com/"
    driver.get(org_crawling_url)
    time.sleep(2)

    # 검색창 소스
    element = driver.find_element(By.CLASS_NAME, 'query.tf_keyword')

    # send_keys를 통해 검색창 입력설정
    element.send_keys(keyword)
    time.sleep(2)

    # 팝업창 닫기
    driver.find_element(By.CLASS_NAME, 'DimmedLayer').click()
    time.sleep(2)

    # 검색실행
    driver.find_element(By.CLASS_NAME, 'go.ico_search.btn_search.active').click()
    time.sleep(2)

    # 장소 더보기(많은 장소들을 불러오기 위함)
    driver.find_element(By.ID, 'info.search.place.more').click()
    time.sleep(2)

    return driver
