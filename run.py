#!/usr/bin/env python

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

from alarmpi import Alarmpi
from sys import platform
import random, time, os

'''
Bellow you can enter your credentials
in order to personalise your AlarmPi.

Explanation:

Alarmpi(owner = 'your name/nickname',               # name by which it will greet you
        tune = True or False,                       # enable or disable alarm tune
        voice_female = True or False or name,       # make the voice female or give specific name
        voice_male = True or False or name,         # make the voice male or give specific name
        auth = 'your Ivona auth key',               # Ivona auth key
        auth_secret = 'your Ivona auth secret',     # Ivona auth secret key
        weather = True or False,                    # turn weather forecasting on / off
            weather_auth='your Open Weather auth',  # Open Weather auth code for weather
            city='London',                          # Your city name
            country_code='uk',                      # Your country 2 character code
        news = True or False,                       # turn news telling on / off
            world_news = True or False,             # enable / disable world news
            uk_news = True or False,                # enable / disable UK news
            health_news = True or False,            # enable / disable UK medical news
            tech_news = True or False,              # enable / disable UK tech news
            science_news = True or False)           # enable / disable UK science news

'''

app_directory = '/home/pi/alarmpi'

def main():
    
    # --- ENTER YOUR PERSONAL CREDENTIALS BELLOW ---

    alarmpi = Alarmpi(  owner = 'Your name',
                        app_dir = app_directory,
                        tune = False,
                        voice_female = True,
                        voice_male = False,
                        ivona_auth = 'auth',
                        ivona_auth_secret = 'auth_secret',
                        weather = True,
                            weather_auth='auth',
                            city='London',
                            country_code='uk',
                        news = False,
                            world_news = False,
                            country_news = True,
                            health_news = True,
                            tech_news = True,
                            science_news = False)
    
    if alarmpi.tune:
        alarmpi.alarm_sound()

    time.sleep(10)
    
    alarmpi.main()

if __name__ == "__main__":

    # --- turn speakers on ---
    
    if 'linux' in platform:
        os.system(home_directory + '/audio_output/./AUDIO_JACK.sh')
    
    # --- main function ---
    
    main()
    time.sleep(5*random.random())
    
    # --- turn speakers off ---
    
    if 'linux' in platform:
        os.system(home_directory + '/audio_output/./HDMI_out.sh')