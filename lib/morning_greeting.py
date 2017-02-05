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

import itertools, random, time, arrow

class Greeting:

	# --- generates hello and goodbye greetings ---

	def __init__(self, owner):
		
		self.owner = owner
		self.time_in_day = {'morning': False, 
					'afternoon': False, 
					'evening': False, 
					'night': False}
		self.import_quotes()
		self.get_day()
		self.generate_greeting()


	def import_quotes(self):

		try:
			self.quotes = [line for line in open('/home/pi/alarmpi/lib/morning_quotes.csv')]
		except:
			self.quotes = False
			print '\nERROR while importing quotes!\n'

	def generate_greeting(self):

		self.statement = False
		self.quote = False

		for part, check in self.time_in_day.items():

			if check:

				if part == 'morning':

					greet = list(itertools.product(
							['Good morning,', 'Buenos dias,', 'Rise and shine,', 'Up you get,', 'Cock-a-doodle-do,', 
							'The early bird catches the worm, as they say,'],
							[self.owner, self.owner, 'sleepy-head.', 'creater.', 'sir.', 'master.']))
					
					if self.quotes:
						quote = list(itertools.product(
								["It's time for your morning phrase.", 'The quote for today is.', 'Quote for the day.',
				 				"Let's get up on a good mood.", "I'm feeling happy today.", 'Wanna know something?'],
								self.quotes))

						self.quote = ' '.join(random.choice(quote))
					
					self.statement = ' '.join(random.choice(greet))
					break

				else:

					self.statement = 'Good %s %s' %(part, random.choice(['sir', self.owner]))
					break
		
		if not self.statement:

			self.statement = "I don't know what part of the day it is... But I know it's %s%s" %(self.now.format('HH:mm'), self.now.format('a'))

		bye = list(itertools.product(
				["Well. That's all the info from me today %s." %(self.owner), "And there you go %s. Your daily dose of awesome information." %(self.owner),
				 "I'm such a clever not aren't I? Well %s." %(self.owner), "I don't know about you. But I found that very interesting. Then again, I find everything interesting!", 
				 "And now you're well informed!", "I feel so informed already! Just kidding, I'm just a bot, huh hah hah!"],
				["Have a%s day %s." %(random.choice(['n amazing', ' great', ' nice', ' fantastic', 'n awesome']), random.choice(['boss', 'sir', 'dude', 'smarty pants'])),
				 "I hope you have a%s day %s." %(random.choice(['n amazing', ' great', ' nice', ' fantastic', 'n awesome']), random.choice(['boss', 'sir', 'dude', 'smarty pants'])),
				 "I have a%s feeling about today." %(random.choice(['n amazing', ' great', ' good', ' fantastic', 'n awesome']))],
				['Bye now!', 'TTFN, ta-ta for now.', 'Good bye!', 'See you later', 'Cheers!']))
		
		self.bye = ' '.join(random.choice(bye))

	def get_day(self):

		self.now = arrow.now()
		today  = self.now.format('DD/MM/YYYY')
		self.meridiem = self.now.format('a')

		if self.meridiem == 'am':

			if int(self.now.format('HH')) in range(0, 6):
				self.time_in_day['night'] = True

			elif int(self.now.format('HH')) in range(6, 12):
				self.time_in_day['morning'] = True

		elif self.meridiem == 'pm':
			
			if int(self.now.format('HH')) in range(12, 17):
				self.time_in_day['afternoon'] = True
			
			elif int(self.now.format('HH')) in range(17, 20):
				self.time_in_day['evening'] = True
			
			else:
				self.time_in_day['night'] = True

		self.date_today = 'Today is %s the %s of %s, %s.' %(self.now.format('dddd'), self.now.format('Do'), self.now.format('MMMM'), self.now.format('YYYY'))

                self.day_special = False

                if 'friday' in self.now.format('dddd').lower():
                        self.day_special = "I love Fridays. Last day of the week, you must have been looking forward to it! Just one more day for the weekend."
                if 'saturday' in self.now.format('dddd').lower():
                        self.day_special = "Finally, it's the weekend. Time to chill and do something productive; or do something exciting!"
                if 'sunday' in self.now.format('dddd').lower():
                        self.day_special = "I love Sundays. A good day to just relax, do some coding, or read a book... And look forward to a new week!"
