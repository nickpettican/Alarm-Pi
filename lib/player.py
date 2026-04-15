#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import arrow, subprocess, sys, os

def choose_tune(path):

    # --- chooses tune according to date ---

    today = arrow.now().format('DD MMMM').lower()

    xmas_time = 'december'
    valentines = '14 february'
    summer = ['june', 'july', 'august']

    if xmas_time == today.split()[1]:
        return path + '/sounds/xmas/'

    if valentines == today:
        return path + '/sounds/valentines/'

    if any(month in today for month in summer):
        return path + '/sounds/summer/'

    return path + '/sounds/default/'


def play_sound(path, sound):

    # --- plays the song / tune ---

    filepath = path + sound
    if sys.platform == 'darwin':
        subprocess.run(['afplay', filepath], check=True)
    else:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.mp3':
            subprocess.run(['mpg123', '-q', filepath], check=True)
        else:
            subprocess.run(['aplay', filepath], check=True)
