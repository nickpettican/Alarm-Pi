#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import random

from pivona_talk import Pivona
        
class Write_greeting:
    def __init__(self):
        greet = list(itertools.product(
                ["Ring ring! I'm your fucking alarm!", 'Wubba lubba dub dub!', 'I can talk?! Fantastic!'],
                ['Good morning', 'Rise and shine', 'Time to get up'],
                ['Insert-name-here!', 'Mr Opensourse!', 'Sleapy-head!'], 
                ["You've got a big day ahead! A great one!", 'Time for work! Come on then!', 
                 "Let's get ready! Go go go!", 'Get off your lazy ass! Just kidding, master!', 
                 'Breakfast time! Yum yum! Remember to be healthy!', 'Today is going to be a great day!']))
        replace = [('  ', ' ')]
        response = ' '.join(random.choice(greet))
        for s, r in replace:
            response = response.replace(s, r)
        self.response = response
    
    def greet(self):
        vona = Pivona()
        vona.vona_talk(self.response)

