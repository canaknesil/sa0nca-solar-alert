# SA0NCA Solar Alert

Alert system on changes in band availability for amateur radio operators. Changes are notified through ntfy.sh.

Solar data is fetched from <https://www.hamqsl.com/solar.html>. 

`src/hourly.py` should be executed periodically, at most hourly.

Configuration is done via environment variables:
- `SA0NCA_SOLAR_ALERT_STATE_FNAME`, optional, default to `/tmp/solar-alert-state.json`
- `SA0NCA_SOLAR_ALERT_NTFY_TOPIC`

