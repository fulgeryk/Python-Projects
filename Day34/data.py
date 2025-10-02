import requests

parameters= {
    "amount" : 10,
    "type" : "boolean"
}
response_api = requests.get(url="https://opentdb.com/api.php", params=parameters)
response_api.raise_for_status()
question_data = response_api.json()["results"]

