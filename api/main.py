import json
from fastapi import FastAPI, Request
from typing import Optional
from fastapi.responses import FileResponse

cases_storage = "D:\Coding\Python\Covid-Tracker\cases_storage.json"
app = FastAPI()


@app.get("/countries/{countryName}")
def main(countryName: str):
    with open(cases_storage) as f:
        data = json.load(f)
        return {"cases": data["countries"][countryName]["cases"], "deaths": data["countries"][countryName]["deaths"], "recovers": data["countries"][countryName]["recovers"]}


@app.get("/total")
def main(request: Request):
    with open(cases_storage) as f:
        data = json.load(f)
        return{"cases": data["TOTAL"]["cases"], "deaths": data["TOTAL"]["deaths"], "recovers": data["TOTAL"]["recovers"]}
