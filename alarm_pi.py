#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, time, json, random, pyvona, pygame

from pivona_talk import Pivona
from weather import Weather
from good_morning import Write_greeting
from nice_day import Have_a

def alarm_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('wake_up.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def main():
    alarm_sound()
    nova = Pivona()
    greeting = Write_greeting()
    greeting.greet()
    time.sleep(3)
    weather = Weather()
    weather.weather_talk()
    have_a = Have_a()
    have_a.nice_day()

if __name__ == "__main__":
    main()
