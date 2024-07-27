import json
import requests
import pandas as pd


def call_api(address, API_KEY):
    # 리스트설정
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=address)
    headers = {"Authorization": "KakaoAK " + API_KEY}
    result = json.loads(str(requests.get(url, headers=headers).text))
    return result


# 주소를 위도경도로 설정하는 함수
def get_lat_lng(address, API_KEY):
    result = call_api(address, API_KEY)

    if result['documents']:
        match_first = result['documents'][0]['address']
        return {"lat": str(match_first['x']), "lng": str(match_first['y'])}
    else:
        return dict()


def add_lat_with_lon(API_KEY):
    cake_shops = pd.read_csv("./kakaomap.csv", encoding="utf-8")
    lat_list = []
    lng_list = []

    for name, address in zip(cake_shops['name'], cake_shops['addr1']):
        latlng = get_lat_lng(address, API_KEY)
        if latlng:
            lat = latlng['lat']
            lng = latlng['lng']
            lat_list.append(lat)
            lng_list.append(lng)
        else:
            lat_list.append(None)
            lng_list.append(None)

    # pd.Series와 Concat을 이용하여 행을 추가하고 csv파일로 저장
    sr1 = pd.Series(lat_list, name='lat')
    sr2 = pd.Series(lng_list, name='lng')
    datas = pd.concat([cake_shops, sr1, sr2], axis=1)
    datas.to_csv('kakao_map_latLng.csv', index=False)