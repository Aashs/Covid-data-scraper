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
      f'data last updated {lastUpdate} minute ago, a nice dashboard will be here soon....'
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
        return {"Key error"}


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
Thread(target=run).start()