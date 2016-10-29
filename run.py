#!/usr/bin/env python

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
'''

AlarmPi 0.0.4 by Nicolas Pettican

Bellow you can enter your credentials
in order to personalise your AlarmPi.
Explanation:

Alarmpi(owner = 'your name/nickname',               # name by which it will greet you
        tune = True or False,                       # able or disable alarm tune
        voice_female = True or False or name,       # make the voice female or give specific name
        voice_male = True or False or name,         # make the voice male or give specific name
        auth = 'your Ivona auth key',               # Ivona auth key
        auth_secret = 'your Ivona auth secret',     # Ivona auth secret key
        WOEID = 'Yahoo Weather location code',      # your Yahoo Weather location code
        weather = True or False,                    # turn weather forecasting on / off
        news = True or False,                       # turn news telling on / off
        world_news = True or False,                 # able / disable world news
        uk_news = True or False,                    # able / disable UK news
        health_news = True or False,                # able / disable UK medical news
        tech_news = True or False,                  # able / disable UK tech news
        science_news = True or False)               # able / disable UK science news

'''

from alarmpi import Alarmpi
import random, time, os

def main():
    
    # ENTER YOUR PERSONAL CREDENTIALS BELLOW
    
    alarmpi = Alarmpi(  owner = '',
                        tune = True,
                        voice_female = True,
                        voice_male = False,
                        auth = '',
                        auth_secret = '',
                        WOEID = '',
                        weather = True,
                        news = True,
                        world_news = True,
                        uk_news = True,
                        health_news = True,
                        tech_news = True,
                        science_news = True)
    
    if alarmpi.tune:
        alarmpi.alarm_sound()
    time.sleep(10)
    alarmpi.main()

if __name__ == "__main__":
    # IMPORTANT NOTE: the os.system commands bellow are for Raspberry Pi only
    # if you are not using the AlarmPi on the RPi disable them with the '#'
    os.system('/home/pi/alarmpi/audio_output/./AUDIO_JACK.sh')
    main()
    time.sleep(5*random.random())
    os.system('/home/pi/alarmpi/audio_output/./HDMI_out.sh')
