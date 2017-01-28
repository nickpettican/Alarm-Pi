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

import time, random, os, pygame
from lib.miscellaneous import *
from lib.player import *
from lib.vona import Pivona
from lib.morning_greeting import Greeting
from lib.weather_today import Weather_today
from lib.news import Gnews

class Alarmpi:

	# --- AlarmPi V 1.0.6 by nickpettican ---

	def __init__(self,
				owner,
                app_dir,
				tune,
				voice_female,
				voice_male,
				ivona_auth,
				ivona_auth_secret,
				weather,
				weather_auth,
				city,
				country_code,
				news,
				world_news,
				country_news,
				health_news,
				tech_news,
				science_news):

		self.pwd = app_dir

		self.response = { 'weather': False, 
						  'news': False}
		self.owner = owner
		self.tune = tune
		self.tell_weather = weather
		self.tell_news = news
		self.news = {	'world news': world_news,
						'country news': country_news, 
						'medical news': health_news, 
						'technological news': tech_news, 
						'scientific news': science_news	}
		self.greet = Greeting(owner = self.owner)
		self.start_bonni(ivona_auth, ivona_auth_secret, voice_female, voice_male)
		self.get_weather(weather_auth, city, country_code)
		self.get_news(country_code)

	def start_bonni(self, ivona_auth, ivona_auth_secret, voice_female, voice_male):

		# --- creates Bonni for talking ---

		try:
			if voice_female != voice_male:
				if voice_female:
					if type(voice_female) == str:
						voice = voice_female
					else:
						voice = 'Salli'
				elif voice_male:
					if type(voice_male) == str:
						voice = voice_male
					else:
						voice = 'Brian'
			else:
				print 'ERROR, the voice has to be either male or female!'
				exit()

			self.bonni = Pivona(voice = voice, auth = ivona_auth, auth_secret = ivona_auth_secret)
		except:
			print 'ERROR while creating voice!'

	def get_weather(self, weather_auth, city, country_code):

		# --- obtains weather from Open Weather API ---

		if self.tell_weather:
			try:	
				self.weather = Weather_today(	owner = self.owner, 
												auth = weather_auth, 
												city = city, 
												country_code = country_code)
				self.response['weather'] = True
			except:
				print 'ERROR while obtaining weather info!\n'
				time.sleep(5)
				try:
					self.weather = Weather_today(	owner = self.owner, 
													auth = weather_auth, 
													city = city, 
													country_code = country_code)
					self.response['weather'] = True
				except:
					self.bonni.talk("Sorry %s, I couldn't get the weather module started. Check you entered the correct data." %(self.owner))

	def get_news(self, country_code):

		# --- obtains news from Google ---

		try:
			self.gnews = Gnews(country_code)
			self.response['news'] = True

		except:
			print 'ERROR while starting Google News!\n'
			time.sleep(5)

			try:
				self.gnews = Gnews(country_code)
				self.response['news'] = True
			except:
				self.bonni.talk("Sorry %s, I couldn't get the news module started." %(self.owner))

	def alarm_sound(self):

		# --- plays the alarm tune ---

		try:
			print 'Choosing tune... ',
			tunes_dir = choose_tune(self.pwd)
			
			print 'playing... ',
			play_sound(tunes_dir, self.choose_from_dir(tunes_dir, '.mp3'))
			
			print 'DONE!\n'
		except:
			print 'ERROR while playing tune!\n'

	def morning_greeting(self):

		# --- generates a morning greeting ---

		try:

			if not Chances().one_in_twenty():
			   self.bonni.talk(self.greet.statement)
			else:
				self.funny_quotes('morning')
			time.sleep(4*random.random())

			if self.greet.quote:
				self.bonni.talk(self.greet.quote)
				time.sleep(4*random.random())
			
			self.bonni.talk(self.greet.date_today)
			time.sleep(4*random.random())
		
		except:
			self.bonni.talk('Good morning %s!' %(self.owner))

	def weather_forecast(self):

		# --- forecast the weather ---

		if self.tell_weather and self.response['weather']:

			try:
				
				# --- temperature ---
				
				try:
					self.bonni.talk(self.weather.temperature)
				except:
					self.bonni.talk(could_not_obtain('temperature', self.owner))
				
				time.sleep(6*random.random())

				# --- condition ---
				
				#try:
				if True:
					if not self.weather.rain_today:
						self.bonni.talk(self.weather.condition)
						if self.weather.future_forecast:
							self.bonni.talk(self.weather.future_condition)

					else:
						if Chances().one_in_ten():
							if int(self.weather.info['condition_id']) in range(500, 600) and float(self.weather.info['wind']) < 25.00:
								self.funny_quotes('rain_sideways')
							else:
								self.funny_quotes('rain')
						else:
							self.bonni.talk(self.weather.condition)
							if self.weather.future_forecast:
								self.bonni.talk(self.weather.future_condition)
				#except:
				#	self.bonni.talk(could_not_obtain('weather condition', self.owner))

				if Chances().one_in_twenty():
					self.funny_quotes('cant_go_out')

				time.sleep(6*random.random())

				# --- wind ---

				try:
					if self.weather.wind:
						self.bonni.talk(self.weather.wind)
				except:
					self.bonni.talk(could_not_obtain('wind', self.owner))

				time.sleep(6*random.random())

				# --- astrology ---

				try:
					self.bonni.talk(self.weather.sun)
				except:
					self.bonni.talk(could_not_obtain('astrology', self.owner))

				time.sleep(6*random.random())

			except:
				self.bonni.talk(could_not_obtain('weather', self.owner))

		elif self.tell_weather and not self.response['weather']:
			self.funny_quotes('dont_have_the_power')
			self.bonni.talk("%s I couldn't obtain the weather. You'll have to look out of the window today %s." %(random.choice(['Looks like', "I'm afraid", 'Sorry, but']), self.owner))

		else:
			print 'Weather disabled.'

	def funny_quotes(self, statement):

		# --- just some humour ---

		self.funny_sounds_path = self.pwd + '/sounds/funny/'

		if 'rain' in statement:
			self.bonni(random.choice([  'And now for the weather. Over to you Ollie.', 
										'And now, over to Ollie Williams for the weather.', 
										"And now here's Ollie Williams with the black-you-weather forecast."]))
			if statement == 'rain':
				play_sound(self.funny_sounds_path, 'Its_Gon_Rain.mp3')
			elif statement == 'rain_sideways':
				play_sound(self.funny_sounds_path, 'raining_sideways.mp3')
			self.bonni('Thanks Olly.')

		if statement == 'nobody-cares':
			play_sound(self.funny_sounds_path, 'OMG_WHO_THE_HELL_CARES.mp3')

		if statement == 'cant_go_out':
			play_sound(self.funny_sounds_path, 'you_cant_go_out_there.mp3')

		if statement == 'morning':
			path = self.funny_sounds_path + '/morning/'
			play_sound(path, self.choose_from_dir(path, '.mp3'))
			self.bonni.talk('And a Good Morning from me too!')

		if statement == 'trump':
			path = self.funny_sounds_path + '/trump/'
			play_sound(path, self.choose_from_dir(path, '.mp3'))

		if statement == 'back_to_you':
			play_sound(self.funny_sounds_path, 'back_to_you_frs.mp3')

		if statement == 'dont_have_the_power':
			play_sound(self.funny_sounds_path, 'dont_have_the_power.mp3')

	def choose_from_dir(self, path, end):

		# --- choses random file from path that ends in 'whatever' ---

		return random.choice([file for file in os.listdir(path) if file.endswith(end)])

	def news_for_today(self):

		# --- the anchorwoman --- 

		if self.tell_news and self.response['news']:
			
			for news, tell in self.news.items():
				if tell:
					#try:
					if True: 
						self.bonni.talk('%s the top %s.' %(random.choice([	'And now for', 
																			"Let's have a look at", 
																			'Now reading']), news))
						time.sleep(4*random.random())
						top_10 = self.gnews.get_news(news)
						self.news_loop(top_10)
						if Chances().one_in_twenty():
							self.funny_quotes('back_to_you')
					#except:
					#	self.bonni.talk(could_not_obtain('news', self.owner))
			
			if Chances().one_in_twenty():
				self.funny_quotes('nobody-cares')

	def news_loop(self, top_10):

		# --- tells the top news ---
		
		for news in top_10:
			try:
				if not any(news in n for n in self.gnews.all_news):
					self.bonni.talk(news)
					self.gnews.all_news.append(news)
					if 'trump' in news.lower():
						if Chances().one_in_five():
							self.funny_quotes('trump')
					time.sleep(4*random.random())
			except:
				continue

	def goodbye(self):

		# --- good bye ---

		try:
			self.bonni.talk(self.greet.bye)
			time.sleep(4*random.random())
		except:
			self.bonni.talk('Bye %s' %(random.choice([self.owner, 'now', 'bye'])))

	def main(self):

		# --- handles all the main operations ---

		self.morning_greeting()

		self.weather_forecast()

		self.news_for_today()

		self.goodbye()
