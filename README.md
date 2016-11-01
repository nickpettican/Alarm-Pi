# AlarmPi 0.0.5
A basic Python based smart alarm clock for the Raspberry Pi.

> Uses Python 2.7

## Example run:

For a quick run, first see _How to set up_ and insert your credentials in _run.py_. Once it is set, just use `python run.py` and (given all the credentials are set to 'True') the following will happen:

1. Short 5 - 10 second tune plays
2. Greets 'Good morning' and gives you a short motivational quote
3. Tells you the date i.e. day of the week and day of the month
4. Gives you a weather forecast: first the temperature and then the condition for today
5. Reads the top 10 news headlines for the Worl and/or the UK
6. Reads the top 10 Medical, Technological and Scientific news headlines (for UK)
7. Wishes you a pleasant day

## Functionality:

* Use of Ivona as the text-to-speech voice, with the option to change the voice.
* Cheeky/cheesy personality with a dash of positiveness.
* 6 different randomly selected tunes and the option to add more.
* Randomly generated morning greetings with motivational quotes.
* Accurate and personalised weather prediction using Yahoo Weather.
* Reading of the top 10 headlines for World, UK, Science, Medical and Tech news from Google News.
* All with the option to pick and choose the functions and disable those you don't want.

## Python library requirements

* **Requests 2.10.0** - don't use 2.11+ because it does not work with pyvona
* **Beautiful Soup** - to parse html
* **Pyvona** - the voice wrapper
* **Pygame** - the audio wrapper
* **Arrow** - provides the date
* **Itertools**
* **Random**
* **Time**
* **JSON** - to sort the weather data from Yahoo! Weather

`sudo pip install <package>` should work just fine

To downgrade to Requests 2.10.0 use `sudo pip install requests==2.10.0`

## Yahoo Weather

To use the weather forecast function you need a [**Yahoo Weather WOEID** code](http://woeid.rosselliot.co.nz/). 

This can be obtained from [here](http://woeid.rosselliot.co.nz/).

## Ivona (Pyvona)

In order to use the Ivona voice you need to sign up for a free beta test account at Amazon: 

> [https://www.ivona.com/us/account/speechcloud/creation/](https://www.ivona.com/us/account/speechcloud/creation/)

After signing up you should get an AuthKey and AuthSecret which you insert in the credentials in _run.py_.

## How to set up

To enter your credentials and personal options open _run.py_. You will see the following:

```
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
```

As shown above, just insert your name, Ivona API authentication codes, your Yahoo Weather WOEID code and select what you want AlarmPi to say.

Note that you can also insert a custom Ivona voice name (e.g. 'Nicole'). However, make sure you leave the other sex's voice as False.

## How to schedule

To schedule the script in your RPi I recommend using _crontab_, which can be installed on your Raspberry Pi by running `sudo apt-get crontab`.

Once you have _crontab_ installed, run `sudo crontab -e` in order to schedule your AlarmPi. Go to the bottom of the file that comes up and insert:

Option 1: `* * * * * /home/pi/AlarmPi/run.py`

Option 2: `* * * * * /home/pi/AlarmPi/run_alarm.sh` 

Breakdown explanation:

```
#        * * * * *  command to execute
#        ┬ ┬ ┬ ┬ ┬
#        │ │ │ │ │
#        │ │ │ │ │
#        │ │ │ │ └───── day of week (0 - 7) (0 to 6 are Sunday to Saturday, or use names; 
#	     │ │ │ │		7 is Sunday, the same as 0)
#        │ │ │ └────────── month (1 - 12)
#        │ │ └─────────────── day of month (1 - 31)
#        │ └──────────────────── hour (0 - 23)
#        └───────────────────────── min (0 - 59)
```

For example: `00 7 * * 1-5 AlarmPi/run_alarm.sh` will run it every weekday at 7am, and `00 9 * * 6-7 AlarmPi/run_alarm.sh` will run it in the weekend at 9am.

With Option 1 AlarmPi will simply run, however with Option 2 (the one I use), AlarmPi will store what it says in _log.txt_. I know it goes without saying, but make sure you include the right path to the file (yours might not be in /home/pi/AlarmPi/).

If you use Option 2 make sure _run_alarmp.sh_ is executable. If not, you can easily make it by running `sudo chmod +x run_alarm.sh`. 

## Audio output

Just to bear in mind.

AlarmPi comes with its own audio output command files in order to reduce background noise when the alarm is off. As it starts, it switches the audio output to AUDIO_JACK and as it finishes it switches back to HDMI. In order to change this go to the bottom of _run.py_ and disable or change as you wish.

The reason I did this is because the RPi has background noise when connected to the AUDIOJACK i.e. to speakers, so by only using them as output during the alarm you avoid this.

If you want to take advantage of this feature make sure the audio output files are executable. Again, this can be done by simply running `sudo chmod +x filename.sh`.

## Future development

AlarmPi is still under development. My next task is to make the alarm adjustable to women users i.e. it currently greets 'sir' but no 'madam'.

Additionally, it currently only reads the news headlines. So a future version may also read out a small description.

Unfortunately, the weather (and news) is tailored mostly to people in the UK or a country with similar weather. If your country has more extreme weather then feel free to contribute and make AlarmPi more worldwide.
