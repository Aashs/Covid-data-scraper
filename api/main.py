import json
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.get("/")
def dashboard():
  with open("cases_storage.json") as f:
    data = json.load(f)
    newTime = time.time()
    lastUpdate = round((newTime - float(data['lastScrapped']['lastUpdateTime']))/60)
    return {
      f'data last updated {lastUpdate} minute ago, code can be found here https://github.com/Aashs/Covid-data-scraper and for documentation about requesting data https://covid19data.tk/docs.'
    }


@app.get("/countries/{countryName}")
def get_country(countryName: str):
    try:
        with open("cases_storage.json") as f:
            data = json.load(f)
            return {
                "cases": data["countries"][countryName]["cases"],
                "deaths": data["countries"][countryName]["deaths"],
                "recovers": data["countries"][countryName]["recovers"]
            }
    except KeyError:
      try:
        country_upper=countryName.title()
        return{"cases": data["countries"][country_upper]["cases"],
                "deaths": data["countries"][country_upper]["deaths"],
                "recovers": data["countries"][country_upper]["recovers"]}
      except KeyError:  
        return 'Key Error'    


@app.get("/total")
def all_country_total(request: Request):
    with open("cases_storage.json") as f:
        data = json.load(f)
        return {
            "cases": data["TOTAL"]["cases"],
            "deaths": data["TOTAL"]["deaths"],
            "recovers": data["TOTAL"]["recovers"]
        }

        
def run():
  print(f"Server Thread is running...")
  uvicorn.run(app, host='0.0.0.0', port=8080)


covid19data().start()
