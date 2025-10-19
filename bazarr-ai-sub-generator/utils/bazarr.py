import requests
import configparser

config = configparser.RawConfigParser()
config.read("config.cfg")

token = config._sections["bazarr"]["token"]
base_url = config._sections["bazarr"]["url"]


def get_wanted_episodes():
    url = f"{base_url}/api/episodes/wanted"

    payload = {}
    headers = {"accept": "application/json", "X-API-KEY": token}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_episode_details(episode_id: str):
    url = f"{base_url}/api/episodes?episodeid%5B%5D={episode_id}"

    payload = {}
    headers = {"accept": "application/json", "X-API-KEY": token}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()["data"][0]


def sync_series():
    url = f"{base_url}/api/system/tasks?taskid=update_series"

    payload = {}
    headers = {"accept": "application/json", "X-API-KEY": token}

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 204:
        print("Updated Bazarr")
