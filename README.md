# AlarmPi 0.0.3
A basic Python based smart alarm clock for the Raspberry Pi.

> Uses Python 2.7

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

Tu use the weather forecast function you need a [**Yahoo Weather WOEID** code](http://woeid.rosselliot.co.nz/). 

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

To schedule the script in your RPi I recommend using `crontab`:

`crontab -e * * * * * /home/pi/AlarmPi/run.py`

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

Make sure you set _run.py_ as the file to run the AlarmPi

## Audio output

Just to bear in mind.

AlarmPi 0.0.3 comes with its own audio output command files in order to reduce background noise when the alarm is off. As it starts, it switches the audio output to AUDIO_JACK and as it finishes it switches back to HDMI. In order to change this go to the bottom of _run.py_ and disable or change as you wish.

The reason I did this is because the RPi has background noise when connected to the AUDIOJACK i.e. to speakers, so by only using them as output during the alarm you avoid this.

## Future development

AlarmPi is still under development. My next task is to make the alarm adjustable to women users i.e. it currently greets 'sir' but no 'madam'.

Additionally, it currently only reads the news headlines. So a future version may also read out a small description.

Unfortunately the weather is tailored mostly to people in the UK or a country with similar weather. If your country has more extreme weather then feel free to change the way AlarmPi anounces it.
