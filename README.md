# AlarmPi 1.1.1
Your smart alarm clock for the Raspberry Pi.

> Python 3 · Open-Meteo · Piper TTS · Google News RSS

## Synopsis

Have you got a Raspberry Pi abandoned in a drawer? AlarmPi is a smart alarm clock for the Raspberry Pi that plays music, gives you a weather forecast, reads the top news headlines, and greets you with a configurable personality — from calm and professional to absolute chaos. All you need is a speaker plugged into the Pi.

## What it does

For a quick test, set your credentials in `run.py`. Once configured, AlarmPi will:

1. Play a short 10–20 second tune that adapts to the time of year (e.g. Christmas songs in December)
2. Greet you by name with a time-aware greeting and an optional morning quote
3. Tell you the date and any special day message (Friday, Saturday, Sunday)
4. Give a weather forecast: temperature, sky condition (with umbrella advice if raining), wind (when rain/snow ≥ 20 km/h)
5. Read up to 10 headlines per enabled news category from Google News
6. Wish you a pleasant day
7. Randomly inject funny sound clips depending on your personality mode

## Motivation

I had a Raspberry Pi and it occurred to me to build a smart alarm clock that gives me everything I need in the morning over breakfast — like a radio, but more personalised.

## Requirements

### Python

Python 3.8 or later. Install dependencies with:

```bash
pip install requests arrow
```

### Text-to-speech

**On Linux / Raspberry Pi**: [Piper TTS](https://github.com/rhasspy/piper) — a fast, offline, neural TTS engine.

1. Download the Piper binary for your platform from the [Piper releases page](https://github.com/rhasspy/piper/releases)
2. Download a voice model (`.onnx` + `.onnx.json`) from the [Piper voice library](https://huggingface.co/rhasspy/piper-voices)
3. Set `piper_executable` and `piper_model` in `run.py` to their paths

Audio playback on Linux uses `aplay` (WAV) and `mpg123` (MP3) — both available via `apt`.

**On macOS**: AlarmPi uses the built-in `say` command. No configuration needed; `piper_executable` and `piper_model` are ignored.

### Weather

Weather is provided by [Open-Meteo](https://open-meteo.com/) — **no API key required**.

Supply either a `city` name (geocoded automatically) or `latitude`/`longitude` directly to skip geocoding.

### News

Google News RSS — no API key required.

## How to set up

Open `run.py` and fill in the `Alarmpi()` constructor:

```python
alarmpi = Alarmpi(
    owner            = 'Your name',         # name used in greetings
    app_dir          = app_directory,        # path to the alarmpi directory
    tune             = False,                # play a morning tune (True/False)
    piper_executable = '/path/to/piper',     # Piper binary (Linux only)
    piper_model      = '/path/to/model.onnx',# Piper voice model (Linux only)
    personality      = 'bubbly',             # serious | cheeky | bubbly | chaos
    weather_enabled  = True,
        # city         = 'London',           # city name (used if lat/lon not given)
        latitude       = 51.5,               # latitude  (skips geocoding if given)
        longitude      = -0.12,              # longitude (skips geocoding if given)
        country_code   = 'uk',               # 2-letter country code
    news_enabled     = False,
        world_news     = False,              # global news
        local_news     = True,               # your country's edition
        health_news    = True,               # health & medicine
        tech_news      = True,               # technology
        science_news   = False,              # science
        search_queries = [],                 # e.g. ['formula 1', 'AI']
)
```

### Parameter reference

| Parameter | Default | Description |
|:---|:---|:---|
| `owner` | `'Your name'` | Name AlarmPi uses to greet and refer to you |
| `app_dir` | `app_directory` | Absolute path to the AlarmPi directory |
| `tune` | `False` | Play a seasonal morning tune before speaking |
| `piper_executable` | — | Path to Piper binary (Linux/Pi only) |
| `piper_model` | — | Path to Piper `.onnx` voice model (Linux/Pi only) |
| `personality` | `'bubbly'` | Speaking style — see Personality modes below |
| `weather_enabled` | `True` | Enable weather forecast |
| `city` | `None` | City name for geocoding (ignored if lat/lon given) |
| `latitude` | `None` | Latitude — skips geocoding API call |
| `longitude` | `None` | Longitude — skips geocoding API call |
| `country_code` | `None` | ISO 3166-1 alpha-2 country code (e.g. `uk`, `us`) |
| `news_enabled` | `False` | Enable news reading |
| `world_news` | `False` | Read global news |
| `local_news` | `False` | Read your country's local edition |
| `health_news` | `False` | Read health & medical news |
| `tech_news` | `False` | Read technology news |
| `science_news` | `False` | Read science news |
| `search_queries` | `[]` | Custom search terms, e.g. `['formula 1']` |

## Personality modes

The `personality` parameter controls AlarmPi's tone, vocabulary, and how often it plays funny sound clips.

| Mode | Style | Sound effects |
|:---|:---|:---|
| `serious` | Formal, factual, no-nonsense | Disabled entirely |
| `cheeky` | Sarcastic and witty | Occasional |
| `bubbly` | Upbeat and enthusiastic (original behaviour) | Normal |
| `chaos` | Combines cheeky + bubbly vocabulary | Maximum — all clips in rotation |

Sound clips (in `sounds/funny/`) are played at random based on the personality. You can add your own MP3s to the relevant subdirectories.

## How to schedule

Use `crontab` to schedule AlarmPi on your Raspberry Pi:

```bash
sudo crontab -e
```

Add one of:

**Option 1** — run without logging:
```
00 7 * * 1-5 python3 /home/pi/alarmpi/run.py
```

**Option 2** — run with logging via the shell wrapper:
```
00 7 * * 1-5 /home/pi/alarmpi/run_alarm.sh
```

Make sure `run_alarm.sh` is executable:
```bash
sudo chmod +x run_alarm.sh
```

Example: run at 7am on weekdays and 9am on weekends:
```
00 7 * * 1-5 /home/pi/alarmpi/run_alarm.sh
00 9 * * 6-7 /home/pi/alarmpi/run_alarm.sh
```

Crontab format reference:
```
# ┌───────── min (0–59)
# │ ┌─────── hour (0–23)
# │ │ ┌───── day of month (1–31)
# │ │ │ ┌─── month (1–12)
# │ │ │ │ ┌─ day of week (0–7, both 0 and 7 = Sunday)
# │ │ │ │ │
# * * * * *  command
```

## Audio output

On Raspberry Pi, `run.py` switches audio to the 3.5mm jack at startup and back to HDMI on exit (via scripts in `audio_output/`). This eliminates background hiss when the alarm is idle. Make the scripts executable:

```bash
sudo chmod +x audio_output/AUDIO_JACK.sh audio_output/HDMI_out.sh
```

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
