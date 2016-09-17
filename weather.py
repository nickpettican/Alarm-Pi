#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, time, json, random

from pivona_talk import Pivona

class Weather:
    def __init__(self):
        weather_url = ['https://query.yahooapis.com' +
                       '/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%3D' + 
                       '28218' + 
                       '%20and%20u%3D%27C%27' + 
                       '&format=json'][0]
        self.weather_url = weather_url
    
    def get_weather_info(self):
        weather_info = requests.get(self.weather_url)
        response = weather_info.json()
        #prettified = json.dumps(response, indent=2)
        #print prettified
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
        
    def current_temperature(self, today_temp):
        if today_temp < 0:
            current_temp = 'It is freezing today! The temperature is %s degrees! ' %(today_temp)
            self.current_temp = current_temp + random.choice(['You should better wear something warm!', 
                                                             'Put on a very warm jacket! Keep warm!', 
                                                             "Don't catch a cold, I can't take of you!"])
        elif 0 <= today_temp < 5:
            current_temp = "It's quite cold at the moment! The temperature is %s degrees! " %(today_temp)
            self.current_temp = current_temp + random.choice(['Wear something warm, drink some coffee!', 
                                                             "Don't under-estimate the cold!", 
                                                             "Don't catch a cold, I can't take of you!"])
        elif 5 <= today_temp < 10:
            current_temp = "It's chilly at the moment! The temperature is %s degrees! " %(today_temp)
            self.current_temp = current_temp + random.choice(['Not too cold, but still, keep warm!', 
                                                             'Chilly chilly, not too bad for Manchester!'])
        elif 10 <= today_temp < 15:
            current_temp = "It's a bit chilly at the moment! The temperature is %s degrees! " %(today_temp)
            self.current_temp = current_temp + random.choice(["Not a bad temperature! For Manchester anyway...", 
                                                             "Should be a nice day, if it's not raining!", 
                                                             "Chilly chilly, but just a tad!"])
        elif 15 <= today_temp < 20:
            current_temp = "The temperature is quite nice, at %s degrees! " %(today_temp)
            self.current_temp = current_temp + random.choice(["Nice temperate, isn't it? Thank you Manchester...", 
                                                             "Should be a very nice day, if it's not raining!", 
                                                             "Very nice! So warm, in fact!"])
        elif 20 <= today_temp < 25:
            current_temp = "Oh my god! It's so warm! No way, it's %s degrees! " %(today_temp)
            self.current_temp = current_temp + random.choice(["Let's go to the park! Oh wait, I can't move from here...", 
                                                             "I am looking forward to today!", 
                                                             "Are we still in Manchester?!"])
        elif today_temp > 25:
            current_temp = "This is not Manchester. How can it be %s degrees? " %(today_temp)
            self.current_temp = current_temp + random.choice(["It's so hot! My circuits can't take it", 
                                                             "Let's go to the beach!", 
                                                             "Are you sure we're not in Spain?"])
    
    def condition_today(self, now, later):
        if now == later:
            if 'cloudy' in now.lower():
                return 'Looks like the weather today is %s, and, unfortunately it will remain like this for the rest of the day...' %(now)
            elif 'sunny' in now.lower():
                return 'Good news! The weather today will be %s all day!' %(now)
            elif 'rain' in now.lower():
                return "Bad news! It's going to be raining today! Take your umbrella!"
        else:
            if 'cloudy' in now.lower() and 'cloudy' in later.lower():
                return "Looks like the weather today is %s, but later on, it will become %s." %(now, later)
            elif 'cloudy' in now.lower() and 'sunny' in later.lower():
                return "It might be %s at the moment, but luckily it will become %s later!" %(now, later)
            elif 'rain' in now.lower() and 'rain' not in later.lower():
                return "Oh dear, it's %s right now. Take an umbrella! But it will be %s later!" %(now, later)
            elif 'rain' not in now.lower() and 'rain' in later.lower():
                return "Bad news, it's %s right now. But it will be %s later on, so take an umbrella!" %(now, later)

    def wind(self, speed):
        if speed < 20.00:
            return "Oh nice, there's very little wind."
        elif 20.00 < speed < 40.00:
            return "There's a slight breeze, but nothing too strong."
        elif speed > 40.00:
            return "It's pretty windy outside! Take care!"
        
    def weather_talk(self):
        vona = Pivona()
        statements = ['And now, for the weather!', "Let's see what the weather is like today!", 
                      "I like being the weather-lady!", 'Another day in paradise! Or not!']
        vona.vona_talk(random.choice(statements))
        time.sleep(2)

        self.get_weather_info()
        
        self.current_temperature(int(self.today_info['current_temp']))
        vona.vona_talk(self.current_temp)
        time.sleep(2)
    
        high_low = 'The temperature will then reach a high of %s, and a low of %s.' %(self.today_info['current_high'],self.today_info['current_low'])
        vona.vona_talk(high_low)
        time.sleep(2)
    
        condition = self.condition_today(self.today_info['conditions'], self.today_info['forecast_conditions'])
        vona.vona_talk(condition)
        time.sleep(2)
    
        wind_speed = self.wind(float(self.today_info['wind']))
        vona.vona_talk(wind_speed)
        time.sleep(2)
    
        sun_rise_set = 'And finally, the sun rises at %s, and sets at %s today.' %(self.today_info['sunrise'], self.today_info['sunset'])
        vona.vona_talk(sun_rise_set)
        time.sleep(2)

