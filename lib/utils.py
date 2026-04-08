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

import random, os
from lib.player import *

class Chances:

	# --- returns True or False depending on the chances ---

	def __init__(self):

		pass

	def one_in_five(self):

		return random.choice([True, False, False, False, False])

	def one_in_ten(self):

		return random.choice([	True, False, False, False, False,
								False, False, False, False, False])

	def one_in_twenty(self):

		return random.choice([	True, False, False, False, False,
								False, False, False, False, False,
								False, False, False, False, False,
								False, False, False, False, False])

	def one_in(self, n):
		"""Return True with probability 1/n. Returns False if n is 0 (disabled)."""
		if n == 0:
			return False
		return random.randint(1, n) == 1

def could_not_obtain(statement, owner, sound_n=5):

    # --- when certain information can't be obtained ---

    if Chances().one_in(sound_n):

        play_sound(os.path.join(os.path.dirname(__file__), '..', 'sounds', 'funny') + '/', 'dont_have_the_power.mp3')

    return "%s, I couldn't obtain the %s %s, %s %s." % (
        random.choice(['Oops', 'Error', 'Darn it', 'Oh boy']), statement,
        random.choice(['data', 'info', 'information']),
        random.choice(['sorry', 'apologies', "I hope it's a nice day"]), owner)
