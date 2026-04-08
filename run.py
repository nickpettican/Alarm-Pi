#!/usr/bin/env python3

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
        piper_executable = '/path/to/piper',        # path to Piper binary (Linux only; ignored on macOS)
        piper_model = '/path/to/model.onnx',        # path to Piper ONNX voice model (Linux only)
        personality = 'bubbly',                     # serious | cheeky | bubbly | chaos
        weather_enabled = True or False,            # turn weather forecasting on / off
            city='London',                          # Your city name (used for geocoding if lat/lon not given)
            country_code='uk',                      # Your country 2 character code
            latitude=51.5,                          # (optional) latitude — skips geocoding API if provided
            longitude=-0.12,                        # (optional) longitude — skips geocoding API if provided
        news_enabled = True or False,               # turn news telling on / off
            world_news = True or False,             # enable / disable world news (global topics)
            local_news = True or False,             # enable / disable local edition (uses country_code)
            health_news = True or False,            # enable / disable health news
            tech_news = True or False,              # enable / disable technology news
            science_news = True or False,           # enable / disable science news
            search_queries = ['formula 1'])         # (optional) list of custom search terms

'''

app_directory = '/home/pi/alarmpi'

def main():
    
    # --- ENTER YOUR PERSONAL CREDENTIALS BELLOW ---

    alarmpi = Alarmpi(  owner = 'Your name',
                        app_dir = app_directory,
                        tune = False,
                        piper_executable = '/path/to/piper',
                        piper_model      = '/path/to/model.onnx',
                        personality      = 'bubbly',
                        weather_enabled  = True,
                        # city='London',
                        latitude=51.531034,
                        longitude=-0.154686,
                        country_code='uk',
                        news_enabled = False,
                            world_news = False,
                            local_news = True,
                            health_news = True,
                            tech_news = True,
                            science_news = False,
                            search_queries = [])
    
    if alarmpi.tune:
        alarmpi.alarm_sound()

    time.sleep(10)
    
    alarmpi.main()

if __name__ == "__main__":

    # --- turn speakers on ---
    
    if 'linux' in platform:
        os.system(app_directory + '/audio_output/./AUDIO_JACK.sh')
    
    # --- main function ---
    
    main()
    time.sleep(5*random.random())
    
    # --- turn speakers off ---
    
    if 'linux' in platform:
        os.system(app_directory + '/audio_output/./HDMI_out.sh')