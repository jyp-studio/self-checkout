import requests
import json


CONTEXT = [
    {"name": "mouse", "price": 499},
    {"name": "keyboard", "price": 799},
    {"name": "laptop", "price": 40000},
    {"name": "cup", "price": 199},
    {"name": "chair", "price": 500},
]


class DataBaseManager():
    def __init__(self) -> None:
        self.line_key = "fAf1bFGa2-3np-NztbgltNCQfj3ew3ha6gx7PwBm9IQ"
        self.line_event = "sendLineJson"
        self.sheet_key = "fAf1bFGa2-3np-NztbgltNCQfj3ew3ha6gx7PwBm9IQ"
        self.sheet_event = "sendSheets"

    def sendLine(key: str, event: str, context: dict) -> None:

        # Your IFTTT LINE_URL with event name, key and json parameters (values)
        LINE_URL = f"https://maker.ifttt.com/trigger/{LINE_EVENT}/json/with/key/{LINE_KEY}"
        # session.post(LINE_URL, data=context_json, headers={'Content-Type': 'application/json'})
        r = requests.post(LINE_URL, data=json.dumps(context), headers={
            'Content-Type': 'application/json'})

    def getSheet() -> None:
        pass

    def sendSheet(key: str, event: str, context: dict) -> None:
        pass
