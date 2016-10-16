#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
        Copyright 2016 Nicolas Pettican

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

'''

import itertools, random, time, arrow

class Greeting:
    def __init__(self, owner):
        self.owner = owner
        self.get_day()
        self.good_morning()

    def good_morning(self):
        greet = list(itertools.product(
                ['Good morning,', 'Buenos dias,', 'Rise and shine,', 'Up you get,', 'Cock-a-doodle-do! LOL,'],
                ['%s.' %(self.owner), 'sleepy-head.', 'you.', 'boss.', 'sir.', 'master.']))
        quote = list(itertools.product(
                ['Time for your morning quote.', 'The quote for today is.', 'Quote of the day.',
                 "Let's get up on a good mood.", "I'm feeling happy today.", 'Quote time!'],
                ['Set a goal that makes you want to jump out of bed in the morning.',
                 'When you start each day with a grateful heart, light illuminates from within.',
                 'I opened two gifts this morning: they were my eyes.',
                 'You will never have this day again, so make it count.',
                 'Rise up, start fresh, see the bright oppportunity in each new day.',
                 'The algorithm for a lovely day is. Smile at strangers. Slow down. Say thank you. Give lots of compliments. Dress nicely. Wear perfume. Observe and listen. Be charming. Laugh. Wish others a lovely day.',
                 'Having a rough morning? Place your hand over your heart. Feel that? That is called purpose. You are alive for a reason.',
                 'Every day may not be good... But there is something good in every day.',
                 'Each morning we are born again. What we do today is what matters most.',
                 'While you wake up today, someone is breathing their last breath... Be thankful and seize the day.',
                 'I love the smell of possibility in the morning.',
                 'Good morning sunshine! The earth says: "Hello!"',
                 'You do not have to be great to start, but you have to start to be great.',
                 'Rise up and attack the day with enthusiasm.',
                 'Yesterday is gone. Tomorrow is mystery. Today is blessing.',
                 'Mistakes increase your experience. And experience decreases your mistakes.',
                 'Love the life you live. Live the life you love.',
                 'Life laughs at you when you are unhappy. Life smiles at you when you are happy. But, life salutes you when you make others happy.',
                 'The plan for today? Same as always: drink coffee and be sexy!',
                 'The best thing about waking up is knowing you have another cup of coffee to enjoy.',
                 'No matter how good or bad your life is, wake up each morning and be thankful that you still have one.',
                 'If you want to make your dreams come true, the first thing to do is wake up.',
                 'Every morning starts a new page in your story. Make it a great one today.',
                 'A day without laughter is a day wasted.',
                 'You have never lived this day before. And you never will again. So make the most of it.',
                 'Life is like a mirror. It will smile at you if you smile at it.',
                 'Your future is created by what you do today not tomorrow.',
                 'If you do not risk anything, you risk more.',
                 'Be in love with your life every minute of it.',
                 'Stay positive. The only difference between a good day and a bad day is your attitude.',
                 'Every morning is a blank canvas. It is whatever you make out of it.',
                 'A smile and good morning goes a long way. And saying thank you goes even further.',
                 'Good morning you sexy beast!']))
        bye = list(itertools.product(
                ["Well. That's it for me %s." %(self.owner), "And there you go %s. Your daily dose of information." %(self.owner),
                 "I hope I didn't bore you %s." %(self.owner), "I don't know about you. But I found that very interesting."],
                ["Have a%s day %s." %(random.choice(['n amazing', ' great', ' nice', ' fantastic', 'n awesome']), self.owner),
                 "I hope you have a%s day %s." %(random.choice(['n amazing', ' great', ' nice', ' fantastic', 'n awesome']), self.owner),
                 "I have a%s feeling about today." %(random.choice(['n amazing', ' great', ' nice', ' fantastic', 'n awesome']))],
                ['Bye now!', 'TTFN, ta-ta for now.', 'Goodbye!', 'See you later', 'Cheers!']))
        self.morning = ' '.join(random.choice(greet))
        self.quote = ' '.join(random.choice(quote))
        self.bye = ' '.join(random.choice(bye))

    def get_day(self):
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
        self.date_today = 'Today is %s the %s of %s.' %(self.day_of_week, self.day_of_month, self.month_of_year)
