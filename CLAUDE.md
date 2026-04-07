# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AlarmPi is a smart alarm clock for Raspberry Pi (Python 2.7) that greets the user, reads weather forecasts, news headlines, and plays audio via text-to-speech (Ivona API) and Pygame.

## Running the Alarm

```bash
python /home/pi/alarmpi/run.py
```

Via cron (with logging):
```bash
* * * * * /home/pi/alarmpi/run_alarm.sh
```

There are no build steps, no linting configuration, and no test suite.

## Architecture

**Entry point**: `run.py` — instantiates `Alarmpi` with all credentials and feature flags hardcoded, then calls `alarmpi.main()`.

**Orchestrator**: `alarmpi.py` — the `Alarmpi` class sequences all alarm features:
1. `morning_greeting()` → time-aware greeting + optional quote (`lib/morning_greeting.py`)
2. `weather_forecast()` → OpenWeatherMap API (`lib/weather_today.py`)
3. `news_for_today()` → Google News RSS parsing (`lib/news.py`)
4. `goodbye()` → farewell message

**Supporting libs** (`lib/`):
- `vona.py` — Pyvona wrapper for Ivona text-to-speech; generates MP3 and plays via Pygame
- `player.py` — Pygame audio playback; selects seasonal tunes from `sounds/` subdirectories
- `miscellaneous.py` — `Chances` class for probabilistic sound clip injection (1-in-N rolls)

**Audio flow**: `audio_output/AUDIO_JACK.sh` → alarm plays → `audio_output/HDMI_out.sh` (Raspberry Pi audio routing).

## Configuration

All config is in `run.py` via the `Alarmpi()` constructor arguments (owner name, API keys, city, feature toggles). There is no separate config file — the README notes this as a future improvement.

Key external dependencies and their constraints:
- **Requests 2.10.0** (exact version required — newer versions break Pyvona)
- **Pyvona** — Ivona (Amazon) TTS API wrapper
- **Pygame** — audio playback
- **Arrow** — date/time handling (used in `morning_greeting.py`)
- **lxml + BeautifulSoup** — Google News RSS parsing

## Notable Behaviors

- Greetings vary by time of day (morning/afternoon/evening/night) and day of week (Friday/Saturday/Sunday have special messages) — logic in `lib/morning_greeting.py`
- Tune selection is seasonal: `sounds/xmas/`, `sounds/valentines/`, `sounds/summer/`, `sounds/default/`
- Funny clips from `sounds/funny/` are injected randomly via `Chances` rolls (1-in-5, 1-in-10, etc.)
- Mention of "Trump" in news triggers a specific audio clip
- Rain conditions trigger "Ollie Williams" Family Guy clips
- App directory path `/home/pi/alarmpi` is hardcoded in several lib files (not just `run.py`)

## Commands for Claude

Do not make any changes until you have 95% confidence in what you need to build. Ask me follow-up questions until you reach that confidence.
