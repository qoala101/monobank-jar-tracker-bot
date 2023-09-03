import httpx


def GetShortIdFromJarUri(jar_uri: str) -> str:
    uri_parts = jar_uri.split("/")
    return uri_parts[-1]


def FetchLongJarId(short_jar_id: str) -> str:
    request_json = {
        "c": "hello",
        "clientId": short_jar_id,
        "Pc": "0",
    }
    response = httpx.post(url="https://send.monobank.ua/api/handler", json=request_json)
    response_json = response.json()
    return response_json["extJarId"]


def FetchJarAmount(long_jar_id) -> int:
    response = httpx.get(url=f"https://api.monobank.ua/bank/jar/{long_jar_id}")
    response_json = response.json()
    return int(response_json["amount"])
