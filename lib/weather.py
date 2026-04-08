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

import requests, random, itertools, arrow

# WMO weather code descriptions
WMO_DESCRIPTIONS = {
    0: 'clear sky',
    1: 'mainly clear', 2: 'partly cloudy', 3: 'overcast',
    45: 'fog', 48: 'icy fog',
    51: 'light drizzle', 53: 'moderate drizzle', 55: 'heavy drizzle',
    61: 'slight rain', 63: 'moderate rain', 65: 'heavy rain',
    71: 'slight snow', 73: 'moderate snow', 75: 'heavy snow',
    77: 'snow grains',
    80: 'slight rain showers', 81: 'moderate rain showers', 82: 'violent rain showers',
    85: 'slight snow showers', 86: 'heavy snow showers',
    95: 'thunderstorm',
    96: 'thunderstorm with slight hail', 99: 'thunderstorm with heavy hail',
}

WMO_TO_MAIN = {
    0: 'Clear',
    1: 'Clear', 2: 'Clouds', 3: 'Clouds',
    45: 'Atmosphere', 48: 'Atmosphere',
    51: 'Drizzle', 53: 'Drizzle', 55: 'Drizzle',
    61: 'Rain', 63: 'Rain', 65: 'Rain',
    71: 'Snow', 73: 'Snow', 75: 'Snow',
    77: 'Snow',
    80: 'Rain', 81: 'Rain', 82: 'Rain',
    85: 'Snow', 86: 'Snow',
    95: 'Thunderstorm',
    96: 'Thunderstorm', 99: 'Thunderstorm',
}

# WMO codes that involve rain or snow (used to gate wind reporting)
_RAIN_WMO = frozenset([51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99])
_SNOW_WMO = frozenset([71, 73, 75, 77, 85, 86])
_RAIN_SNOW_WMO = _RAIN_WMO | _SNOW_WMO

GEOCODING_URL = 'https://geocoding-api.open-meteo.com/v1/search'
FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'


