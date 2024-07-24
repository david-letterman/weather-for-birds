from flask import Flask, jsonify, Response

import requests
import sqlite3

app = Flask(__name__)


@app.get("/")
def index() -> object:
    return (
        "Choose a state to learn about birds and the weather "
        "challenges they face.",
        200,
        {"content-type": "text/html; charset=utf-8"},
    )


def get_bird_data(state: str) -> object:
    conn = sqlite3.connect("birds.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(f"select * from birds where abbreviation = '{state}';")
    row = cursor.execute(f"select * from birds where abbreviation = '{state}';")
    res = row.fetchall()
    list_accumulator = []
    for item in res:
        print(item)
        list_accumulator.append({k: item[k] for k in item.keys()})
    return list_accumulator


def get_weather_data(state: str) -> object:
    r = requests.get(f"https://api.weather.gov/alerts/active?area={state}")
    return r.json()


@app.get("/<string:state>")
def bird(state: str) -> Response:
    bird_data = get_bird_data(state)
    weather_data = get_weather_data(state)
    return jsonify(
        {
            "bird": bird_data,
            "weather": weather_data,
        }
    )
