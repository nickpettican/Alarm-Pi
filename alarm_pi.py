#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, time, json, random, pyvona

from pivona_talk import Pivona
from weather import Weather
from good_morning import Write_greeting

def main():
    greeting = Write_greeting()
    greeting.greet()
    weather = Weather()
    weather.weather_talk()

if __name__ == "__main__":
    main()
