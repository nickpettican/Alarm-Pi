#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import random

from pivona_talk import Pivona
        
class Have_a:
    def __init__(self):
        greet = list(itertools.product(
                ["Have a great day,", 'Go change the world,', 'Work hard play hard,'],
                ['You cheeky lad', 'Scooby-Doo', 'master!'],
                ["Don't forget to make lunch", 'Make some lunch for later!', 
                 'Drink plenty of water!', 'Today is going to be a great day!']))
        replace = [('  ', ' ')]
        response = ' '.join(random.choice(greet))
        for s, r in replace:
            response = response.replace(s, r)
        self.response = response
    
    def nice_day(self):
        vona = Pivona()
        vona.vona_talk(self.response)

