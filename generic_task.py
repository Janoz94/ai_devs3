import configparser

import click
import requests

# consts
TASKNAME = "helloapi"   
BASE_URL = "https://tasks.aidevs.pl"
config = configparser.ConfigParser()
with open('config.cfg') as config_file:
    config.read_file(config_file)


@click.group()
def group():
    pass


def generate_answer_body(task_name: str, answer: str) -> dict:
    return {
            "task": task_name,
            "apikey": config.get("KEYS", "API_KEY"),
            "answer": answer
     }

def get_auth_token(api_key: str, task_name: str) -> str:
    url = f"{BASE_URL}/token/{task_name.lower()}"
    headers = {"Content-Type": "application/json"}
    payload = {"apikey": api_key}
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        return response.json()  # zakładamy, że token jest zawarty w odpowiedzi JSON
    else:
        raise Exception(f"Błąd podczas autoryzacji: {response.text}")


# Krok 2: Pobieranie zadania (dane wejściowe)


def get_task(token: str) -> dict:
    url = f"{BASE_URL}/task/{token}"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Błąd podczas pobierania zadania: {response.text}")


def post_answer(token: str, answer: str):
    url = f"{BASE_URL}/answer/{token}"
    headers = {"Content-Type": "application/json"}
    payload = {"answer": answer}
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        print("Odpowiedź została pomyślnie przesłana.")
    else:
        raise Exception(f"Błąd podczas zgłaszania odpowiedzi: {response.text}")


def _get_task_command():
    auth_token = get_auth_token(config.get("KEYS", "API_KEY"), TASKNAME)["token"]
    print("Token autoryzacyjny został uzyskany.")
    task = get_task(auth_token)
    cookie = task["cookie"]
    post_answer(auth_token, cookie)
    print(f"Task: {task}")


@group.command()
def get_task_command():
    _get_task_command()


if __name__ == "__main__":
    # auth_token = get_auth_token(API_KEY, TASKNAME)["token"]
    # print("Token autoryzacyjny został uzyskany.")
    # task = get_task(auth_token)
    # cookie = task["cookie"]
    # post_answer(auth_token, cookie)
    # print(f"Task: {task}")
    group()
