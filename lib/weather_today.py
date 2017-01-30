#!/usr/bin/env python
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

import requests, time, json, random, itertools, arrow
from datetime import datetime

class Weather_today:

    def __init__(self, owner, auth, city, country_code):

        # --- start Weather forecast ---
        
        self.owner = owner
        self.city = city
        self.start_requests()

        open_weather = 'http://api.openweathermap.org/data/2.5/weather?q=%s,%s&APPID=%s%s'
        celcius = '&units=metric'
        format_json = '&format=json'
        self.weather_url = open_weather %(city, country_code, auth, celcius)
        
        response = self.get_weather_info(self.weather_url)

        if response:
            self.info = self.sort_data(response)
        if self.info:
            self.get_temperature()
            self.rain_today = False
            self.condition = self.get_condition(self.info['condition'], 
                                                self.info['condition_id'], 
                                                self.info['condition_desc'], 'now')
            if self.future_forecast:
                self.future_condition = self.get_condition( self.info['future_condition'], 
                                                            self.info['future_condition_id'], 
                                                            self.info['future_condition_desc'], 'later')
            self.get_wind()
            self.get_sun_rise_set(self.info)

    def start_requests(self):

        # --- starts requests session ---

        self.pull = requests.Session()
        user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
        self.pull.headers.update({'User-Agent': user_agent})

    def sort_data(self, response):

        # --- creates the today info dictionary and returns boolean ---

        if len(response['weather']) > 1:

            if len(response['weather']) == 2:
                self.future_forecast = True
                later_desc = [response['weather'][1]['description']]
                later_id = response['weather'][1]['id']
                later_main = response['weather'][1]['main']

            elif len(response['weather']) > 2:
                self.future_forecast = True
                first = [response['weather'][1]['description'], response['weather'][1]['id'], response['weather'][1]['main']]
                later_desc = [first[0] + random.choice([' then ', ' followed by ', ' and ']) + main['description'] for main in response['weather'][2:]]
                later_id = [first[1] + main['id'] for main in response['weather'][1:]]
                later_main = [first[2] + main['main'] for main in response['weather'][1:]]

            try:
                today_info = {  'current_temp': float(response['main']['temp']),
                                'current_low': float(response['main']['temp_min']),
                                'current_high': float(response['main']['temp_max']),
                                'condition': response['weather'][0]['main'],
                                'condition_id': response['weather'][0]['id'],
                                'condition_desc': response['weather'][0]['description'],
                                'future_condition': later_main,
                                'future_condition_desc': later_desc,
                                'future_condition_id': later_id,
                                'wind': response['wind']['speed'],
                                'sunrise': arrow.get(response['sys']['sunrise']),
                                'sunset': arrow.get(response['sys']['sunset'])}
                return today_info

            except:
                print 'ERROR while sorting weather data.\n'
                return False

        else:
            self.future_forecast = False
            try:
                today_info = {  'current_temp': float(response['main']['temp']),
                                'current_low': float(response['main']['temp_min']),
                                'current_high': float(response['main']['temp_max']),
                                'condition': response['weather'][0]['main'],
                                'condition_id': response['weather'][0]['id'],
                                'condition_desc': response['weather'][0]['description'],
                                'wind': response['wind']['speed'],
                                'sunrise': arrow.get(response['sys']['sunrise']),
                                'sunset': arrow.get(response['sys']['sunset'])}
                return today_info

            except:
                print 'ERROR while sorting weather data.\n'
                return False

    def get_weather_info(self, weather_url):

        # --- request weather from open weather ---

        print 'Requesting weather info from Open Weather... ',
        
        try:
            response = self.pull.get(weather_url)
            if response.ok:
                print 'success!'
                return response.json()
            else:
                print '%s ERROR' %(response.status_code)
                return False
        except:
            print 'ERROR while requesting weather info!'
            return False
        

    def get_temperature(self):

        # --- generates random statements to discribe the temperature ---

        temp = int(self.info['current_temp'])
        high = int(self.info['current_high'])
        low = int(self.info['current_low'])

        options = list(itertools.product(
                        ['The temperature is %s degrees,', "It's %s degrees,"], 
                        ['with a high of %s and a low of %s', 'reaching a high of %s and a low of %s']))
        temperature = ' '.join(random.choice(options)) %(temp, high, low)

        if temp < 0 and high < 0:
            state = random.choice(['fhfuhfuh freezing' ,'absolutely freezing', 'very very cold', "colder than a polar bear's butt", 'minus zero'])
            clothes = random.choice(['your warmest clothes', 'three layers of jackets', 'plenty of clothes and gloves', 'all your wardrobe', 'at least 5 scarves'])
            advice = random.choice(["don't you dare catch a cold", 'stay warm', "don't stay outside for too long", 'stay inside like a caveman', 
                                    "of course, it's hot %s time" %(random.choice(['tea', 'coffee', 'beverage']))])

        if temp in range(0, 4) or (temp < 0 and high > 0):
            state = random.choice(['colder than a day-old dumpling', 'very cold', 'freezing', 'very very chilly'])
            clothes = random.choice(['warm clothes', 'a big coat', 'plenty of clothes', 'a blanket, but not outside though', 'your scarf'])
            advice = random.choice(["don't catch a cold", 'stay warm', "don't stay outside for too long", 'stay inside', 
                                    "of course, it's hot %s time" %(random.choice(['tea', 'coffee', 'beverage']))])

        if temp in range(4, 8):
            state = random.choice(['cold', 'pretty cold', 'very chilly'])
            clothes = random.choice(['warm clothes', 'a jacket', 'plenty of clothes', 'a warm jumper', 'your scarf'])
            advice = random.choice(['cover your chest', 'stay warm', "don't stay out in the cold", 'stay inside', 
                                    'make a warm %s' %(random.choice(['tea', 'coffee', 'beverage']))])

        if temp in range(8, 12):
            state = random.choice(['chilly', 'a bit cold', 'mildly cold', 'cold ish'])
            clothes = random.choice(['warm clothes', 'a jacket', 'something warm', 'a warm sweater'])
            advice = random.choice(['cover your chest', 'take care', "don't stay out too long", 'hope it gets warmer', 
                                    'make a warm %s' %(random.choice(['tea', 'coffee', 'beverage']))])

        if temp in range(12, 16):
            state = random.choice(['chilly but okay', 'mild', 'pretty mild'])
            clothes = random.choice(['a jumper and a jacket', 'a thin jacket', 'spring clothes', 'a jumper'])
            advice = random.choice(['cover your chest', 'stay warm', "don't stay out in the cold", 'stay inside', 
                                    'make a warm %s' %(random.choice(['tea', 'coffee', 'beverage']))])

        if temp in range(16, 20):
            state = random.choice(['kinda warm', 'warm ish', 'a bit warm', 'pleasant'])
            clothes = random.choice(['a shirt or jumper', 'a t-shirt and jacket', 'something loose'])
            advice = random.choice(['enjoy the day', 'get some fresh air', "don't stay inside all day", 'get out there', 
                                    'make yourself %s' %(random.choice(['tea', 'coffee', 'beverage']))])

        if temp in range(20, 24):
            state = random.choice(['nice and warm', 'warm', 'very nice', 'pleasant', 'very pleasant'])
            clothes = random.choice(['a shirt', 'a t-shirt', 'something loose', 'something thin'])
            advice = random.choice(['enjoy the day', 'get some fresh air', "don't stay inside all day", 'get out there and enjoy', 
                                    'make yourself a nice %s' %(random.choice(['tea', 'coffee', 'beverage']))])

        if temp in range(24, 34):
            state = random.choice(['very warm', 'hot', 'nice and hot', 'pleasantly hot'])
            clothes = random.choice(['a t-shirt or tank top', 'some shorts and a shirt', 'some of that summer clothing', 'summer clothes'])
            advice = random.choice(['enjoy the day', 'get some fresh air', "don't stay inside all day", 'get out there', 
                                    'make yourself an iced %s' %(random.choice(['tea', 'coffee', 'beverage']))])

        if temp > 33:
            state = random.choice(['very very hot', 'sizzling hot', 'too hot', 'unbearably hot', 'boiling'])
            clothes = random.choice(['nothing but a cap', 'some shorts and a loose t-shirt', 'plenty of sunscreen', "your birthday suit, honestly it's boiling"])
            advice = random.choice(["don't go out if you wanna live", 'get some cold fresh air', 'drink plenty of water', 'hydrate yourself', 
                                    'make yourself an iced %s' %(random.choice(['tea', 'coffee', 'beverage']))])


        when = random.choice(['now', 'right now', 'at the moment', 'at this time'])
        what_to_do = random.choice(['Make sure to', 'Be sure to', 'Do', 'Please'])

        self.temperature = "It's %s %s %s. %s. %s wear %s, and %s." %(state, random.choice(['outside', 'in %s' %(self.city)]), when, temperature, what_to_do, clothes, advice)


    def get_condition (self, condition, condition_id, condition_desc, when):

        # --- generates random statements to discribe the weather conditions ---

        if when == 'now':
            intro = random.choice(['Forecast shows', 'I foresee', 'Data shows', 'Looks like we have', 'We have'])

        elif when == 'later':
            intro = random.choice(['And later on, it shows ', 'And further on, I foresee ', 'And later, data shows ', 'And later we have '])
            if len(condition) > 1:
                return intro + ','.join(condition_desc)
            elif condition_id == self.info['condition']:
                return random.choice(['And looks like it will be like this for the rest of the day.', 'And the rest of the day should be the same.'])

        else:
            return 'Something went wrong in the "get condition function".'

        if 200 <= condition_id < 300:
            # thunderstorm
            comment = random.choice(['Scary! Although I kinda like it', 'Are you scared?', 'Oh My God', "I'm so scared %s" %self.owner, 'Bazinga'])
            advice = random.choice(['Be careful out there', "Don't get struck by lightning", 'Good luck out there'])

        if 300 <= condition_id < 400:
            # drizzle
            comment = random.choice(["Well let's enjoy the day regardless", "Rain rain go away, come again another day", "Let's hope it gets better", "It could be worse"])
            advice = random.choice(["Don't forget your umbrella", "Take your umbrella %s, don't forget" %(self.owner), 'Take your umbrella just in case'])

        if 500 <= condition_id < 600:
            self.rain_today = True
            # rain
            comment = random.choice(["Darn it, rain really fries my circuits", "Well, just another rainy day", "Yikes, wish it was sunny."])
            advice = random.choice(["Don't forget your umbrella", "Cover up and take your umbrella", "Take your umbrella %s" %(self.owner)])

        if 600 <= condition_id < 603:
            # snow
            comment = random.choice(['Snow snow snow, I love snow; can you tell?', 'Snow day, oh yeah', 'Frosty the snowman, was a holly, jolly, soul; he would talk like me, and say hello, until I ate his nose'])
            advice = random.choice(['Can I be cheesy and ask to build a snowman?', 'Does this mean I can skip work?', 'Fun times are ahead!'])

        if 611 <= condition_id < 700:
            # snow showers
            comment = random.choice(['Not the nicest of weather conditions..', "I don't mind snow, but I do mind this", "Let's hope it gets better", "Let's not let this get in the way of an awesome day"])
            advice = random.choice(["Don't forget your umbrella", 'Take your umbrella', "Use your umbrella today"])

        if 700 <= condition_id < 762:
            # atmosphere
            comment = random.choice(["At least it's not raining", "Well, it could be better", "Kinda creepy weather condition"])
            advice = random.choice(["I can't see anything %s" %(self.owner), "Unless you're driving you'll be fine.", "Try not to walk into a lamp-post"])

        if 762 <= condition_id < 800:
            # volcanic ash, tornado
            comment = random.choice(['Oh bum, this is not good', 'Oh My God'])
            advice = random.choice(["Get out of there, or not: I don't know", 'Be careful and good luck'])

        if 800 == condition_id:
            # clear
            comment = random.choice(["I love standing under the stars... before you say anything, don't forget: the Sun is a star", "Yay, Sunshine", 'Good morning Sunshine, the Earth says: hello', 'Loving life'])
            advice = random.choice(['Although clear skies sometimes makes it colder..', 'Absense of clouds makes me happy', "It's just as clear as my source code: wink wink", "Let's enjoy it"])

        if 800 < condition_id < 900:
            # clouds
            comment = random.choice(['Just another cloudy day in %s' %(self.city), "Come out Sun. Where are you?", "At least it's not raining", "Grey, grim: that is all."])
            advice = random.choice(['Be positive though', "It's okay"])

        if 903 <= condition_id < 906:
            # cold, hot, windy
            comment = random.choice(["I don't get the point of this information either"])
            advice = random.choice(["But that's all I could find for now"])

        if condition_id == 906:
            # hail
            comment = random.choice(['Ouch, watch your head.', "Don't get hit by one", "It doen't usually last long"])
            advice = random.choice(['Be careful', 'Good luck out there', 'Be cautious'])

        if 950 <= condition_id < 957:
            # breeze / wind
            comment = random.choice(["Don't get blown away", "Not the best news"])
            advice = random.choice(['Be careful', 'Good luck out there'])

        if 957 <= condition_id < 961:
            # gale
            comment = random.choice(["Wow, it's pretty windy outside", "You'll get blown away if you go outside"])
            advice = random.choice(['Be careful', 'Good luck'])

        if 961 <= condition_id < 963 or 900 <= condition_id <= 902:
            # HURRICANE
            comment = random.choice(['Oh My Fucking God, get into a bath and strap yourself to a pipe', 'This is not a joke, get the hell out of town while you can'])
            advice = random.choice(['And take me with you', "And don't forget about me"])

        self.condition = "%s %s. %s. %s." %(intro, condition_desc, comment, advice)
        return self.condition
                
    def get_wind(self):

        # --- generates statements to describe the wind speed ---

        speed = float(self.info['wind'])
        condition_id = int(self.info['condition_id'])

        if speed < 20.00:
            if condition_id in range(200, 600):
                self.wind = "Luckily there's very little wind, so the rain shouldn't be too bad."
            else:
                self.wind = False
        elif 20.00 <= speed < 40.00:
            if condition_id in range(200, 600):
                self.wind = "It's windy today. Bring a strong umbrella just in case."
            else:
                self.wind = "There's wind today. Nothing to get blown away with though, hopefully."
        elif speed > 40.00:
            if condition_id in range(200, 600):
                self.wind = "Sorry to be the bearer of bad news. It's very windy and raining outside. So it might be raining sideways. Bring your strongest umbrella!"
            else:
                self.wind = "I must warn you. It's pretty windy outside! So take care!"

    def get_sun_rise_set(self, info):

        # --- generates random statements to describe sunrise and sunset ---

        time_now = arrow.now()
        sunrise = arrow.get(info['sunrise'])
        sunset = arrow.get(info['sunset'])
        
        if time_now < sunrise:
            state_rise = '%s %s' %(random.choice(['will', 'is going to', 'should']), random.choice(['rise', 'come up', 'rise and shine', 'be rising']))
            state_rise_short = 'is'
        else:
            state_rise = '%s %s' %(random.choice(['already', 'showed his face and']), random.choice(['rose', 'came up', 'came out']))
            state_rise_short = 'was'

        if time_now < sunset:
            state_set = '%s %s' %(random.choice(['will', 'is going to', 'should']), random.choice(['set', "say it's goodbyes"]))
            state_set_short = 'is'
        else:
            state_set = '%s %s' %(random.choice(['already', 'has already']), random.choice(['set', 'gone to sleep', 'gone down']))
            state_set_short = 'was'

        sunrise_time = sunrise.humanize()
        sunset_time = sunset.humanize()

        self.sun = random.choice([  "%sthe sun today %s %s and %s %s" %(   random.choice(['Finally, ', 'And ', 'To conclude, ', 'So, ', 'Just FYI, ', 'To finish of, ']), 
                                                                            state_rise, sunrise_time, state_set, sunset_time),
                                    "%ssunrise %s at %s, %s. And sunset %s at %s, %s" %(random.choice(['Finally, ', 'And ', 'To conclude, ', '', 'Just FYI, ', '']),
                                                                                        state_rise_short, sunrise.format('HH:mm'), sunrise_time, 
                                                                                        state_set_short, sunset.format('HH:mm'), sunset_time)])

