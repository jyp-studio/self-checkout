import requests
import json


LINE_KEY = "fAf1bFGa2-3np-NztbgltNCQfj3ew3ha6gx7PwBm9IQ"
LINE_EVENT = "test_json"

CONTEXT = [
    {"name": "cherry", "price": "10"},
    {"name": "apple", "price": "50"},
    {"name": "note", "price": "100"},
    {"name": "cup", "price": "40"},
]


def sendLine (key: str, event: str, context: dict) -> None:

    # Your IFTTT LINE_URL with event name, key and json parameters (values)
    LINE_URL=f"https://maker.ifttt.com/trigger/{LINE_EVENT}/json/with/key/{LINE_KEY}"
    # session.post(LINE_URL, data=context_json, headers={'Content-Type': 'application/json'})
    r = requests.post(LINE_URL, data=json.dumps(context), headers={'Content-Type': 'application/json'})


sendLine(LINE_KEY, LINE_EVENT, CONTEXT)