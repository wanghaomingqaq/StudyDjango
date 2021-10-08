import logging
import feedparser
from urlextract import URLExtract
import requests
from lxml import html
import tweepy
from app01 import models,base
from app01.base import Pc

etree = html.etree


class Weibo():
    def parse(self, url):
        d = feedparser.parse(url)
        wei = []
        for entry in d.entries:
            weibo = {}
            extractor = URLExtract()
            text = entry.description
            urls = extractor.find_urls(text)
            weibo['title'] = entry.title
            weibo['content'] = entry.description
            href = []
            for url in urls:
                flag = ".jpg" in url
                if flag is True:
                    href.append(url)
            weibo['href'] = href
            weibo['url'] = entry.link
            wei.append(weibo)
        return wei


class Hupu:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
    }
    def hupu(self, url):
        page_text = requests.get(url, headers=self.headers).text
        tree = etree.HTML(page_text)
        li_list = tree.xpath('//*[@idx="Profile-activities"]/div[2]/div')
        hupu_list = []
        for li in li_list:
            content = li.xpath('./div[2]/div[2]/div[1]/span/text()') # //*[@id="Profile-activities"]/div[2]/div[5]/div[2]/div/div[2]/div[1]/span/text()

            #href = 'https://bbs.hupu.com' + li.xpath('./div/a/@href')[0]
            #hupu['title'] = content[0]
            #hupu['href'] = href
            #hupu['day']= content[]
            hupu_list.append(content)
        return page_text



            #hupu_list.append(content)
       # return hupu_list


class Twitter():
    consumer_key = 'TVkCxZC3oHK0hguoguqJB1xmd'
    consumer_secret = '6PsMTfcJSZPvQFy9wYoRNJHDsRuJ44Tkesh5jMrzCa8sAAfdZL'
    access_token = '767361443675017216-R0YmR2a6Q1qepakf8Kmdp6RI74DfQzS'
    access_token_secret = 'prdouOQWqMfSsOTRSj5gm6dUsTJAPv8jfcJs4A0Kt8LmJ'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    def twitter(self,username):
        api = tweepy.API(self.auth)
        public_tweets = api.user_timeline(username)
        a = []
        for tweet in public_tweets:
            content = tweet.text
            a.append(content)
        return a
class Qidian():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'

    }
    def qidian(self):
        count = 0
        models.QiDian.objects.filter().delete()
        for page in range(1, 10):
            url = 'https://www.qidian.com/rank/yuepiao?page=' + str(page)
            page_text = requests.get(url, headers=self.headers).text
            tree = etree.HTML(page_text)
            li_list = tree.xpath('//*[@id="rank-view-list"]/div/ul/li')

            for li in li_list:
                count += 1
                title = li.xpath('./div[2]/h4/a/text()')[0]
                author = li.xpath('./div[2]/p/a/text()')[0]
                type = li.xpath('./div[2]/p/a[2]/text()')[0]
                href = 'https:' + li.xpath('./div[2]/h4/a/@href')[0]
                status = li.xpath('./div[2]/p/span/text()')[0]
                models.QiDian.objects.create(rank=count, title=title, author=author, type=type, href=href,
                                             status=status)
class Cat():
    def cat(self):
        li_list = base.Pc().pc('http://www.maomaogougou.cn/tupian/maomi/keai/', '//*[@id="list"]/div[1]/div')
        img_src = []
        for li in li_list:
            img = li.xpath('./a/img/@src')[0]
            img_src.append(img)
        return img_src
class Jlu():
    def jlu(self):
        li_list = Pc().pc('https://oa.jlu.edu.cn/defaultroot/PortalInformation!jldxList.action?channelId=179577',
                          '//*[@id="itemContainer"]/div')
        for li in li_list:
            title = li.xpath('./a/text()')[0]
            author = li.xpath('./a/text()')[1]
            href = 'https://oa.jlu.edu.cn/defaultroot/' + li.xpath('./a/@href')[0]
            time = li.xpath('./span/text()')[0]
            if title in models.Jilin.objects.all():
                pass
            else:
                models.Jilin.objects.create(title=title,time=time,href=href,author=author)
