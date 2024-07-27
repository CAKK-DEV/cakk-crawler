import pandas as pd
from Setting import setting_with_keyword
from kakao.Crawling_In_Kakao import crawling_cake_shop

search_keyword = input('검색어를 입력하세요: ')
driver = setting_with_keyword(search_keyword)
cake_shops = crawling_cake_shop(driver)

cake_shop_name = []
cake_shop_addr1 = []
cake_shop_addr2 = []

for shop_name in cake_shops.keys():
    value = cake_shops[shop_name]
    shop_addr1 = value[0]
    shop_addr2 = value[1]
    cake_shop_name.append(shop_name)
    cake_shop_addr1.append(shop_addr1)
    cake_shop_addr2.append(shop_addr2)

# 11. 데이터프레임 설정 후 csv로 저장
data = {"name": cake_shop_name, "addr1": cake_shop_addr1, "addr2": cake_shop_addr2}
df = pd.DataFrame(data)

# 12. kakaomap.csv 저장할 때 index값을 id로 설정해야 front에서 사용하기 좋음
df.to_csv("kakaomap.csv", encoding="utf-8-sig", index_label=['Id'])