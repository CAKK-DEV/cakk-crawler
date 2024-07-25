import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

# 2. Driver & BeautifulSoup
driver = webdriver.Chrome()

# 3. 크롤링할 url을 설정
org_crawling_url = "https://map.kakao.com/"
driver.get(org_crawling_url)
time.sleep(2)

# 4. 검색창 소스
element = driver.find_element(By.CLASS_NAME, 'query.tf_keyword')

# 5. send_keys를 통해 검색창 입력설정
element.send_keys("동탄 수제케이크")
time.sleep(2)

# 6. 팝업창 닫기
driver.find_element(By.CLASS_NAME, 'DimmedLayer').click()
time.sleep(2)

# 7. 검색실행
driver.find_element(By.CLASS_NAME, 'go.ico_search.btn_search.active').click()
time.sleep(2)

# 8. 장소 더보기(많은 장소들을 불러오기 위함)
driver.find_element(By.ID, 'info.search.place.more').click()
time.sleep(4)

# 9. 데이터를 넣을 공간 설정
cake_shop_addr1 = []
cake_shop_addr2 = []
cake_shop_name = []

page = 1 # 현재 크롤링하는 페이지가 전체에서 몇 번째 페이지인지
cur_page = 0 # 1 ~ 5개 패에지 중 몇 번째인지
error_cnt = 0

# 10. while문으로 page 차례대로 설정
while 1:
    try:
        cur_page += 1
        print("**", page, "**")

        driver.find_element(By.XPATH, f'//*[@id="info.search.page.no{cur_page}"]').send_keys(Keys.ENTER)

        place_lists = driver.find_elements(By.CLASS_NAME, 'PlaceItem.clickArea')

        # 장소리스트값들을 하나씩 select문으로 텍스트값을 저장 후 리스트에 추가
        for p in place_lists:
            store_html = p.get_attribute('innerHTML')
            store_info = BeautifulSoup(store_html, "html.parser")
            name = store_info.select('div.head_item.clickArea > strong > a.link_name')[0].text.strip()
            addr1 = store_info.select('div.info_item > div.addr > p')[0].text.strip()
            addr2 = store_info.select('div.info_item > div.addr > p.lot_number')[0].text.strip()
            cake_shop_name.append(name)
            cake_shop_addr1.append(addr1)
            cake_shop_addr2.append(addr2)

        # 해당 페이지 케이크 샵 리스트
        cake_shop_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')

        # 한 페이지에 장소 개수가 15개 미만이라면 해당 페이지는 마지막 페이지
        if len(cake_shop_list) < 15:
            break
        # 다음 버튼을 누를 수 없다면 마지막 페이지
        if not driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').is_enabled():
            break

        # (8) 다섯번째 페이지까지 왔다면 다음 버튼을 누르고 cur_page = 0으로 초기화
        if cur_page % 5 == 0:
            driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
            cur_page = 0

        page += 1

    except Exception as e:
        error_cnt += 1
        print(e)
        print('ERROR!' * 3)

        if error_cnt > 5:
            break



# 11. 데이터프레임 설정 후 csv로 저장
data = {"name": cake_shop_name, "addr1": cake_shop_addr1, "addr2": cake_shop_addr2}
df = pd.DataFrame(data)
print(df)

# 12. kakaomap.csv 저장할 때 index값을 id로 설정해야 front에서 사용하기 좋음
df.to_csv("kakaomap.csv", encoding="utf-8-sig", index_label=['Id'])