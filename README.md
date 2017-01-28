# AlarmPi 1.1.1
Your smart alarm clock for the Raspberry Pi.

> Uses Python 2.7

## Synopsis

Have you got a Raspberry Pi that's just abandoned in a drawer? AlarmPi is a smart alarm 'clock' for the Raspberry Pi that plays music, gives you a weather forecast for the day, reads the top news, has a wacky personality, finds Trump quite funny and likes movie quote clips. All you need is a speaker to splug into the Pi and to follow the instructions bellow.

## Example:

For a quick test, first see _How to set up_ and insert your credentials in _run.py_. Once it is set, just use `python run.py` in the terminal and (given all the credentials are set to 'True') the following will happen:

1. Plays a short 10 - 20 second tune - which adapts to the time of year (e.g. Xmas songs)
2. Greets 'Good morning/afternoon/evening/night' and gives you a short motivational quote in the morning (you can add your own)
3. Gives you the date i.e. day of the week and day of the month
4. Gives you a weather forecast: first the temperature, followed by the condition (tells you to take an umbrella if it's raining, if it's windy, etc) and finally when the sun rises and sets
5. Reads the top 10 news headlines for the World or your own home country from Google News
6. Reads the top 10 Medical, Technological and Scientific news headlines for your home country from Google News - these can be toggled on/off
7. Wishes you a pleasant day
8. It may randomly give you a Jim Carrey, Rick and Morty or Family Guy sound clip for your (mainly my) amusement

## Motivation

I had a Raspberry Pi and it just occurred to me to make a smart alarm clock that gives me all the information I need in the mornings while I have breakfast. Kind of like a radio, but more personalised and gives you the information whenever you want it to.

## Python library requirements

* **Requests 2.10.0** - don't use 2.11+ because it does not work with text-to-speach yet
* **lxml** - to parse HTML
* **Beautiful Soup** - to parse HTML
* **Pyvona** - the voice wrapper
* **Pygame** - the audio wrapper
* **Arrow** - provides the date and time
* **Itertools** - for efficient looping
* **Random** - randomise stuff
* **Time** - no clock could do without time
* **JSON** - to sort the weather data from Yahoo! Weather

`sudo pip install <package>` should work just fine

To downgrade to Requests 2.10.0 use `sudo pip install requests==2.10.0`

## APIs

### Ivona

Ivona is the API that converts text to speech; without it AlarmPi can't talk! In order to use the Ivona voice you need to sign up for a free beta test account at Amazon: 

