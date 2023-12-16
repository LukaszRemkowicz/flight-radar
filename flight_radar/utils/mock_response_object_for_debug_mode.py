import json


def get_response() -> dict:
    with open("response.json", "w", encoding="utf-8") as f:
        return json.loads(f.read())


async def save_response(response: dict) -> None:
    with open("response.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(response))