class Weather:

    def __init__(self, owner, city=None, country_code=None, latitude=None, longitude=None):

        # --- start Weather forecast ---

        self.owner = owner
        self.city  = city if city else 'your area'
        self.client = requests.Session()
        self.sun = None  # populated only if get_sun_rise_set() is called explicitly

        if latitude is not None and longitude is not None:
            lat, lon = latitude, longitude
        elif city:
            lat, lon = self.geocode(city)
        else:
            raise ValueError("Provide either 'city' or both 'latitude' and 'longitude'.")

        response = self.get_weather_info(lat, lon)

        if response:
            self.info = self.sort_data(response)
        if self.info:
            self.get_temperature()
            self.rain_today = False
            self.condition = self.get_condition(self.info['wmo_code'],
                                                self.info['condition_desc'], 'now')
            if self.future_forecast:
                self.future_condition = self.get_condition(self.info['future_wmo_code'],
                                                           self.info['future_condition_desc'], 'later')
            self.get_wind()

    def geocode(self, city):

        # --- resolve city name to lat/lon via Open-Meteo geocoding ---

        print(f'Geocoding {city}... ', end='')
        try:
            response = self.client.get(GEOCODING_URL, params={'name': city, 'count': 1, 'language': 'en', 'format': 'json'})
            data = response.json()
            result = data['results'][0]
            print(f"found: {result['name']}, {result['country']}")
            return result['latitude'], result['longitude']
        except Exception as e:
            print(f'ERROR geocoding city: {e}')
            raise

    def get_weather_info(self, lat, lon):

        # --- request weather from Open-Meteo ---

        print('Requesting weather from Open-Meteo... ', end='')
        try:
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,apparent_temperature,weather_code,wind_speed_10m',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset',
                'timezone': 'auto',
                'forecast_days': 2,
            }
            response = self.client.get(FORECAST_URL, params=params)
            if response.ok:
                print('success!')
                return response.json()
            else:
                print(f'{response.status_code} ERROR')
                return False
        except Exception as e:
            print(f'ERROR while requesting weather info: {e}')
            return False

    def sort_data(self, response):

        # --- extract and normalise Open-Meteo response ---

        try:
            current = response['current']
            daily = response['daily']

            wmo = current['weather_code']
            tomorrow_wmo = daily['weather_code'][1]

            self.future_forecast = True

            today_info = {
                'current_temp': float(current['temperature_2m']),
                'current_low':  float(daily['temperature_2m_min'][0]),
                'current_high': float(daily['temperature_2m_max'][0]),
                'wmo_code':      wmo,
                'condition':      WMO_TO_MAIN.get(wmo, 'Unknown'),
                'condition_desc': WMO_DESCRIPTIONS.get(wmo, 'clear sky'),
                'future_wmo_code':       tomorrow_wmo,
                'future_condition':      WMO_TO_MAIN.get(tomorrow_wmo, 'Unknown'),
                'future_condition_desc': WMO_DESCRIPTIONS.get(tomorrow_wmo, 'clear sky'),
                'wind':    float(current['wind_speed_10m']),
                'sunrise': arrow.get(daily['sunrise'][0]),
                'sunset':  arrow.get(daily['sunset'][0]),
            }
            return today_info

        except Exception as e:
            print(f'ERROR while sorting weather data: {e}')
            return False

    def get_temperature(self):

        # --- generates random statements to describe the temperature ---

        temp = int(self.info['current_temp'])
        high = int(self.info['current_high'])
        low  = int(self.info['current_low'])

        options = list(itertools.product(
                        ['The temperature is %s degrees,', "It's %s degrees,"],
                        ['with a high of %s and a low of %s', 'reaching a high of %s and a low of %s']))
        temperature = ' '.join(random.choice(options)) % (temp, high, low)

        if temp < 0 and high < 0:
            state   = random.choice(['fhfuhfuh freezing', 'absolutely freezing', 'very very cold', "colder than a polar bear's butt", 'sub-zero'])
            clothes = random.choice(['your warmest clothes', 'three layers of jackets', 'plenty of clothes and gloves', 'all your wardrobe', 'at least 5 scarves'])
            advice  = random.choice(["don't you dare catch a cold", 'stay warm', "don't stay outside for too long", 'stay inside like a caveman',
                                     "of course, it's hot %s time" % random.choice(['tea', 'coffee', 'beverage'])])

        if temp in range(0, 4) or (temp < 0 and high > 0):
            state   = random.choice(['colder than a day-old dumpling', 'colder than a Monday morning', 'very cold', 'freezing', 'very very chilly'])
            clothes = random.choice(['warm clothes', 'a big coat', 'plenty of clothes', 'your thickest jacket', 'your scarf'])
            advice  = random.choice(["don't catch a cold", 'stay warm', "don't stay outside for too long", 'stay inside',
                                     "of course, it's hot %s time" % random.choice(['tea', 'coffee', 'beverage'])])

        if temp in range(4, 8):
            state   = random.choice(['cold', 'pretty cold', 'very chilly'])
            clothes = random.choice(['warm clothes', 'a jacket', 'plenty of clothes', 'a warm jumper', 'your scarf'])
            advice  = random.choice(['cover your chest', 'stay warm', "don't stay out in the cold", 'stay inside',
                                     'make a warm %s' % random.choice(['tea', 'coffee', 'beverage'])])

        if temp in range(8, 12):
            state   = random.choice(['chilly', 'a bit cold', 'mildly cold', 'cold ish'])
            clothes = random.choice(['warm clothes', 'a jacket', 'something warm', 'a warm sweater'])
            advice  = random.choice(['cover your chest', 'take care', "don't stay out too long", 'hope it gets warmer',
                                     'make a warm %s' % random.choice(['tea', 'coffee', 'beverage'])])

        if temp in range(12, 16):
            state   = random.choice(['chilly but okay', 'mild', 'pretty mild'])
            clothes = random.choice(['a jumper and a jacket', 'a thin jacket', 'spring clothes', 'a jumper'])
            advice  = random.choice(['layer up just in case', "a warm drink wouldn't go amiss", 'enjoy the fresh air',
                                     'make a warm %s' % random.choice(['tea', 'coffee', 'beverage'])])

        if temp in range(16, 20):
            state   = random.choice(['kinda warm', 'warm ish', 'a bit warm', 'pleasant'])
            clothes = random.choice(['a shirt or jumper', 'a t-shirt and jacket', 'something loose'])
            advice  = random.choice(['enjoy the day', 'get some fresh air', "don't stay inside all day", 'get out there',
                                     'make yourself %s' % random.choice(['tea', 'coffee', 'a beverage'])])

        if temp in range(20, 24):
            state   = random.choice(['nice and warm', 'warm', 'very nice', 'pleasant', 'very pleasant'])
            clothes = random.choice(['a shirt', 'a t-shirt', 'something loose', 'something thin'])
            advice  = random.choice(['enjoy the day', 'get some fresh air', "don't stay inside all day", 'get out there and enjoy',
                                     'make yourself a nice %s' % random.choice(['tea', 'coffee', 'beverage'])])

        if temp in range(24, 34):
            state   = random.choice(['very warm', 'hot', 'nice and hot', 'pleasantly hot'])
            clothes = random.choice(['a t-shirt or tank top', 'some shorts and a shirt', 'some of that summer clothing', 'summer clothes'])
            advice  = random.choice(['enjoy the day', 'get some fresh air', "don't stay inside all day", 'get out there',
                                     'make yourself an iced %s' % random.choice(['tea', 'coffee', 'beverage'])])

        if temp > 33:
            state   = random.choice(['very very hot', 'sizzling hot', 'too hot', 'unbearably hot', 'boiling'])
            clothes = random.choice(['nothing but a cap', 'some shorts and a loose t-shirt', 'plenty of sunscreen', "your birthday suit, honestly it's boiling"])
            advice  = random.choice(["don't go out if you wanna live", 'get some cold fresh air', 'drink plenty of water', 'hydrate yourself',
                                     'make yourself an iced %s' % random.choice(['tea', 'coffee', 'beverage'])])

        when       = random.choice(['now', 'right now', 'at the moment', 'at this time'])
        what_to_do = random.choice(['Make sure to', 'Be sure to', 'Do', 'Please'])
        location   = random.choice(['outside', 'in %s' % self.city])

        self.temperature = "It's %s %s %s. %s. %s wear %s, and %s." % (
            state, location, when, temperature, what_to_do, clothes, advice)

    def get_condition(self, wmo_code, condition_desc, when):

        # --- generates random statements to describe the weather conditions ---

        if when == 'now':
            intro = random.choice(['Forecast shows', 'I foresee', 'Data shows', 'Looks like we have', 'We have'])

        elif when == 'later':
            intro = random.choice(['And later on, it shows ', 'And further on, I foresee ', 'And later, data shows ', 'And later we have '])
            if wmo_code == self.info['wmo_code']:
                return random.choice(['And looks like it will be like this for the rest of the day.', 'And the rest of the day should be the same.'])
            return intro + condition_desc

        else:
            return 'Something went wrong in the "get condition function".'

        if wmo_code >= 96:
            comment = random.choice(['Ouch, watch your head.', "Don't get hit by one", "It doesn't usually last long"])
            advice  = random.choice(['Be careful', 'Good luck out there', 'Be cautious'])

        elif wmo_code == 95:
            comment = random.choice(['Scary! Although I kinda like it', 'Are you scared?', 'Oh My God', "I'm so scared %s" % self.owner, 'Bazinga'])
            advice  = random.choice(['Be careful out there', "Don't get struck by lightning", 'Good luck out there'])

        elif wmo_code in (85, 86):
            comment = random.choice(['Not the nicest of weather conditions..', "I don't mind snow, but I do mind this", "Let's hope it gets better", "Let's not let this get in the way of an awesome day"])
            advice  = random.choice(['Take your umbrella', 'Use your umbrella today', 'Layer up out there'])

        elif wmo_code in (71, 73, 75, 77):
            comment = random.choice(['Snow snow snow, I love snow; can you tell?', 'Snow day, oh yeah', 'Frosty the snowman, was a holly, jolly, soul; he would talk like me, and say hello, until I ate his nose'])
            advice  = random.choice(['Can I be cheesy and ask to build a snowman?', 'Does this mean I can skip work?', 'Fun times are ahead!'])

        elif wmo_code in (61, 63, 65, 80, 81, 82):
            self.rain_today = True
            comment = random.choice(["Darn it, rain really fries my circuits", "Well, just another rainy day", "Yikes, wish it was sunny."])
            advice  = random.choice(["Don't forget your umbrella", "Cover up and take your umbrella", "Take your umbrella %s" % self.owner])

        elif wmo_code in (51, 53, 55):
            comment = random.choice(["Well let's enjoy the day regardless", "Rain rain go away, come again another day", "Let's hope it gets better", "It could be worse"])
            advice  = random.choice(["Don't forget your umbrella", "Take your umbrella %s, don't forget" % self.owner, 'Take your umbrella just in case'])

        elif wmo_code in (45, 48):
            comment = random.choice(["At least it's not raining", "Well, it could be better", "Kinda creepy weather condition"])
            advice  = random.choice(["I can't see anything %s" % self.owner, "Unless you're driving you'll be fine.", "Try not to walk into a lamp-post"])

        elif wmo_code == 0:
            comment = random.choice(["I love standing under the stars... before you say anything, don't forget: the Sun is a star", "Yay, Sunshine", 'Good morning Sunshine, the Earth says...: hello', 'Loving life'])
            advice  = random.choice(['Although clear skies sometimes makes it colder...', 'Absence of clouds makes me happy', "It's just as clear as my source code: wink wink", "Let's enjoy it"])

        else:  # 1, 2, 3 (mainly clear / partly cloudy / overcast)
            comment = random.choice(['Just another cloudy day in %s' % self.city, "Come out Sun. Where are you?", "At least it's not raining", "Grey... grim...: that is all."])
            advice  = random.choice(['Be positive though', "It's okay", 'Every cloud has a silver lining'])

        self.condition = "%s %s. %s. %s." % (intro, condition_desc, comment, advice)
        return self.condition

    def get_wind(self):

        # --- reports wind only when it accompanies rain or snow and speed is notable ---

        speed   = float(self.info['wind'])
        wmo     = int(self.info['wmo_code'])
        is_rain = wmo in _RAIN_WMO
        is_snow = wmo in _SNOW_WMO

        if (is_rain or is_snow) and speed >= 20.0:
            if is_rain:
                if speed >= 40.0:
                    self.wind = "Sorry to be the bearer of bad news. It's very windy and raining outside. So it might be raining sideways. Bring your strongest umbrella!"
                else:
                    self.wind = "It's windy today. Bring a strong umbrella just in case."
            else:  # snow
                if speed >= 40.0:
                    self.wind = "It's very windy and snowing out there. Visibility could be poor, so take extra care."
                else:
                    self.wind = "It's a bit windy along with the snow. Layer up and brace yourself!"
        else:
            self.wind = False

    def get_sun_rise_set(self, info=None):

        # --- generates random statements to describe sunrise and sunset ---

        info     = info or self.info
        time_now = arrow.now()
        sunrise  = info['sunrise']
        sunset   = info['sunset']

        if time_now < sunrise:
            state_rise       = '%s %s' % (random.choice(['will', 'is going to', 'should']), random.choice(['rise', 'come up', 'rise and shine', 'be rising']))
            state_rise_short = 'is'
        else:
            state_rise       = '%s %s' % (random.choice(['already', 'showed his face and']), random.choice(['rose', 'came up', 'came out']))
            state_rise_short = 'was'

        if time_now < sunset:
            state_set       = '%s %s' % (random.choice(['will', 'is going to', 'should']), random.choice(['set', "say it's goodbyes"]))
            state_set_short = 'is'
        else:
            state_set       = '%s %s' % (random.choice(['already', 'has already']), random.choice(['set', 'gone to sleep', 'gone down']))
            state_set_short = 'was'

        sunrise_time = sunrise.humanize()
        sunset_time  = sunset.humanize()

        self.sun = random.choice([
            "%sthe sun today %s %s and %s %s" % (
                random.choice(['Finally, ', 'And ', 'To conclude, ', 'So, ', 'Just FYI, ', 'To finish of, ']),
                state_rise, sunrise_time, state_set, sunset_time),
            "%ssunrise %s at %s, %s. And sunset %s at %s, %s" % (
                random.choice(['Finally, ', 'And ', 'To conclude, ', '', 'Just FYI, ', '']),
                state_rise_short, sunrise.format('HH:mm'), sunrise_time,
                state_set_short,  sunset.format('HH:mm'),  sunset_time),
        ])
        return self.sun