> [https://www.ivona.com/us/account/speechcloud/creation/](https://www.ivona.com/us/account/speechcloud/creation/)

After signing up you should get an AuthKey and AuthSecret which you insert in the credentials in _run.py_.

Browse the different voices available, the defaults for AlarmPi are 'Salli' and 'Brian', but you can use whichever you want really.

### Open Weather 

AlarmPi gets its weather information from Open Weater. It's free, and it's very easy to sign up and obtain an _auth key_:

> [https://home.openweathermap.org/users/sign_up](https://home.openweathermap.org/users/sign_up)

## How to set up

Before you do anything, check that you have all the required Python libraries. See _Python library requirements_ above. Also make sure you signed up to the _APIs_.

To enter your credentials and personal options open _run.py_. You will see the following:

```
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
```

Let me explain what it all means:

|	Variables   		|	Defaults   		|	Explanation 															|
|:---------------------:|:-----------------:|:------------------------------------------------------------------------	|
|	owner 				|	'Your name' 	|	Name by which AlarmPi will greet you and refer to you					|
|	app_dir 			|	app_directory 	|	*IMPORTANT! This tells AlarmPi where everything is 						|
|	tune 				|	True 			|	True or False depending on if you want it to play a morning tune		|
|	voice_female 		|	True 			|	True/False or the 'name' of the voice you want AlarmPi to have 			|
|	voice_male 			|	False 			|	True/False or the 'name' of the voice you want AlarmPi to have 			|
|	ivona_auth 			|	'auth' 			|	The Ivona authorisation code needed for AlarmPi to talk 				|
|	ivona_auth_secret 	|	'auth_secret'	|	The Ivona authorisation secret code needed for AlarmPi to talk 			|
|	weather 			|	True 			|	True or False depending on if you want to listen to the weather info 	|
|	weather_auth 		|	'auth' 			|	The Open Weather auth code in order to receive weather information 		|
|	city 				|	'London'		|	Your City, if this doesn't work try the closest big city near you 		|
|	country_code 		|	'uk'			|	Your country code, it has to be two characters e.g. uk is United Kingdom|
|	news 				|	True 			|	True or False depending on if you want to listen to the news 			|
|	world_news 			|	False			|	True or False depending on if you want to listen to the World news 		|
|	country_news 		|	True 			|	True or False depending on if you want to listen to your country's news |
|	health_news 		|	True 			|	True or False depending on if you want to listen to the medical news 	|
|	tech_news 			|	True 			|	True or False depending on if you want to listen to the technology news |
|	science_news 		|	False 			|	True or False depending on if you want to listen to the scientific news |

*If AlarmPi's directory is not '/home/pi/alarmpi' please make sure you go into _morning_greeting.py_ and change the directory there as well. This is something I need to fix but for now this will solve the quote import problem.

Note that you can also insert a custom Ivona voice name (e.g. 'Nicole'). However, make sure you leave the other gender's voice as False or AlarmPi will complain.

Once all is set, go to _How to schedule_ to set up the time you want it to run in.

## How to schedule

To schedule the script in your RPi I recommend using _crontab_, which can be installed on your Raspberry Pi by running `sudo apt-get crontab`.

Once you have _crontab_ installed, run `sudo crontab -e` in order to schedule your AlarmPi. Go to the bottom of the file that comes up and insert:

**Option 1**: `* * * * * python /home/pi/alarmpi/run.py`

* This will run AlarmPi but will not record activity in the _log.txt_.

**Option 2**: `* * * * * /home/pi/alarmpi/run_alarm.sh` 

* This will record all AlarmPi activity in _log.txt_. Make sure _run_alarmp.sh_ is executable by running `sudo chmod +x run_alarm.sh`. While you're at it, do the same command for both files in _audio_output_.

I know it goes without saying, but make sure you include the right path to the file (yours might not be in /home/pi/alarmpi/).

Breakdown explanation:

```
#        * * * * *  command to execute
#        ┬ ┬ ┬ ┬ ┬
#        │ │ │ │ │
#        │ │ │ │ │
#        │ │ │ │ └───── day of week (0 - 7) (0 to 6 are Sunday to Saturday; 
#	     │ │ │ │		7 is Sunday, the same as 0)
#        │ │ │ └────────── month (1 - 12)
#        │ │ └─────────────── day of month (1 - 31)
#        │ └──────────────────── hour (0 - 23)
#        └───────────────────────── min (0 - 59)
```

For example: `00 7 * * 1-5 /home/pi/alarmpi/run_alarm.sh` will run it every weekday at 7am, and `00 9 * * 6-7 /home/pi/alarmpi/run_alarm.sh` will run it in the weekend at 9am. 

## Audio output

AlarmPi comes with its own audio output command files in order to reduce background noise when the alarm is off. As it starts, it switches the audio output to AUDIO_JACK and as it finishes it switches back to HDMI. In order to change this go to the bottom of _run.py_ and disable or change as you wish.

The reason I did this is because the RPi has background noise when connected to the AUDIOJACK i.e. to speakers, so by only using them as output during the alarm you avoid this.

If you want to take advantage of this feature make sure the audio output files are executable. Again, this can be done by simply running `sudo chmod +x filename.sh`.

## Future development

Next steps will include storing all user credentials in a config file, making it easier for the user while fixing corrent issues with paths.

Also in the works is include a list of international days, so that AlarmPi will let you know what international festive/non-festive day it is.

## License

Copyright 2017 Nicolas Pettican

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.