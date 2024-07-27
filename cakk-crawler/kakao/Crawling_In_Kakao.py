from bs4 import BeautifulSoup
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def crawling_cake_shop(driver):
    # 데이터를 넣을 공간 설정
    cake_shops = dict()

    page = 1  # 현재 크롤링하는 페이지가 전체에서 몇 번째 페이지인지
    cur_page = 0  # 1 ~ 5개 패에지 중 몇 번째인지
    error_cnt = 0

    # while문으로 page 차례대로 설정
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
                addr1 = store_info.select('div.info_item > div.addr > p')[0].text.splitlines()[1].strip()
                addr2 = store_info.select('div.info_item > div.addr > p.lot_number')[0].text.strip()
                addr_list = [addr1, addr2]
                cake_shops[name] = addr_list

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
    return cake_shops
