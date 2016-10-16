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

import time, random, os, pygame
from vona import Pivona
from morning_greeting import Greeting
from weather_today import Weather_today
from news import Gnews

class Alarmpi:
    def __init__(self, owner, voice_female, voice_male, auth,
                 auth_secret, WOEID, weather, news, world_news,
                 uk_news, health_news, tech_news, science_news):
        self.owner = owner
        self.pick_voice(voice_female, voice_male)
        self.auth = auth
        self.auth_secret = auth_secret
        self.WOEID = WOEID
        self.weather = weather
        self.news = news
        self.world_news = world_news
        self.uk_news = uk_news
        self.health_news = health_news
        self.tech_news = tech_news
        self.science_news = science_news

    def pick_voice(self, voice_female, voice_male):
        if voice_female != voice_male:
            if voice_female:
                if type(voice_female) == str:
                    self.voice = voice_female
                else:
                    self.voice = 'Salli'
            elif voice_male:
                if type(voice_male) == str:
                    self.voice = voice_male
                else:
                    self.voice = 'Brian'
        else:
            print 'Error, the voice has to be either male or female!'
            exit()
        
    def alarm_sound(self):
        sounds = ['wake_up.wav', 'bad-crew-pad.wav', 'dirtbag-pad.wav',
                  'guitarloop.wav', 'glamour-pad.wav', 'feel-it.wav']
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/' + random.choice(sounds))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def morning_greeting(self, vona, greet):
        vona.talk(greet.morning)
        time.sleep(4*random.random())
        vona.talk(greet.quote)
        time.sleep(4*random.random())
        vona.talk(greet.date_today)
        time.sleep(4*random.random())

    def weather_for_today(self, vona):
        weather = Weather_today(owner = self.owner, WOEID_code = self.WOEID)
        vona.talk(weather.temperature)
        time.sleep(4*random.random())
        vona.talk(weather.condition)
        time.sleep(4*random.random())
        vona.talk(weather.wind)
        time.sleep(4*random.random())
        vona.talk(weather.sun)
        time.sleep(4*random.random())

    def news_for_today(self, vona):
        gnews = Gnews()
        if self.world_news:
            try:
                world = gnews.get_world_news()
                vona.talk('And now for the top 10 news stories about the world today.')
                time.sleep(4*random.random())
                for news in world:
                    vona.talk(news)
                    time.sleep(4*random.random())
            except:
                vona.talk('Error, could not get world news.')
        if self.uk_news:
            try:
                uk = gnews.get_uk_news()
                vona.talk('Now for the top news in the UK.')
                time.sleep(4*random.random())
                for news in uk:
                    vona.talk(news)
                    time.sleep(4*random.random())
            except:
                vona.talk('Error, could not get UK news.')
        if self.health_news:
            try:
                health = gnews.get_health_news()
                vona.talk('And now for the top medical news.')
                time.sleep(4*random.random())
                for news in health:
                    vona.talk(news)
                    time.sleep(4*random.random())
            except:
                vona.talk('Error, could not get medical news.')
        if self.tech_news:
            try:
                health = gnews.get_tech_news()
                vona.talk('And now for the top tech news.')
                time.sleep(4*random.random())
                for news in health:
                    vona.talk(news)
                    time.sleep(4*random.random())
            except:
                vona.talk('Error, could not get tech news.')
        if self.science_news:
            try:
                health = gnews.get_science_news()
                vona.talk('And now for the top scientific news.')
                time.sleep(4*random.random())
                for news in health:
                    vona.talk(news)
                    time.sleep(4*random.random())
            except:
                vona.talk('Error, could not get scientific news.')

    def goodbye(self, vona, greet):
        vona.talk(greet.bye)
        time.sleep(4*random.random())

    def main(self):
        vona = Pivona(voice = self.voice, auth = self.auth,
                      auth_secret = self.auth_secret)
        greet = Greeting(owner = self.owner)
        self.morning_greeting(vona, greet)
        if self.weather:
            self.weather_for_today(vona)
        if self.news:
            self.news_for_today(vona)
        self.goodbye(vona, greet)
        
