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
from urllib.parse import quote_plus

MAX_HEADLINES = 10

# Google News RSS topic URLs (global editions)
# Topic IDs may change; verify at news.google.com if feeds stop returning results
_TOPIC_URLS = {
    'world news':   'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JXVnVMVWRDR2dKSlRpZ0FQAQ',
    'health news':  'https://news.google.com/rss/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE',
    'tech news':    'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ',
    'science news': 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp0Y1RjU0JXVnVMVWRDR2dKSlRpZ0FQAQ',
}

# Country code → (language, Google country code) for local editions
# Google News local edition URL format:
#   https://news.google.com/rss?hl={lang}-{GL}&gl={GL}&ceid={GL}:{lang}
_COUNTRY_LANG = {
    'UK': ('en', 'GB'), 'GB': ('en', 'GB'),
    'US': ('en', 'US'), 'AU': ('en', 'AU'),
    'CA': ('en', 'CA'), 'IN': ('en', 'IN'),
    'IE': ('en', 'IE'), 'NZ': ('en', 'NZ'),
    'ZA': ('en', 'ZA'), 'SG': ('en', 'SG'),
    'FR': ('fr', 'FR'), 'DE': ('de', 'DE'),
    'ES': ('es', 'ES'), 'IT': ('it', 'IT'),
    'PT': ('pt', 'PT'), 'BR': ('pt', 'BR'),
    'MX': ('es', 'MX'), 'AR': ('es', 'AR'),
    'JP': ('ja', 'JP'), 'CN': ('zh', 'CN'),
    'KR': ('ko', 'KR'), 'RU': ('ru', 'RU'),
    'PL': ('pl', 'PL'), 'NL': ('nl', 'NL'),
    'SE': ('sv', 'SE'), 'NO': ('no', 'NO'),
}


def _local_news_url(country_code):
    lang, gl = _COUNTRY_LANG.get(country_code.upper(), ('en', country_code.upper()))
    return f'https://news.google.com/rss?hl={lang}-{gl}&gl={gl}&ceid={gl}:{lang}'


class News:

    def __init__(self, country_code=None, search_queries=None):

        self.client = requests.Session()
        self.client.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
        })

        self.urls = dict(_TOPIC_URLS)

        if country_code:
            self.urls['local news'] = _local_news_url(country_code)

        for query in (search_queries or []):
            self.urls[f'{query} news'] = f'https://news.google.com/rss?q={quote_plus(query)}'

        self.seen_headlines = []

    def get_news(self, category):

        try:
            response = self.client.get(self.urls[category], timeout=10)
            response.raise_for_status()
            return self.parse_headlines(response.content)
        except Exception:
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

        # "Headline text - Source Name" → "Source Name says: Headline text."
        headline, sep, source = raw.rpartition(' - ')
        if sep and source:
            return f"{source.strip()} says: {headline.strip()}."
        return raw.strip()
