#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___        AlarmPi V 1.1.1 by nickpettican            ___
# ___   Your smart alarm clock for the Raspberry Pi     ___

# ___        Copyright 2017 Nicolas Pettican            ___

# ___   This software is licensed under the Apache 2    ___
# ___   license. You may not use this file except in    ___
# ___   compliance with the License.                    ___
# ___   You may obtain a copy of the License at         ___

# ___    http://www.apache.org/licenses/LICENSE-2.0     ___

# ___    Unless required by applicable law or agreed    ___
# ___    to in writing, software distributed under      ___
# ___    the License is distributed on an "AS IS"       ___
# ___    BASIS, WITHOUT WARRANTIES OR CONDITIONS OF     ___
# ___    ANY KIND, either express or implied. See the   ___
# ___    License for the specific language governing    ___
# ___    permissions and limitations under the License. ___

from bs4 import BeautifulSoup
import requests, json

class Gnews:

    # --- obtains news from Google News ---

    def __init__(self, country_code):
        
        self.start_requests()

        self.country_code = country_code
        self.urls = {   'world news': 'http://news.google.com/news?output=rss',
                        'country news': 'http://news.google.com/news?output=rss&ned=%s' %(country_code), 
                        'medical news': 'http://news.google.com/news?output=rss&ned=%s&topic=m' %(country_code), 
                        'technological news': 'http://news.google.com/news?output=rss&ned=%s&topic=t' %(country_code), 
                        'scientific news': 'http://news.google.com/news?output=rss&ned=%s&topic=snc' %(country_code) }
        self.all_news = ['to avoid repeating news']

    def start_requests(self):

        # --- start requests session as 'pull' ---

        self.pull = requests.Session()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        self.pull.headers.update({'User-Agent': user_agent})

    def get_news(self, choice):

        # --- requests news from Google News ---

        try:
            response = self.pull.get(self.urls[choice])
            return self.news_titles(response)
        except:
            return False

    def news_titles(self, response):

        # --- finds just the news titles ---

        news = BeautifulSoup(response.content, 'lxml')
        news_titles_raw = news.find_all('title')
        news_titles = [news.text.encode('utf-8') for news in news_titles_raw if 'Google' not in news.text]
        # ouch, can't get any news on Google itself - need to fix this
        return self.remove_tail(news_titles)

    def remove_tail(self, news_titles):

        # --- removes 'tail' from titles ---

        news_titles_done = []
        for news in news_titles:
            head, sep, tail = news.partition(' - ')
            news_titles_done.append(head)
        return [line.replace('&', 'and') for line in news_titles_done]
