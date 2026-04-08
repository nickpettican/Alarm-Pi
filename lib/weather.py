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
from lib.personality import WEATHER_NOW_INTROS, WEATHER_LATER_INTROS, WEATHER_SAME_AS_NOW, WEATHER_CONDITIONS, pick

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

    def __init__(self, owner, city=None, country_code=None, latitude=None, longitude=None, personality='bubbly'):

        # --- start Weather forecast ---

        self.owner = owner
        self.city  = city if city else 'your area'
        self.personality = personality
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

    def _wmo_to_cond_key(self, wmo_code):

        if wmo_code in (96, 99):
            return 'hail'
        elif wmo_code == 95:
            return 'thunderstorm'
        elif wmo_code in (85, 86):
            return 'snow_showers'
        elif wmo_code in (71, 73, 75, 77):
            return 'snow'
        elif wmo_code in (61, 63, 65, 80, 81, 82):
            return 'rain'
        elif wmo_code in (51, 53, 55):
            return 'drizzle'
        elif wmo_code in (45, 48):
            return 'fog'
        elif wmo_code == 0:
            return 'clear'
        else:
            return 'clouds'

    def get_condition(self, wmo_code, condition_desc, when):

        # --- generates random statements to describe the weather conditions ---

        # track rain for current conditions
        if when == 'now' and wmo_code in (61, 63, 65, 80, 81, 82):
            self.rain_today = True

        if when == 'now':
            intro = pick(WEATHER_NOW_INTROS[self.personality])

        elif when == 'later':
            if wmo_code == self.info['wmo_code']:
                return pick(WEATHER_SAME_AS_NOW[self.personality])
            intro = pick(WEATHER_LATER_INTROS[self.personality])

        else:
            return 'Something went wrong in the "get condition function".'

        cond_key = self._wmo_to_cond_key(wmo_code)

        if self.personality == 'serious':
            result = f"{intro} {condition_desc}."
        else:
            pool = WEATHER_CONDITIONS[self.personality].get(cond_key, [])
            if pool:
                comment, advice = random.choice(pool)
                comment = comment.format(owner=self.owner, city=self.city)
                advice  = advice.format(owner=self.owner, city=self.city)
                result  = f"{intro} {condition_desc}. {comment} {advice}"
            else:
                result = f"{intro} {condition_desc}."

        if when == 'now':
            self.condition = result
        return result

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
