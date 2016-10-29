#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
        Copyright 2016 Nicolas Pettican

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

'''

from bs4 import BeautifulSoup
import requests, json

class Gnews:
    def __init__(self):
        self.pull = requests.Session()
        self.user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
        self.update_header()
        self.world_url = 'http://news.google.com/news?output=rss'
        self.uk_url = 'http://news.google.com/news?output=rss&ned=uk'
        self.health_url = 'http://news.google.com/news?output=rss&ned=uk&topic=m'
        self.tech_url = 'http://news.google.com/news?output=rss&ned=uk&topic=t'
        self.science_url = 'http://news.google.com/news?output=rss&ned=uk&topic=snc'

    def update_header(self):
        if self.pull.headers['User-Agent']:
            if 'python' in self.pull.headers['User-Agent'].lower():
                self.pull.headers.update({'User-Agent': self.user_agent})

    def get_world_news(self):
        response = self.pull.get(self.world_url)
        return self.news_titles(response)

    def get_uk_news(self):
        response = self.pull.get(self.uk_url)
        return self.news_titles(response)

    def get_health_news(self):
        response = self.pull.get(self.health_url)
        return self.news_titles(response)

    def get_tech_news(self):
        response = self.pull.get(self.tech_url)
        return self.news_titles(response)

    def get_science_news(self):
        response = self.pull.get(self.science_url)
        return self.news_titles(response)

    def news_titles(self, response):
        news = BeautifulSoup(response.content, 'html5lib')
        news_titles_raw = news.find_all('title')
        news_titles = [news.text.encode('utf-8') for news in news_titles_raw if 'Google' not in news.text]
        return self.remove_tail(news_titles)

    def remove_tail(self, news_titles):
        news_titles_done = []
        for news in news_titles:
            head, sep, tail = news.partition(' - ')
            news_titles_done.append(head)
        return [line.replace('&', 'and') for line in news_titles_done]
