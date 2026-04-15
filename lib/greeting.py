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

import random, arrow
from lib.personality import MORNING_GREETINGS, TIME_OF_DAY, DAY_SPECIAL, GOODBYE, pick

_QUOTE_INTROS = {
    'serious': [
        'The quote for today is.',
        'A thought for today:',
        'Your morning reading:',
    ],
    'cheeky': [
        "Here's something to ponder while you struggle to feel human.",
        'Your daily dose of unsolicited wisdom:',
        'And a quote, because why not:',
        "Wise words incoming. Try to look impressed.",
        "Someone once said, and I quote:",
    ],
    'bubbly': [
        "It's time for your morning phrase!",
        'The quote for today is.',
        'Quote for the day!',
        "Let's get up on a good mood!",
        "I'm feeling happy today!",
        'Wanna know something?',
    ],
}
_QUOTE_INTROS['chaos'] = _QUOTE_INTROS['cheeky'] + _QUOTE_INTROS['bubbly']

class Greeting:

    # --- generates hello and goodbye greetings ---

    def __init__(self, owner, app_dir, personality='bubbly'):

        self.owner = owner
        self.app_dir = app_dir
        self.personality = personality
        self.time_in_day = {'morning': False,
                    'afternoon': False,
                    'evening': False,
                    'night': False}
        self.import_quotes()
        self.get_day()
        self.generate_greeting()


    def import_quotes(self):

        try:
            with open(self.app_dir + '/lib/morning_quotes.csv') as f:
                self.quotes = [line.strip() for line in f if line.strip()]
        except Exception as e:
            self.quotes = False
            print(f'\nERROR while importing quotes: {e}\n')

    def generate_greeting(self):

        self.statement = False
        self.quote = False

        for part, check in self.time_in_day.items():

            if check:

                if part == 'morning':

                    greet = MORNING_GREETINGS[self.personality]
                    self.statement = ' '.join(random.choice(greet)).format(owner=self.owner)

                    if self.quotes:
                        intro = random.choice(_QUOTE_INTROS[self.personality])
                        self.quote = f"{intro} {random.choice(self.quotes)}"

                else:

                    tod = TIME_OF_DAY[self.personality]
                    self.statement = ' '.join(random.choice(tod)).format(owner=self.owner, part=part)

                break

        if not self.statement:

            self.statement = "I don't know what part of the day it is... But I know it's %s%s" % (self.now.format('HH:mm'), self.now.format('a'))

        active_part = next((p for p, v in self.time_in_day.items() if v), 'morning')
        self.bye = pick(GOODBYE[self.personality][active_part], owner=self.owner)

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

        self.date_today = 'Today is %s the %s of %s, %s.' % (self.now.format('dddd'), self.now.format('Do'), self.now.format('MMMM'), self.now.format('YYYY'))

        self.day_special = False

        day_name = self.now.format('dddd').lower()
        pool = DAY_SPECIAL[self.personality].get(day_name)
        if pool:
            self.day_special = pick(pool, owner=self.owner)
