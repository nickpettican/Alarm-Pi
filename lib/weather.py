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
AIR_QUALITY_URL = 'https://air-quality-api.open-meteo.com/v1/air-quality'


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

        self._lat = lat
        self._lon = lon

        response = self.get_weather_info(lat, lon)

        if response:
            self.info = self.sort_data(response)
        if self.info:
            self.get_temperature()
            self.get_humidity()
            self.rain_today = False
            self.sun_today = False
            self.condition = self.get_condition(self.info['wmo_code'],
                                                self.info['condition_desc'], 'now')
            if self.future_forecast:
                self.future_condition = self.get_condition(self.info['future_wmo_code'],
                                                           self.info['future_condition_desc'], 'tomorrow')
            self.get_wind()
            self.get_air_quality(lat, lon)

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
                'current': 'temperature_2m,apparent_temperature,weather_code,wind_speed_10m,relative_humidity_2m',
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
                'humidity':     int(current.get('relative_humidity_2m', 0)),
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
            state   = random.choice(['fuh fuh fuh freezing', 'absolutely freezing', 'very very cold', "colder than a polar bear's butt", 'sub-zero'])
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

    def get_humidity(self):

        # --- generates a statement describing relative humidity, factoring in temperature ---

        humidity = self.info.get('humidity', 0)
        temp     = int(self.info['current_temp'])
        is_hot   = temp >= 24
        is_cold  = temp < 10

        if humidity < 30:
            level = random.choice(['very dry', 'quite dry', 'bone dry'])
            if is_hot:
                comment = random.choice([
                    'The dry heat will sap your energy fast — drink plenty of water.',
                    'At least there is no humidity, but stay hydrated in this heat.',
                    'Desert-like conditions. Sunscreen and water are your best friends today.',
                ])
            elif is_cold:
                comment = random.choice([
                    'The dry cold air will chap your lips and skin — moisturise up.',
                    'Cold and dry is a harsh combo. Lip balm and a warm drink should help.',
                    'Dry and cold — your skin is not going to thank you. Stay hydrated.',
                ])
            else:
                comment = random.choice([
                    'You might want to keep some water nearby.',
                    'Grab some lip balm and stay hydrated.',
                    'A good hair day, but drink plenty of water.',
                ])

        elif humidity < 50:
            level = random.choice(['comfortable', 'nice and comfortable', 'pleasantly dry'])
            if is_hot:
                comment = random.choice([
                    'The heat is real but at least the humidity is not making it worse.',
                    'Warm but not sticky — could be much worse.',
                    'Good humidity for the heat. Stay in the shade and you will be fine.',
                ])
            elif is_cold:
                comment = random.choice([
                    'Humidity is not adding to the chill, so that is something.',
                    'Dry cold is more manageable — layer up and you should be okay.',
                    'The cold feels cleaner at least. Wrap up well.',
                ])
            else:
                comment = random.choice([
                    'Pretty ideal conditions.',
                    'Humidity-wise, you lucked out today.',
                    'Comfortable out there — enjoy it.',
                ])

        elif humidity < 70:
            level = random.choice(['a little humid', 'somewhat humid', 'moderately humid'])
            if is_hot:
                comment = random.choice([
                    'The heat combined with the humidity will make it feel warmer than it is.',
                    'It is going to feel muggy out there. Stay in the shade where you can.',
                    'Not unbearable, but the humidity will make the heat feel stickier.',
                ])
            elif is_cold:
                comment = random.choice([
                    'The damp air will make the cold feel sharper than the temperature suggests.',
                    'Humid cold has a way of cutting through your clothes. Layer up well.',
                    'It will feel colder than it looks — the moisture in the air does not help.',
                ])
            else:
                comment = random.choice([
                    'You might feel a bit sticky outside.',
                    'Could be worse — still breathable.',
                    'A bit muggy, but manageable.',
                ])

        elif humidity < 85:
            level = random.choice(['quite humid', 'very humid', 'pretty humid'])
            if is_hot:
                comment = random.choice([
                    'The heat and humidity together are going to feel oppressive out there.',
                    'It will feel significantly hotter than the temperature reading. Stay cool.',
                    'High humidity and heat is a rough combo. Try not to overdo it outside.',
                ])
            elif is_cold:
                comment = random.choice([
                    'Damp cold is miserable — it will seep into your bones. Dress in layers.',
                    'The cold is going to feel much worse with all this moisture in the air.',
                    'Wet and cold outside. Not a great day to be hanging around outdoors.',
                ])
            else:
                comment = random.choice([
                    'Expect that lovely sticky feeling the moment you step outside.',
                    "Hair's going to do whatever it wants today.",
                    "It'll feel heavier than the temperature suggests.",
                ])

        else:
            level = random.choice(['extremely humid', 'oppressively humid', 'tropical levels of humid'])
            if temp > 30:
                comment = random.choice([
                    'Stepping outside will feel like walking into a sauna.',
                    "You'll be sweating before you've gone two steps.",
                    'The air is basically water at this point.',
                ])
            elif temp < 15:
                comment = random.choice([
                    'The cold can get into your bones, stay warm.',
                    'Not a great combination with the chilly weather.',
                    'The air is basically water at this point.',
                ])
            else:
                comment = random.choice([
                    'You will be feeling very sticky I imagine, fortunately the temperature is mild.',
                    'The air is basically water at this point.',
                ])

        self.humidity = 'Relative humidity is at %d percent — %s. %s' % (humidity, level, comment)

    def get_air_quality(self, lat, lon):

        # --- fetches European AQI from open-meteo air quality API and stores average ---

        print('Requesting air quality... ', end='')
        try:
            params = {
                'latitude':  lat,
                'longitude': lon,
                'hourly':    'european_aqi,pm2_5',
            }
            response = self.client.get(AIR_QUALITY_URL, params=params)
            if response.ok:
                data   = response.json()
                values = [v for v in data['hourly']['european_aqi'] if v is not None]
                avg    = int(round(sum(values) / len(values))) if values else None
                print(f'avg AQI: {avg}')
                self.aqi_value = avg
                self.aqi       = self._aqi_statement(avg) if avg is not None else False
            else:
                print(f'{response.status_code} ERROR')
                self.aqi_value = None
                self.aqi       = False
        except Exception as e:
            print(f'ERROR while requesting air quality: {e}')
            self.aqi_value = None
            self.aqi       = False

    def _aqi_statement(self, aqi):

        # --- generates a statement describing the air quality index ---

        if aqi <= 20:
            category = random.choice(['excellent', 'great', 'pristine'])
            comment  = random.choice([
                'Breathe it all in — wonderfully clean out there.',
                'Perfect air quality. Lucky you.',
                'As fresh as it gets.',
            ])
        elif aqi <= 40:
            category = random.choice(['good', 'fairly good', 'decent'])
            comment  = random.choice([
                'Nothing to worry about air-wise.',
                'Pretty clean out there.',
                'Healthy air today.',
            ])
        elif aqi <= 60:
            category = random.choice(['moderate', 'acceptable', 'okay'])
            comment  = random.choice([
                'Sensitive individuals might want to take it easy outside.',
                'Not ideal, but most people will be fine.',
                'A bit below perfect but generally okay.',
            ])
        elif aqi <= 80:
            category = random.choice(['poor', 'not great', 'fairly bad'])
            comment  = random.choice([
                'Limit prolonged outdoor activity if you can.',
                'Might want to keep outdoor time short today.',
                "Not the best day for a long run outside.",
            ])
        elif aqi <= 100:
            category = random.choice(['very poor', 'quite bad', 'unhealthy'])
            comment  = random.choice([
                'Best to stay indoors where possible.',
                "If you're sensitive to air quality, today's a good day to stay in.",
                'Keep outdoor exposure minimal today.',
            ])
        else:
            category = random.choice(['extremely poor', 'hazardous', 'dangerous'])
            comment  = random.choice([
                'Seriously consider staying inside today.',
                'This is not a good day to be breathing outdoor air.',
                'An air quality mask would not go amiss if you must go out.',
            ])

        return 'The air quality index is %d, which is %s. %s' % (aqi, category, comment)

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

        # track rain and sun for current conditions only — 'later' is tomorrow's forecast
        if when == 'now':
            if wmo_code in (61, 63, 65, 80, 81, 82):
                self.rain_today = True
            if wmo_code in (0, 1):
                self.sun_today = True
            intro = pick(WEATHER_NOW_INTROS[self.personality])

        elif when == 'tomorrow':
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
        return result  # for both 'now' and 'tomorrow'

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
