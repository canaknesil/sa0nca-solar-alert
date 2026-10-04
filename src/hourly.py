#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import urllib.request
import json
from pathlib import Path
import requests
import os


def create_empty_state():
    return {
        "80m-40m": {"day": None, "night": None},
        "30m-20m": {"day": None, "night": None},
        "17m-15m": {"day": None, "night": None},
        "12m-10m": {"day": None, "night": None},
        "80m-40m": {"day": None, "night": None},
        "30m-20m": {"day": None, "night": None},
        "17m-15m": {"day": None, "night": None},
        "12m-10m": {"day": None, "night": None},
    }


def write_state(fname, state):
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)


def read_state(fname):
    with open(fname, "r", encoding="utf-8") as f:
        state = json.load(f)
    return state


def state_diff(new_state, old_state):
    change = []
    for band in new_state:
        new_band_state = new_state[band]
        old_band_state = old_state[band]
        for time in new_band_state:
            new_condition = new_band_state[time]
            old_condition = old_band_state[time]
            #print(old_condition, "->", new_condition)
            if new_condition != old_condition:
                change.append((band, time, old_condition, new_condition))
    return change


def create_change_report(change):
    s = ""
    for (band, time, old, new) in change:
        s += f"{band} {time}: {old} -> {new}\n"
    return s



def fetch_data():
    URL = "https://www.hamqsl.com/solarxml.php"
    root = ET.fromstring(urllib.request.urlopen(URL, timeout=15).read())
    state = create_empty_state()
    
    for b in root.iter("band"):
        state[b.get("name")][b.get("time")] = b.text.strip()

    return state


def notify_change(msg, ntfy_topic):
    requests.post(
        "https://ntfy.sh/" + ntfy_topic,
        data=msg,
        headers={
            "Title": "Band availability has changed",
        },
        timeout=10,
    )


state_fname = os.environ.get('SA0NCA_SOLAR_ALERT_STATE_FNAME') or "/tmp/solar-alert-state.json"
ntfy_topic = os.environ.get('SA0NCA_SOLAR_ALERT_NTFY_TOPIC')

if not ntfy_topic:
    raise Exception("SA0NCA_SOLAR_ALERT_NTFY_TOPIC isn't set")

new_state = fetch_data()

if Path(state_fname).exists():
    old_state = read_state(state_fname)
else:
    old_state = create_empty_state()

change = state_diff(new_state, old_state)
report = create_change_report(change)
print("Change report:")
print(report)

if len(change) > 0:
    notify_change(report)
    
write_state(state_fname, new_state)
