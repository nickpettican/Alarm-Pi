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

import requests, time, json, random, itertools

class Weather_today:
    def __init__(self, owner, WOEID_code):
        self.owner = owner
        self.pull = requests.Session()
        self.user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
        self.update_header()
        yahoo_weather = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast'
        WOEID = '%20where%20woeid%3D' + WOEID_code
        celcius = '%20and%20u%3D%27C%27'
        format_json = '&format=json'
        self.weather_url = yahoo_weather + WOEID + celcius + format_json
        self.get_weather_info(self.weather_url)
        self.get_temperature(self.today_info)
        self.get_condition(self.today_info)
        self.get_wind(self.today_info)
        self.get_sun_rise_set(self.today_info)

    def update_header(self):
        if self.pull.headers['User-Agent']:
            if 'python' in self.pull.headers['User-Agent'].lower():
                self.pull.headers.update({'User-Agent': self.user_agent})

    def get_weather_info(self, weather_url):
        weather_info = self.pull.get(weather_url)
        response = weather_info.json()
        today_info = {}
        today_info['current_temp'] = response['query']['results']['channel']['item']['condition']['temp']
        today_info['current_low'] = response['query']['results']['channel']['item']['forecast'][0]['low']
        today_info['current_high'] = response['query']['results']['channel']['item']['forecast'][0]['high']
        today_info['conditions'] = response['query']['results']['channel']['item']['condition']['text']
        today_info['forecast_conditions'] = response['query']['results']['channel']['item']['forecast'][0]['text']
        today_info['wind'] = response['query']['results']['channel']['wind']['speed']
        today_info['sunrise'] = response['query']['results']['channel']['astronomy']['sunrise']
        today_info['sunset'] = response['query']['results']['channel']['astronomy']['sunset']
        self.today_info = today_info

    def get_temperature(self, info):
        temp = int(info['current_temp'])
        high = int(info['current_high'])
        low = int(info['current_low'])
        if temp < 0 and high < 0:
            say = list(itertools.product(
                    ["It's absolutely freezing today! The temperature is %s degrees, and the highest will only be %s." %(temp, high),
                     "Everything's frozen outside! It's %s degrees with a high of %s! Are you serious?" %(temp, high),
                     "What? How is it so cold? Sorry %s. It's %s degrees and it will be a very cold day..." %(self.owner, temp)],
                    ["Make sure you wear something warm today.", "Put on your warmest clothes.",
                     "Don't catch a cold. Remember that I can't take care of you."],
                    ["Time for a nice warm beverage. Wouldn't you say?", "And take a scarf!", "Don't forget your scarf!"]))
            self.temperature = ' '.join(random.choice(say))

        elif temp < 0 and high > 0:
            say = list(itertools.product(
                    ["It's freezing at the moment, at %s degrees. But it will reach a high of %s later." %(temp, high),
                     "Everything is frozen! It's %s degrees. But it should get better later, with a high of %s." %(temp, high),
                     "It's so cold outside, it's %s degrees." %(temp)],
                    ["Make sure you wear warm clothes today.", "Put on warm clothes and wear a warm jacket.",
                     "Don't catch a cold. Remember that I can't take care of you."],
                    ["Time for a nice warm beverage. Wouldn't you say?", "And don't forget your scarf!"]))
            self.temperature = ' '.join(random.choice(say))

        elif 0 <= temp < 4:
            say = list(itertools.product(
                    ["It's very cold outside. The temperature is %s degrees, reaching a high of %s." %(temp, high),
                     "It's pretty could outside. %s degrees with a high of %s and a low of %s." %(temp, high, low),
                     "The temperature right now is %s degrees. It's really cold outside, but it will reach a high of %s later." %(temp, high)],
                    ["Make sure you put on warm clothes.", "Don't underestimate the cold. Wear something warm.",
                     "Put on some warm clothes and a warm scarf."],
                    ["Have a nice and warm beverage. God, I wish I could drink...", "Take care of yourself. OK?",
                     "Time for a nice warm beverage. Wouldn't you say?"]))
            self.temperature = ' '.join(random.choice(say))

        elif 4 <= temp < 8:
            say = list(itertools.product(
                    ["It's a bit %s at the moment. The temperature is %s with a high of %s and a low of %s." %(random.choice(['chilly', 'cold']), temp, high, low),
                     "The temperature right now is %s degrees. It's cold, but it will reach a high of %s later" %(temp, high)],
                    ["Wear something warm. OK?", "As mum says. wear something warm.", "Don't go catching a cold now."],
                    ["Have a nice and warm beverage. God, I wish I could drink...", "Take care of yourself.",
                     "Time for a nice warm beverage. Wouldn't you say?"]))
            self.temperature = ' '.join(random.choice(say))

        elif 8 <= temp < 12:
            say = list(itertools.product(
                    ["It's a bit nippy but not too cold. The temperature is now %s degrees and will reach a high of %s later." %(temp, high),
                     "The temperature right now is %s degrees. It's a bit cold, but fortunately it will reach a high of %s later." %(temp, high)],
                    ["A jumper and a jacket should suffice for today.", "Just wear a sweater and a jacket and you should be fine."]))
            self.temperature = ' '.join(random.choice(say))

        elif 12 <= temp < 16:
            say = list(itertools.product(
                    ["It's not too cold today. It's %s degrees now, and it will reach a high of %s." %(temp, high),
                     "Not too bad today. It's currently %s degrees with a high of %s and a low of %s." %(temp, high, low)],
                    ["A couple of layers of clothes should be fine. But take a thin jacket just in case.",
                     "Just wear a sweater and maybe a thin jacket just to make sure."]))
            self.temperature = ' '.join(random.choice(say))

        elif 16 <= temp <= 20:
            say = list(itertools.product(
                    ["Looks like a nice temperate day, with %s degrees and a high of %s." %(temp, high),
                     "I predict a nice day! It's %s degrees now and it will reach a high of %s later on." %(temp, high)],
                    ["Wack on a t-shirt and maybe a jumper just in case. You should be fine though.",
                     "Wear some nice thin clothes, you might not need a jumper, but take one just in case."]))
            self.temperature = ' '.join(random.choice(say))

        elif temp < 20:
            say = list(itertools.product(
                    ["It's nice and warm today. It's %s degrees now and it will reach a high of %s later." %(temp, high),
                     "What a warm day today. The temperature is %s degrees, reaching a high of %s and a low of %s." %(temp, high, low)],
                    ["T-shirt time.", "Don't you dare wear a jacket.", "Nice day for a run!", "Time for a cold beverage.", "Loving this warmth."]))
            self.temperature = ' '.join(random.choice(say))

        else:
            self.temperature = random.choice(
                    ["It's %s degrees at the moment, with a high of %s and a low of %s." %(temp, high, low),
                     "The temperature for today is %s, reaching a high of %s and a low of %s later on." %(temp, high, low)])

    def get_condition (self, info):
        now = info['conditions']
        later = info['forecast_conditions']
        if now.lower() == later.lower():
            if 'cloud' in now.lower() and 'partly' not in now.lower():
                self.condition = random.choice(
                        ["Looks like it's another grey %s day today. Well at least it's not raining." %(now),
                         "Unfortunately it's %s today. Shame. I really wanted some sunshine." %(now)])
            elif 'sun' in now.lower():
                self.condition = random.choice(
                        ["Looks like a nice and %s day today! Really looking forward to the sunshine." %(now),
                         "Good news. It's a nice and %s day today. Enjoy the sunshine %s." %(now, self.owner),
                         "Plenty of sunshine today! The conditions for today look %s. You must be really happy %s." %(now, self.owner)])
            elif 'rain' in now.lower() or 'shower' in now.lower():
                self.condition = random.choice(
                        ["Bad news. We have %s for most of the day. Don't forget to take your umbrella!" %(now),
                         "You're going to need your umbrella today. Looks like a rainy day with %s throughout it." %(now)])
            elif 'snow' in now.lower():
                self.condition = random.choice(
                        ["I've been waiting a long time to say this. It's a snow day! I'm very happy, but I'm not programmed to sound excited. Unfortunately."])
            else:
                self.condition = random.choice(
                        ["The weather condition for today are going to be %s for the whole day."])
        else:
            if 'rain' in now.lower() or 'shower' in now.lower():
                if 'rain' in later.lower() or 'shower' in later.lower():
                    self.condition = random.choice(
                        ["Bad news. We have %s for most of the day. Don't forget to take your umbrella!" %(now),
                         "You're going to need your umbrella today. Looks like a rainy day with %s throughout it." %(now)])
                elif 'sun' in later.lower() or 'partly' in later.lower():
                    self.condition = random.choice(
                        ["Looks like you might need your umbrella this morning because of %s. But it should improve later and be %s." %(now, later),
                         "We have %s this morning, so take an umbrella. But the good news is it should get %s later." %(now, later)])
            elif 'sun' in now.lower():
                if 'rain' in later.lower() or 'shower' in later.lower():
                    self.condition = random.choice(
                        ["I've got good news and bad news. The good news is it's %s at the moment. The bad news is it will be %s later. So don't forget your umbrella." %(now, later),
                         "Looks like a nice day to start with. Being %s. But it will get %s later on, unfortunately. So take an umbrella." %(now, later)])
                elif 'partly' in later.lower():
                    self.condition = random.choice(
                        ["It's a nice and %s day to start with. But it will be %s later on. Still, not a bad day." %(now, later)])
            elif 'storm' in now.lower() or 'storm' in later.lower():
                self.condition = random.choice(
                        ["Oh dear! There's a storm brewing today. It's %s now and %s later. How scary! I am genuinly scared, but my programming won't allow me to express it." %(now, later)])
            elif 'rain' in later.lower() or 'shower' in later.lower():
                self.condition = random.choice(
                        ["Oh dear, right now the conditions are %s, but looks like %s later on. So don't forget your umbrella." %(now, later),
                         "Right now I foresee %s. But I'm afraid later on there's %s... I would take an umbrella if I were you." %(now, later)])
            else:
                self.condition = random.choice(
                        ["The weather conditions for today are going to be %s in the morning and will then be %s later on." %(now, later)])
                
    def get_wind(self, info):
        speed = float(info['wind'])
        condition = info['conditions'] + ' ' + info['forecast_conditions']
        if speed < 20.00:
            if 'rain' in condition or 'shower' in condition:
                self.wind = "Luckily there's very little wind, so the rain shouldn't be too bad."
            else:
                self.wind = "Luckily it looks like there's very little wind today."
        elif 20.00 < speed < 40.00:
            if 'rain' in condition or 'shower' in condition:
                self.wind = "There's a slight breeze today. Bring a strong umbrella just in case."
            else:
                self.wind = "Luckily there's only a slight breeze today. Nothing too strong."
        elif speed > 40.00:
            if 'rain' in condition or 'shower' in condition:
                self.wind = "Sorry to be the bearer of bad news. It's very windy and raining outside. So it might be raining sideways. Bring your strongest umbrella!"
            else:
                self.wind = "I must warn you. It's pretty windy outside! So take care!"

    def get_sun_rise_set(self, info):
        sunrise = info['sunrise']
        sunset = info['sunset']
        rise_hour = int(sunrise[0])
        set_hour = int(sunset[0])
        if 'am' in sunrise and 'pm' in sunset:
            if rise_hour >= 8:
                rises = random.choice([" the sun rises quite late today, at %s." %(sunrise),
                                       " sunrise is at %s today, so it'll be quite dark until then." %(sunrise)])
            elif rise_hour == 7:
                rises = random.choice([" the sun rises at a good time today, %s to be exact." %(sunrise),
                                       " sunrise is at %s today, not a bad time." %(sunrise)])
            elif rise_hour <= 6:
                rises = random.choice([" the sun rises pretty early today, %s to be exact." %(sunrise),
                                       " sunrise is at %s today, really early." %(sunrise)])
            if set_hour < 5:
                sets = random.choice([" And the sun sets very early at %s, so remember it will get dark very soon." %(sunset),
                                      " And remember, it will get dark very early today. Sunset is at %s." %(sunset)])
            elif 7 > set_hour >= 5:
                sets = random.choice([" And the sun sets early at %s, so remember it will get dark then." %(sunset),
                                      " And remember, it will start getting dark after %s." %(sunset)])
            elif 9 > set_hour >= 7:
                sets = random.choice([" And the sun sets at %s, so there's plenty of daylight until then." %(sunset),
                                      " And remember, it starts getting dark after %s, so there's plenty of daylight." %(sunset)])
            elif set_hour >= 9:
                sets = random.choice([" God I love summer, you get such long days. Anyway, the sun sets at %s today." %(sunset),
                                      " We have a long day ahead. What I mean is that the sun sets at %s." %(sunset)])
            self.sun = 'And %s,' %(random.choice(['finally', 'just FYI', 'to conclude', 'to finish on the weather'])) + rises + sets
        else:
            self.sun = random.choice(
                ["And %s, just so you know: the sun rises at %s and sets at %s today." %(random.choice(['finally', 'to conclude', 'now']), sunrise, sunset),
                 "Just as an FYI, the sun today rises at %s and sets at %s." %(sunrise, sunset)])
