import configparser

import click
import requests

import helpers

# consts
config = configparser.ConfigParser()
with open('config.cfg') as config_file:
    config.read_file(config_file)


@click.group()
def group():
    pass


def get_task_0() -> dict:
    url = "https://poligon.aidevs.pl/dane.txt"
    response = requests.post(url)
    if response.ok:
        return response.text.splitlines()
    else:
        raise Exception(f"Request failed: {response.text}")


def post_answer_task_0():
    url = "https://poligon.aidevs.pl/verify"
    headers = {"Content-Type": "application/json"}
    answer = get_task_0()
    payload = helpers.PayloadBody(
        api_key = config.get("KEYS", "API_KEY"),
        task_name = "POLIGON",
        answer = answer 
    )
    print(answer)
    response = requests.post(url, json=payload.to_dict(), headers=headers)
    if response.ok and response.json()["code"] == 0:
        print(f"Answer has been successfully sent with message: {response.json()}")
    else:
        raise Exception(f"Sending answer failed with following error: {response.json()}")

def _day0_task():
    post_answer_task_0()

@group.command()
def day0_task():
    _day0_task()

if __name__ == "__main__":
    group()
