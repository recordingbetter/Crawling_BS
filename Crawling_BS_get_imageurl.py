import requests
from bs4 import BeautifulSoup
import sys

'''
2. 에피소드 번호를 입력하면(no) 내부의 웹툰 이미지 주소를 가져오기 (여러장의 이미지로 분할되어있음)

'''

wtn_num = input('에피소드 번호를 입력하세요. :'.format())



wtn_detail_url = 'http://comic.naver.com/webtoon/detail.nhn'
id_params = {'titleId':'686312', 'no':wtn_num}

target_url = requests.get(wtn_detail_url, params=id_params)
target_html = target_url.text

soup = BeautifulSoup(target_html, "html.parser")

# 서버로부터 정상 응답을 받지못하면 프로그램 종료
if target_url.status_code != 200:
    print('Bad connection')
    sys.exit(1)

# wt_viewer 부분을 분리
wt_viewer = soup.find('div', 'wt_viewer')
# print(wt_viewer)
img_list = wt_viewer.find_all('img')
# print(img_list)

# 찾아진 이미지 갯수만큼 반복
img_link_list = []
for idx, img in enumerate(img_list):
    # print(img)
    img_link = img['src']
    print(idx, img_link)
    img_link_list.append(img_link)


