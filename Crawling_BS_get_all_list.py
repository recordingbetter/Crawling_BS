import requests
from bs4 import BeautifulSoup
import sys
import re

'''
1. 전체 에피소드 리스트를 가져오기
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


def get_episode_num(table_view):
    '''
    에피소드의 번호를 int로 반환한다.
    :param table_view: 
    :return: 
    '''
    a_num = table_view.find_all('tr')[3].a['href']
    pre_max_num = re.search(r'&no=([0-9]*?)&', a_num)
    return int(pre_max_num.group(1))


wtn_url = 'http://comic.naver.com/webtoon/list.nhn'
id_params = {'titleId':'686312', 'page':'1'}

target_url = requests.get(wtn_url, params=id_params)
target_html = target_url.text
# print(target_html)
# print(target_url.status_code)
soup = BeautifulSoup(target_html, "html.parser")

# 서버로부터 정상 응답을 받지못하면 프로그램 종료
if target_url.status_code != 200:
    print('Bad connection')
    sys.exit(1)




# 리스트 부분을 분리
table_view = soup.find('table', 'viewList')
# print(table_view)
tr_list = table_view.find_all('tr')
# print(tr_list)


i = 1
j = 1
max_num = get_episode_num(table_view)

while i <= max_num:
    wtn_url = 'http://comic.naver.com/webtoon/list.nhn'
    id_params = {'titleId': '686312', 'page': j}
    target_url = requests.get(wtn_url, params = id_params)
    target_html = target_url.text
    soup = BeautifulSoup(target_html, "html.parser")
    table_view = soup.find('table', 'viewList')
    tr_list = table_view.find_all('tr')
    j += 1

    for tr in tr_list:
        if not tr.find('td', 'title'):
            continue
        # print(tr)
        title = tr.td.a.img['title']
        # print(title)
        link = tr.td.a.img['src']
        # print(link)
        rating = tr.find('strong').text
        # print(rating)
        date = tr.find('td', 'num').text
        # print(date)

        episode = Episode(
            thumbnail_url=link,
            title=title,
            rating = rating,
            date = date,
        )
        # print(episode)
        episode_list.append(episode)
        i += 1

episode_list.reverse()
for item in episode_list:
    print(item)
# print(type(episode_list))


