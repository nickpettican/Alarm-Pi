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

import time, random, os
from lib.utils import *
from lib.player import *
from lib.tts import Speaker
from lib.greeting import Greeting
from lib.weather import Weather
from lib.news import News
from lib.personality import SOUND_ODDS, NEWS_INTROS, pick

class Alarmpi:

	def __init__(self,
				owner,
				app_dir,
				tune,
				piper_executable,
				piper_model,
				weather_enabled,
				city=None,
				country_code=None,
				latitude=None,
				longitude=None,
				news_enabled=False,
				world_news=False,
				local_news=False,
				health_news=False,
				tech_news=False,
				science_news=False,
				search_queries=None,
				personality='bubbly'):

		self.pwd = app_dir

		self.response = {'weather': False, 'news': False}
		self.owner           = owner
		self.tune            = tune
		self.weather_enabled = weather_enabled
		self.news_enabled    = news_enabled
		self.personality     = personality if personality in SOUND_ODDS else 'bubbly'
		self._odds           = SOUND_ODDS[self.personality]
		self.news_categories = {
			'world news':  world_news,
			'local news':  local_news,
			'health news': health_news,
			'tech news':   tech_news,
			'science news': science_news,
		}
		self.search_queries = search_queries or []
		self.greeting = Greeting(owner=self.owner, app_dir=self.pwd, personality=self.personality)
		self._init_speaker(piper_executable, piper_model)
		self._init_weather(city, country_code, latitude, longitude)
		self._init_news(country_code)

	def _init_speaker(self, piper_executable, piper_model):

		try:
			self.speaker = Speaker(piper_executable=piper_executable, piper_model=piper_model)
		except Exception as e:
			print(f'ERROR while creating speaker: {e}')

	def _init_weather(self, city, country_code, latitude=None, longitude=None):

		if self.weather_enabled:
			try:
				self.weather = Weather(owner=self.owner, city=city, country_code=country_code,
				                       latitude=latitude, longitude=longitude, personality=self.personality)
				self.response['weather'] = True
			except Exception as e:
				print(f'ERROR while obtaining weather info: {e}\n')
				time.sleep(1)
				try:
					self.weather = Weather(owner=self.owner, city=city, country_code=country_code,
					                       latitude=latitude, longitude=longitude, personality=self.personality)
					self.response['weather'] = True
				except:
					self.speaker.talk("Sorry %s, I couldn't get the weather module started. Check you entered the correct data." % self.owner)

	def _init_news(self, country_code):

		try:
			self.news_reader = News(country_code=country_code, search_queries=self.search_queries)
			self.response['news'] = True
		except Exception as e:
			print(f'ERROR while starting Google News: {e}\n')
			time.sleep(1)
			try:
				self.news_reader = News(country_code=country_code, search_queries=self.search_queries)
				self.response['news'] = True
			except:
				self.speaker.talk("Sorry %s, I couldn't get the news module started." % self.owner)

	def alarm_sound(self):

		try:
			print('Choosing tune... ', end='')
			tunes_dir = choose_tune(self.pwd)

			print('playing... ', end='')
			play_sound(tunes_dir, self.choose_from_dir(tunes_dir, '.mp3'))

			print('DONE!\n')
		except:
			print('ERROR while playing tune!\n')

	def morning_greeting(self):

		try:
			if not Chances().one_in(self._odds['morning']):
				self.speaker.talk(self.greeting.statement)
			else:
				self.funny_quotes('morning')
			time.sleep(2*random.random())

			if self.greeting.quote:
				self.speaker.talk(self.greeting.quote)
				time.sleep(2*random.random())

			self.speaker.talk(self.greeting.date_today)
			time.sleep(2*random.random())

			if self.greeting.day_special:
				self.speaker.talk(self.greeting.day_special)
				time.sleep(2*random.random())

		except:
			self.speaker.talk('Good morning %s!' % self.owner)

	def weather_forecast(self):

		if self.weather_enabled and self.response['weather']:

			try:

				# --- temperature ---

				try:
					self.speaker.talk(self.weather.temperature)
				except:
					self.speaker.talk(could_not_obtain('temperature', self.owner))

				time.sleep(3*random.random())

				# --- condition ---

				try:
					if not self.weather.rain_today:
						self.speaker.talk(self.weather.condition)
						if self.weather.future_forecast:
							self.speaker.talk(self.weather.future_condition)
					else:
						if Chances().one_in(self._odds['rain']):
							wmo_code   = int(self.weather.info['wmo_code'])
							wind       = float(self.weather.info['wind'])
							rain_codes = {61, 63, 65, 80, 81, 82}
							if wmo_code in rain_codes and wind < 25.00:
								self.funny_quotes('rain_sideways')
							else:
								self.funny_quotes('rain')
						else:
							self.speaker.talk(self.weather.condition)
							if self.weather.future_forecast:
								self.speaker.talk(self.weather.future_condition)
				except:
					self.speaker.talk(could_not_obtain('weather condition', self.owner, self._odds['error']))

				if Chances().one_in(self._odds['cant_go_out']):
					self.funny_quotes('cant_go_out')

				time.sleep(3*random.random())

				# --- wind ---

				try:
					if self.weather.wind:
						self.speaker.talk(self.weather.wind)
				except:
					self.speaker.talk(could_not_obtain('wind', self.owner, self._odds['error']))

				time.sleep(3*random.random())

				# --- astrology ---

				try:
					if self.weather.sun:
						self.speaker.talk(self.weather.sun)
				except:
					self.speaker.talk(could_not_obtain('astrology', self.owner))

				time.sleep(3*random.random())

			except:
				self.speaker.talk(could_not_obtain('weather', self.owner, self._odds['error']))

		elif self.weather_enabled and not self.response['weather']:
			self.funny_quotes('dont_have_the_power')
			self.speaker.talk("%s I couldn't obtain the weather. You'll have to look out of the window today %s." % (random.choice(['Looks like', "I'm afraid", 'Sorry, but']), self.owner))

		else:
			print('Weather disabled.')

	def funny_quotes(self, statement):

		if self.personality == 'serious':
			return

		funny_sounds_path = self.pwd + '/sounds/funny/'

		if 'rain' in statement:
			self.speaker.talk(random.choice([
				'And now for the weather. Over to you Ollie.',
				'And now, over to Ollie Williams for the weather.',
				"And now here's Ollie Williams with the black-you-weather forecast."]))
			if statement == 'rain':
				play_sound(funny_sounds_path, 'Its_Gon_Rain.mp3')
			elif statement == 'rain_sideways':
				play_sound(funny_sounds_path, 'raining_sideways.mp3')
			self.speaker.talk('Thanks Olly.')

		if statement == 'nobody-cares':
			if self.personality == 'chaos':
				play_sound(funny_sounds_path, random.choice(['OMG_WHO_THE_HELL_CARES.mp3', 'thats_retarded.mp3']))
			else:
				play_sound(funny_sounds_path, 'OMG_WHO_THE_HELL_CARES.mp3')

		if statement == 'cant_go_out':
			play_sound(funny_sounds_path, 'you_cant_go_out_there.mp3')

		if statement == 'morning':
			if self.personality == 'chaos':
				play_sound(funny_sounds_path, random.choice(['you_like_popsickles.mp3']))
			path = funny_sounds_path + 'morning/'
			play_sound(path, self.choose_from_dir(path, '.mp3'))
			self.speaker.talk('And a Good Morning from me too!')

		if statement == 'trump':
			path = funny_sounds_path + 'trump/'
			play_sound(path, self.choose_from_dir(path, '.mp3'))

		if statement == 'back_to_you':
			if self.personality == 'chaos':
				play_sound(funny_sounds_path, random.choice(['back_to_you_frs.mp3', 'for_real_times.mp3', 'thank_you.mp3']))
			else:
				play_sound(funny_sounds_path, 'back_to_you_frs.mp3')

		if statement == 'dont_have_the_power':
			play_sound(funny_sounds_path, 'dont_have_the_power.mp3')

	def choose_from_dir(self, path, end):

		return random.choice([f for f in os.listdir(path) if f.endswith(end)])

	def news_for_today(self):

		if self.news_enabled and self.response['news']:

			active = [cat for cat, enabled in self.news_categories.items() if enabled]
			active += [f'{q} news' for q in self.search_queries]

			for category in active:
				try:
					self.speaker.talk(pick(NEWS_INTROS[self.personality], category=category))
					headlines = self.news_reader.get_news(category)
					self.news_loop(headlines)
					if Chances().one_in(self._odds['back_to_you']):
						self.funny_quotes('back_to_you')
				except:
					self.speaker.talk(could_not_obtain('news', self.owner, self._odds['error']))

			if Chances().one_in(self._odds['nobody_cares']):
				self.funny_quotes('nobody-cares')

	def news_loop(self, headlines):

		for headline in headlines:
			try:
				if not any(headline in seen for seen in self.news_reader.seen_headlines):
					self.speaker.talk(headline)
					self.news_reader.seen_headlines.append(headline)
					if 'trump' in headline.lower():
						if Chances().one_in(self._odds['trump']):
							self.funny_quotes('trump')
					time.sleep(2*random.random())
			except:
				continue

	def goodbye(self):

		try:
			self.speaker.talk(self.greeting.bye)
			time.sleep(2*random.random())
		except:
			self.speaker.talk('Bye %s' % random.choice([self.owner, 'now', 'bye']))

	def main(self):

		self.morning_greeting()
		self.weather_forecast()
		self.news_for_today()
		self.goodbye()
