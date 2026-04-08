#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Personality modes: serious | cheeky | bubbly | chaos

serious — factual, formal, no sound effects
cheeky  — sarcastic and witty, normal sound odds
bubbly  — upbeat and enthusiastic (closest to original behaviour), normal sound odds
chaos   — combines cheeky + bubbly text, maximum sound odds

Text values use {owner} and {city} as placeholders — substituted at runtime.
chaos pools are auto-built as cheeky ∪ bubbly so you only need to edit those two.

──────────────────────────────────────────────────────────────────────────────
SUGGESTED SOUND FILES  (download and drop into the listed directory)
──────────────────────────────────────────────────────────────────────────────
sounds/funny/morning/
  • "Rise and shine, Mr. Freeman" — Half-Life 2 (G-Man)
  • "Good morning Vietnam!" — Robin Williams clip
  • "Eye of the Tiger" intro (5 s) — Survivor
  • "Here comes the sun" intro — The Beatles
  • "I'm up, I'm up" vine
  • "Wakey wakey, eggs and bakey" — general

sounds/funny/weather/   ← new folder
  • "It's raining men" snippet — The Weather Girls
  • "Singin' in the rain" snippet — Gene Kelly
  • "Walking on Sunshine" intro — Katrina & The Waves
  • "Let it go" snippet — Frozen  (for snow)
  • "This is fine" meme — dog in fire (for chaos + bad weather)
  • Sad trombone / wah-wah-wah

sounds/funny/news/      ← new folder
  • "And now for something completely different" — Monty Python
  • Dramatic news-desk jingle (royalty-free)
  • "Dun dun DUNN" dramatic chord
  • "Hold on to your butts" — Jurassic Park (Samuel L. Jackson)

sounds/funny/goodbye/   ← new folder
  • "I'll be back" — Terminator
  • "Bye bye bye" intro (2 s) — *NSYNC
  • "So long, farewell" snippet — The Sound of Music
  • "Get out!" — Michael Scott (The Office)
  • Windows XP shutdown sound

sounds/funny/           (root, existing or new)
  • vine_boom.mp3        — the internet's favourite impact sound
  • rimshot.mp3          — ba-dum-tss
  • curb_theme.mp3       — Curb Your Enthusiasm snippet
  • air_horn.mp3         — general meme
  • "That escalated quickly" — Ron Burgundy (Anchorman)
