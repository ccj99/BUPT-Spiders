# encoding=utf8
# @Time    : 2019-03-10 13:36
# @Author  : Chen Changjv
# @Site    : 
# @File    : bupt_grs.py
# @Software: PyCharm
import urllib, urllib2, cookielib, time, tomd
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    start_time = '2019-03-05'
    while True:
        grs_url = 'https://grs.bupt.edu.cn/list/list.php?p=16_1_1'
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        req = urllib2.Request(grs_url)
        response = opener.open(req)
        soup = BeautifulSoup(str(response.read()), features="lxml")
        news_list = soup.find_all('ul')[2]
        max_time = start_time
        for news_item in news_list:
            if news_item != '\n' and news_item != " ":
                news_item = BeautifulSoup(str(news_item), features="lxml").find('a')
                news_time = BeautifulSoup(str(news_item), features="lxml").find('span').string[1:-1]
                print news_time
                if cmp_time(news_time, start_time):
                    news_title = '[' + news_time + ']' + news_item['title']
                    content_url = 'https://grs.bupt.edu.cn' + news_item['href']
                    print content_url
                    req_content = urllib2.Request(content_url)
                    time.sleep(2)
                    response_content = opener.open(req_content)
                    soup_content = BeautifulSoup(str(response_content.read()), features='lxml')
                    md_artical = tomd.Tomd(str(soup_content.find(id='article'))).markdown
                    send_message(news_title, md_artical)
                    time.sleep(10)
                if cmp_time(news_time, max_time):
                    max_time = news_time
        start_time = max_time
        time.sleep(3600)


def send_message(title, content, key='SCU46090Ta4bd9395b6c3028936d1352b9be7bed25c8474c4bdf1b'):
    post_data = urllib.urlencode({
        'text': title,
        'desp': content
    })
    req = urllib2.Request('https://sc.ftqq.com/' + key + '.send', data=post_data)
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    print response.read()


def cmp_time(time1, time2):
    if (int(time1[:4]) > int(time2[:4])) or (int(time1[:4]) == int(time2[:4]) and int(time1[5:7] > time2[5:7])) or \
            ((int(time1[:4]) == int(time2[:4]) and int(time1[5:7] == time2[5:7]) and int(time1[8:]) >= int(time2[8:]))):
        return True
    else:
        return False;


if __name__ == '__main__':
    main()
