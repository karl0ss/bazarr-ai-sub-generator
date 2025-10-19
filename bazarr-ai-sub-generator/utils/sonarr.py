import requests
import json
import configparser

config = configparser.RawConfigParser()
config.read("config.cfg")

token = config._sections["sonarr"]["token"]
base_url = config._sections["sonarr"]["url"]


def update_show_in_sonarr(show_id):
    url = f"{base_url}/api/v3/command"

    payload = json.dumps({"name": "RefreshSeries", "seriesId": show_id})
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": token,
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 404:
        print("Updated show in Sonarr")
