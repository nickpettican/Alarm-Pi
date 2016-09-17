#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyvona
import random

class Pivona:
    def __init__(self):
        vona = pyvona.create_voice('auth', 'authsecret')
        choices = [True, False]
        if random.choice(choices):
            voices = ['Nicole', 'Gwyneth', 'Salli', 'Emma']
            vona.voice_name = random.choice(voices)
        else:
            vona.voice_name = 'Emma'
        self.vona = vona
        
    def vona_talk(self, talk):
        print talk
        self.vona.speak(talk)
