#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import random
import time
import arrow

from pivona_talk import Pivona
        
class Write_greeting:
    def __init__(self):
        greet = list(itertools.product(
                ["Ring ring! I'm your fucking alarm!", 'Wubba lubba dub dub!', 'I can talk?! Fantastic!'],
                ['Good morning', 'Rise and shine', 'Time to get up'],
                ['Insert-name-here', 'Mr Open-source!', 'Sleapy-head!'], 
                ["You've got a big day ahead! A great one!", 'Time for work! Come on then!', 
                 "Let's get ready! Go go go!", 'Get off your lazy ass! Just kidding, master!', 
                 'Breakfast time! Yum yum! Remember to be healthy!', 'Today is going to be a great day!']))
        replace = [('  ', ' ')]
        response = ' '.join(random.choice(greet))
        for s, r in replace:
            response = response.replace(s, r)
        self.response = response

    def day(self):
        now = arrow.now()
        day_of_month = int(now.format('D'))
        if day_of_month == 1:
            self.day_of_month = '1st'
        elif day_of_month == 2:
            self.day_of_month = '2nd'
        elif day_of_month == 3:
            self.day_of_month = '3rd'
        else:
            self.day_of_month = str(day_of_month) + 'th'
        self.day_of_week = str(now.format('dddd'))
        self.month_of_year = str(now.format('MMMM'))
        self.time_date = 'Today is %s the %s of %s' %(self.day_of_week, self.day_of_month, self.month_of_year)
    
    def greet(self):
        vona = Pivona()
        vona.vona_talk(self.response)
        self.day()
        vona.vona_talk(self.time_date)
        
        

