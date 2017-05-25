import requests
from bs4 import BeautifulSoup
import sys
import re
import os

'''
1. 전체 에피소드 리스트를 가져오기
3. 전체 에피소드의 썸네일 저장
'''
episode_list = []


class Episode:
    def __init__(self, thumbnail_url, title, rating, date):
        self._thumbnail_url = thumbnail_url
        self._title = title
        self._rating = rating
        self._date = date

    def __str__(self):
        return '{} {} {}\n{}'.format(self._title, self._rating, self._date, self._thumbnail_url)

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @property
    def title(self):
        return self._title

    @property
    def rating(self):
        return self._rating

    @property
    def date(self):
        return self._date


def get_episode_num(html):
    '''
    에피소드의 번호
    '''
    a_num = html.find_all('tr')[3].a['href']
    pre_max_num = re.search(r'&no=([0-9]*?)&', a_num)
    return int(pre_max_num.group(1))


wtn_id = '686312'
wtn_url = 'http://comic.naver.com/webtoon/list.nhn'
id_params = {'titleId':wtn_id, 'page':'1'}
target_url = requests.get(wtn_url, params=id_params)
target_html = target_url.text
soup = BeautifulSoup(target_html, "html.parser")

# 서버로부터 정상 응답을 받지못하면 프로그램 종료
if target_url.status_code != 200:
    print('Bad connection')
    sys.exit(1)

table_view = soup.find('table', 'viewList')
tr_list = table_view.find_all('tr')

i = 1
j = 1
max_num = get_episode_num(table_view)

# 페이지 순회
while i <= max_num:
    wtn_url = 'http://comic.naver.com/webtoon/list.nhn'
    id_params = {'titleId': wtn_id, 'page': j}
    target_url = requests.get(wtn_url, params = id_params)
    target_html = target_url.text
    soup = BeautifulSoup(target_html, "html.parser")
    table_view = soup.find('table', 'viewList')
    tr_list = table_view.find_all('tr')
    j += 1
    # 페이지 내의 리스트 순회
    for tr in tr_list:
        if not tr.find('td', 'title'):
            continue
        title = tr.td.a.img['title']
        link = tr.td.a.img['src']
        rating = tr.find('strong').text
        date = tr.find('td', 'num').text

        episode = Episode(
            thumbnail_url=link,
            title=title,
            rating = rating,
            date = date,
        )
        episode_list.append(episode)
        # 썸네일저장
        save = requests.get(link).content
        directory_name = wtn_id+'_images'
        # 썸네일을 저장할 폴더가 없으면 만들어준다.
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        with open(directory_name+'/image_686312_{:03}.jpg'.format(i), 'wb') as img_save:
            img_save.write(save)
        i += 1

# 리스트 순서 뒤집기
episode_list.reverse()
for item in episode_list:
    print(item)