──────────────────────────────────────────────────────────────────────────────
"""

import random

# ── SOUND ODDS ───────────────────────────────────────────────────────────────
# N in a "1-in-N" roll; 0 = never plays

SOUND_ODDS = {
    'serious': {
        'morning':      0,
        'rain':         0,
        'cant_go_out':  0,
        'back_to_you':  0,
        'nobody_cares': 0,
        'trump':        0,
        'error':        0,
    },
    'cheeky': {
        'morning':      5,
        'rain':         5,
        'cant_go_out':  10,
        'back_to_you':  8,
        'nobody_cares': 8,
        'trump':        3,
        'error':        5,
    },
    'bubbly': {
        'morning':      10,
        'rain':         10,
        'cant_go_out':  20,
        'back_to_you':  15,
        'nobody_cares': 20,
        'trump':        5,
        'error':        10,
    },
    'chaos': {
        'morning':      2,
        'rain':         2,
        'cant_go_out':  3,
        'back_to_you':  2,
        'nobody_cares': 3,
        'trump':        2,
        'error':        3,
    },
}

# ── MORNING GREETINGS ─────────────────────────────────────────────────────────
# Each entry is (prefix, suffix) — joined with a space; {owner} substituted at runtime

MORNING_GREETINGS = {
    'serious': [
        ('Good morning,', '{owner}.'),
        ('Good morning,', '{owner}. I hope you rested well.'),
        ('Good morning,', '{owner}. Ready for a new day?'),
    ],
    'cheeky': [
        ("Oh look who decided to roll out of bed. Good morning,", '{owner}.'),
        ("Rise and shine, sunshine.", "The world didn't pause while you were dreaming, {owner}."),
        ("Wakey wakey,", "{owner}. Time to disappoint yourself with a full day of responsibilities."),
        ("Ah, you're alive. Excellent.", "The day may now proceed, {owner}."),
        ("Good morning!", "Or is it? Hard to say until you've had coffee."),
        ("Up and at 'em,", "{owner}. Those emails won't ignore themselves."),
        ("Rise and shine,", "{owner}. The sun is out there somewhere, probably."),
        ("Well well well,", "look who finally emerged. Good morning, {owner}."),
        ("Morning,", "{owner}. Another day, another opportunity to pretend you have it all together."),
    ],
    'bubbly': [
        ('Good morning,', '{owner}!'),
        ('Buenos dias,', '{owner}!'),
        ('Rise and shine,', '{owner}!'),
        ('Up you get,', '{owner}!'),
        ('Cock-a-doodle-do,', '{owner}!'),
        ('The early bird catches the worm, as they say,', '{owner}!'),
        ('Good morning, good morning,', "it's a brand new day!"),
        ('Rise and shine,', 'beautiful! Today is going to be amazing!'),
        ('Top of the morning to you,', "{owner}! Let's make it a wonderful one!"),
        ('Wakey wakey,', '{owner}! Great things are waiting for you today!'),
    ],
}
MORNING_GREETINGS['chaos'] = MORNING_GREETINGS['cheeky'] + MORNING_GREETINGS['bubbly']

# ── TIME-OF-DAY GREETINGS (non-morning) ──────────────────────────────────────
# {part} = afternoon | evening | night

TIME_OF_DAY = {
    'serious':  [
        ('Good {part},', '{owner}.'),
    ],
    'cheeky': [
        ('Good {part},', "{owner}. Still going, I see."),
        ('Ah, good {part},', "{owner}. You've made it this far."),
        ('Good {part},', "{owner}. The day continues, apparently."),
        ('Oh,', "good {part}, {owner}. Better late than never."),
    ],
    'bubbly': [
        ('Good {part},', '{owner}!'),
        ('Good {part}!', "Hope your day has been brilliant, {owner}!"),
        ('A wonderful {part} to you,', '{owner}!'),
    ],
}
TIME_OF_DAY['chaos'] = TIME_OF_DAY['cheeky'] + TIME_OF_DAY['bubbly']

# ── DAY SPECIAL MESSAGES ──────────────────────────────────────────────────────

DAY_SPECIAL = {
    'serious': {
        'friday':   ['It is Friday. The working week is nearly complete.'],
        'saturday': ['It is Saturday. The weekend is here — enjoy it.'],
        'sunday':   ['It is Sunday. Make the most of the day before the new week.'],
    },
    'cheeky': {
        'friday': [
            "Oh look, it's Friday. You survived another week. Gold star.",
            "Friday at last. Only about 8 more hours of pretending to care.",
            "It's Friday! The one day the whole office collectively stops trying.",
            "TGIF, {owner}. That stands for Thank God I'm Finished, right?",
        ],
        'saturday': [
            "It's the weekend! Time to do all those things you said you'd do last weekend.",
            "Saturday! Congratulations on having absolutely no obligations. Don't waste it.",
            "The sacred weekend has arrived. Try not to spend it all scrolling your phone.",
            "Saturday, {owner}. The day belongs to you. Try not to squander it on laundry.",
        ],
        'sunday': [
            "Ah, Sunday. The day of rest, or as I call it, pre-Monday anxiety.",
            "It's Sunday, {owner}. The day belongs to you. And also slightly to dread.",
            "Sunday! Enjoy it. Monday is already sharpening its knives.",
            "Beautiful Sunday. Until about 6pm when it becomes existential dread o'clock.",
        ],
    },
    'bubbly': {
        'friday': [
            "I love Fridays! Last day of the week — you've absolutely smashed it, {owner}!",
            "It's Friday! The best day of the working week! Let's finish strong!",
            "Friday is here! The weekend is so close you can almost taste it!",
        ],
        'saturday': [
            "Finally, it's the weekend! Time to chill and do something brilliant!",
            "Saturday is here! Time to recharge and do something you love, {owner}!",
            "Weekend time! The world is your oyster, {owner}!",
        ],
        'sunday': [
            "I love Sundays! A wonderful day to relax, read, or do something creative!",
            "Sunday! The perfect day to take it easy and look forward to a fresh new week!",
            "Glorious Sunday, {owner}! Rest up and enjoy every moment!",
        ],
    },
}
DAY_SPECIAL['chaos'] = {
    day: DAY_SPECIAL['cheeky'][day] + DAY_SPECIAL['bubbly'][day]
    for day in ('friday', 'saturday', 'sunday')
}

# ── GOODBYES ──────────────────────────────────────────────────────────────────

GOODBYE = {
    'serious': [
        "That concludes your briefing for today, {owner}. Have a productive day.",
        "That is all for this morning, {owner}. Goodbye.",
        "You are now fully informed, {owner}. Have a good day.",
        "Thank you for listening. Have a good day, {owner}.",
    ],
    'cheeky': [
        "And that's your lot! Go forth and try not to embarrass yourself too much, {owner}.",
        "Right, I've done my bit. The rest is up to you, {owner}. No pressure. Absolutely none.",
        "Off you go, {owner}. You've got this. Probably.",
        "That's everything! I'd wish you luck but honestly you're going to need more than that.",
        "And there you have it. I'm done. You should get moving too, {owner}.",
        "Alright, I'm done talking. That makes one of us.",
        "That's all from me. Go out there and try to seem like you know what you're doing, {owner}.",
    ],
    'bubbly': [
        "Well, that's all the info from me today, {owner}! Have an absolutely fantastic day!",
        "And there you go, {owner}! Your daily dose of awesome information! Go smash it!",
        "You are so well informed right now! Have an amazing day, {owner}!",
        "That's it from me! Go out there and have a brilliant day, {owner}! You've got this!",
        "I feel so informed already! Hope your day is as amazing as you are, {owner}!",
        "Off you go, {owner}! Today is going to be wonderful, I just know it!",
    ],
}
GOODBYE['chaos'] = GOODBYE['cheeky'] + GOODBYE['bubbly']

# ── WEATHER ───────────────────────────────────────────────────────────────────

WEATHER_NOW_INTROS = {
    'serious':  ['The forecast shows', 'Current conditions show', 'Meteorological data indicates'],
    'cheeky':   [
        'Brace yourself,', 'I hate to tell you, but', "Well, the data says",
        "Apparently,", "I'm not going to sugarcoat this:",
        "Oh joy, forecast shows", "You're going to love this:",
    ],
    'bubbly':   [
        'Forecast shows', 'I foresee', 'Data shows',
        'Looks like we have', 'We have', 'Exciting news from the skies:',
        'The weather today is looking', 'Here comes the forecast:',
    ],
}
WEATHER_NOW_INTROS['chaos'] = WEATHER_NOW_INTROS['cheeky'] + WEATHER_NOW_INTROS['bubbly']

WEATHER_LATER_INTROS = {
    'serious':  ['Later today,', 'Further in the day,', 'And for later today:'],
    'cheeky':   [
        "And if that wasn't enough, later on ",
        "Oh and it gets better: later ",
        "And then, hold on to your umbrella — later ",
        "Plot twist: later ",
    ],
    'bubbly':   [
        'And later on, it shows ', 'And further on, I foresee ',
        'And later we have ', 'Looking ahead to later today: ',
    ],
}
WEATHER_LATER_INTROS['chaos'] = WEATHER_LATER_INTROS['cheeky'] + WEATHER_LATER_INTROS['bubbly']

WEATHER_SAME_AS_NOW = {
    'serious':  ['Conditions are expected to remain similar throughout the day.'],
    'cheeky':   [
        "And it's more of the same. Shocking.",
        "Looks like the rest of the day is going to be equally delightful. Or not.",
        "And the rest of the day? Same story. Prepare accordingly.",
    ],
    'bubbly':   [
        "And looks like it will be like this for the rest of the day!",
        "The rest of the day should be the same — consistency at its finest!",
        "More of the same today! At least it's predictable!",
    ],
}
WEATHER_SAME_AS_NOW['chaos'] = WEATHER_SAME_AS_NOW['cheeky'] + WEATHER_SAME_AS_NOW['bubbly']

# Per-condition (comment, advice) pairs — {owner} and {city} substituted at runtime
# serious has no comment/advice (handled as a special case in weather.py)

WEATHER_CONDITIONS = {
    'cheeky': {
        'thunderstorm': [
            ("Nature's having a full meltdown out there.", "Try not to get struck by lightning, {owner}. It'd ruin everyone's day."),
            ("Thunderstorm. Brilliant.", "The sky is basically screaming. Perfect ambiance."),
            ("Oh lovely, a thunderstorm.", "Good luck out there. You'll need it."),
        ],
        'drizzle': [
            ("Just enough rain to be annoying but not enough to cancel anything.", "Take the umbrella, {owner}. Just take it."),
            ("Light drizzle — the most passive-aggressive weather there is.", "An umbrella won't hurt."),
            ("Rain rain go away. It won't. But it's worth saying.", "Umbrella, {owner}. You know the drill."),
        ],
        'rain': [
            ("More rain. What a delightful surprise said absolutely nobody.", "Take your umbrella, {owner}. Or don't. I'm a clock, not a cop."),
            ("It's raining. Again. As it does.", "Umbrella time, {owner}."),
            ("Oh fantastic, rain. The sky's crying and honestly, same.", "Cover up and take your umbrella, {owner}."),
            ("Darn it, rain really fries my circuits.", "Don't forget your umbrella, {owner}."),
        ],
        'snow': [
            ("White stuff falling from the sky. Snow or the clouds have dandruff — could go either way.", "Dress warm either way."),
            ("It's snowing! Does this mean you can cancel everything? Asking for you.", "Fun times ahead, probably."),
            ("Snow! The beautiful kind of chaos.", "Can I request a snowman? Asking for a friend."),
        ],
        'snow_showers': [
            ("Snow showers — the weather equivalent of a half-hearted effort.", "Take an umbrella. Yes, even for snow."),
            ("It's trying to snow but can't commit. Relatable.", "Layer up and take an umbrella."),
        ],
        'fog': [
            ("Dense fog out there. Very cinematic, very inconvenient.", "Try not to walk into a lamp-post, {owner}."),
            ("You won't be able to see a thing. At least you won't have to look at anyone.", "Drive carefully, if at all."),
            ("Fog. Atmospheric? Absolutely. Useful? Not remotely.", "Unless you're a ghost, take care out there."),
        ],
        'clear': [
            ("Oh wow, the sun actually showed up. I'll believe it when I feel it.", "Don't get too attached. It might not last."),
            ("Clear skies! Quick, go outside before it changes its mind.", "Absence of clouds makes me suspicious, frankly."),
            ("Blue skies. I find it more alarming than reassuring, personally.", "Enjoy it while it lasts."),
        ],
        'clouds': [
            ("Grey. Grim. Clouds. Another one of those days.", "Be positive though. At least it's not raining. Yet."),
            ("Cloudy. Come out, Sun. We know you're in there.", "Every cloud has a silver lining, allegedly."),
            ("Overcast skies in {city}. Shocking. Truly unprecedented.", "You'll be fine. Probably."),
        ],
        'hail': [
            ("Hail. Because the weather gods apparently hate you specifically, {owner}.", "Watch your head. Seriously."),
            ("Tiny ice projectiles from the sky. Great stuff.", "Good luck out there. And your car."),
        ],
    },
    'bubbly': {
        'thunderstorm': [
            ("Ooh, a thunderstorm! How dramatic and exciting!", "Stay safe out there, {owner}! Nature's putting on quite a show!"),
            ("Thunderstorm today! A bit dramatic but kind of thrilling!", "Be careful out there, {owner}!"),
        ],
        'drizzle': [
            ("Just a light drizzle! Cosy weather if you ask me!", "Pop the umbrella and enjoy the pitter-patter, {owner}!"),
            ("A little drizzle never hurt anyone! Practically refreshing!", "Take your brolly just in case, {owner}!"),
        ],
        'rain': [
            ("It's a rainy day, {owner}! Perfect excuse for a hot drink and a film!", "Don't forget your umbrella!"),
            ("Oh, it's raining! Puddles, potential rainbows, and cosy vibes incoming!", "Cover up and take your umbrella, {owner}!"),
            ("Yikes, wish it was sunny! But a rainy day has its charm!", "Grab your umbrella and embrace it, {owner}!"),
        ],
        'snow': [
            ("It's snowing! Oh I love snow, can you tell?!", "Can I be cheesy and ask to build a snowman?!"),
            ("Snow day! This is the most exciting thing to happen all week!", "Fun times are absolutely ahead, {owner}!"),
            ("Snow snow snow! I love snow!", "Does this mean we can skip work? Asking for a friend!"),
        ],
        'snow_showers': [
            ("Snow showers! A little wintry, a lot wonderful!", "Layer up and enjoy it, {owner}!"),
            ("Ooh, some snow showers! Magical!", "Dress warm and enjoy the winter wonderland, {owner}!"),
        ],
        'fog': [
            ("A bit foggy today! Very mysterious and atmospheric!", "Take care out there, {owner}!"),
            ("Foggy conditions! Like living inside a cloud, how magical!", "Drive carefully, {owner}!"),
        ],
        'clear': [
            ("Yay, sunshine! I love clear skies, they make me so happy!", "Get outside and soak it all up, {owner}!"),
            ("Beautiful clear skies today! The sun showed up and so should you!", "What a gorgeous day, {owner}!"),
            ("Good morning sunshine, the Earth says hello! Clear skies all the way!", "Let's enjoy every single moment of it!"),
            ("Loving life with these clear skies!", "Absence of clouds makes me so happy, {owner}!"),
        ],
        'clouds': [
            ("A cloudy day, but that's totally okay! Silver linings everywhere!", "Be positive, {owner}! Every cloud has one!"),
            ("Overcast today! Perfect weather to get things done or stay cosy!", "It's going to be a great day anyway, {owner}!"),
        ],
        'hail': [
            ("Ooh, hail! A bit wild but kind of exciting!", "Watch your head out there, {owner}!"),
            ("Hail today! Nature's ice machine is working overtime!", "Be careful out there, {owner}!"),
        ],
    },
}
WEATHER_CONDITIONS['chaos'] = {
    cond: WEATHER_CONDITIONS['cheeky'].get(cond, []) + WEATHER_CONDITIONS['bubbly'].get(cond, [])
    for cond in set(list(WEATHER_CONDITIONS['cheeky']) + list(WEATHER_CONDITIONS['bubbly']))
}

# ── NEWS INTROS ───────────────────────────────────────────────────────────────

NEWS_INTROS = {
    'serious':  [
        'The top {category}:', 'Here are the top {category}:',
        'And now, the top {category}:',
    ],
    'cheeky': [
        "Alright, brace yourself for the top {category}.",
        "And now, whether you like it or not, the top {category}.",
        "Let's see what fresh chaos the top {category} has in store.",
        "Here comes the top {category}. Try to look surprised.",
        "Buckle up for the top {category}. It's been a time.",
    ],
    'bubbly': [
        "And now for the top {category}!",
        "Let's have a look at the top {category}!",
        "Now reading the top {category}!",
        "Here we go with the top {category}!",
        "Get ready for the top {category}!",
    ],
}
NEWS_INTROS['chaos'] = NEWS_INTROS['cheeky'] + NEWS_INTROS['bubbly']


def pick(pool, **kwargs):
    """Pick a random item from a pool list and format with kwargs."""
    item = random.choice(pool)
    return item.format(**kwargs) if kwargs else item
