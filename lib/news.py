#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ___        AlarmPi V 1.1.1 by nickpettican            ___
# ___   Your smart alarm clock for the Raspberry Pi     ___

# ___        Copyright 2017 Nicolas Pettican            ___

# ___    This software is licensed under the Apache 2   ___
# ___    license. You may not use this file except in   ___
# ___    compliance with the License.                   ___
# ___    You may obtain a copy of the License at        ___

# ___    http://www.apache.org/licenses/LICENSE-2.0     ___

# ___    Unless required by applicable law or agreed    ___
# ___    to in writing, software distributed under      ___
# ___    the License is distributed on an "AS IS"       ___
# ___    BASIS, WITHOUT WARRANTIES OR CONDITIONS OF     ___
# ___    ANY KIND, either express or implied. See the   ___
# ___    License for the specific language governing    ___
# ___    permissions and limitations under the License. ___

import requests
import xml.etree.ElementTree as ET

MAX_HEADLINES = 10


class News:

    def __init__(self, country_code):

        self.client = requests.Session()
        self.client.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        })

        self.urls = {
            'world news':        'https://news.google.com/rss',
            'country news':      f'https://news.google.com/rss?ned={country_code}',
            'medical news':      f'https://news.google.com/rss?ned={country_code}&topic=m',
            'technological news': f'https://news.google.com/rss?ned={country_code}&topic=t',
            'scientific news':   f'https://news.google.com/rss?ned={country_code}&topic=snc',
        }
        self.seen_headlines = []

    def get_news(self, category):

        try:
            response = self.client.get(self.urls[category])
            return self.parse_headlines(response.content)
        except:
            return []

    def parse_headlines(self, content):

        root   = ET.fromstring(content)
        titles = root.findall('.//item/title')
        return [
            self.format_headline(item.text)
            for item in titles[:MAX_HEADLINES]
            if item.text and 'Google' not in item.text
        ]

    def format_headline(self, raw):

        # "Headline text - Source Name" -> "Source Name says: Headline text."
        headline, sep, source = raw.rpartition(' - ')
        if sep and source:
            return f"{source.strip()} says: {headline.strip()}."
        return raw.strip()
