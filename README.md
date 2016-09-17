# Pi-Alarm-Clock
Python alarm clock for the RPi, greets 'good morning' and tells the weather

Feel free to use it or contribute to its development!

## Motivation
After watching a [YouTube video]('https://www.youtube.com/watch?v=julETnOLkaU') by skiwithpete (which I highly recommend you watch) I really wanted to make my own RPi speaking alarm clock. After some source-code reading I decided to go down a slightly different direction from skiwithpete by using **requests** and **pyvona**.

## Requirements
You need Python2.7 to start with, and the following libraries:

* **Requests 2.10.0** - don't use 2.11+ because it does not work with pyvona
* **Pyvona** - the voice wrapper
* **Pygame** - the audio wrapper
* **Arrow** - provides the date
* **Itertools**
* **Random**
* **JSON** - to sort the weather data from Yahoo! Weather

```sudo pip install <package>``` should work just fine

## Pyvona
For pyvona you need to sign up for a free beta test account at Amazon: 

> [https://www.ivona.com/us/account/speechcloud/creation/]('https://www.ivona.com/us/account/speechcloud/creation/')

After signing up you should get an AuthKey and AuthSecret which you can put in the [pivona_talk.py]('https://github.com/nickpettican/Pi-Alarm-Clock/blob/master/pivona_talk.py') file and should be good to go!

## Setting the alarm
To schedule th script you can use ```crontab```:

> ```crontab -e * * * * * /home/pi/PiAlarm/alarm_pi.py```

```
#       * * * * *  command to execute
#       ┬ ┬ ┬ ┬ ┬
#       │ │ │ │ │
#       │ │ │ │ │
#       │ │ │ │ └───── day of week (0 - 7) (0 to 6 are Sunday to Saturday, or use names; 7 is Sunday, the same as 0)
#       │ │ │ └────────── month (1 - 12)
#       │ │ └─────────────── day of month (1 - 31)
#       │ └──────────────────── hour (0 - 23)
#       └───────────────────────── min (0 - 59)
```

## More to come
I am constantly updating this program, as I am still learning to use classes in Python and there is plenty of room to improve.

### TTFN - Ta ta for now!
