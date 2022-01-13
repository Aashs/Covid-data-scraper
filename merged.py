"""We use this script for hosting it in replit"""
import json, time, requests, uvicorn
from fastapi import FastAPI, Request
from threading import *
from bs4 import BeautifulSoup


"""Getting data on what to scrape"""
class covid19data(Thread):

    def get_cases(self, link):
        s = time.time()
        req = requests.get(link)
        if req.status_code == 200:
            s = time.time()
            str_content = bytes.decode(req.content)
            ind = str_content.lower().find('<div class="maincounter-number"')
            cases = str_content[ind:ind + 100]
            cases = BeautifulSoup(cases, "lxml")
            str_content = str_content[ind + 100:]
            ind = str_content.lower().find('<div class="maincounter-number"')
            deaths = str_content[ind:ind + 100]
            deaths = BeautifulSoup(deaths, "lxml")
            str_content = str_content[ind + 100:]
            ind = str_content.lower().find('<div class="maincounter-number"')
            recover = str_content[ind:ind + 100]
            recover = BeautifulSoup(recover, "lxml")
            cases = cases.span.string
            deaths = deaths.span.string
            recover = recover.span.string
            return (cases, deaths, recover)

    '''Gets all countrys loaded in json'''

    def all_countrys(self):
        source = requests.get(
            "https://www.worldometers.info/coronavirus/#countries")
        soup = BeautifulSoup(source.text, "lxml")
        countries = {country.text: {}
                    for country in soup.find_all('a', class_='mt_a')}
        with open("cases_storage.json", "w") as f:
            json.dump({"countries": countries}, f, indent=4)
    #all_countrys()

    '''Loads cases in json'''

    def run(self):
        print("Thread is running")
        while True:
            print('Loading data')
            with open("cases_storage.json") as f:
                link = f"https://www.worldometers.info/coronavirus/"
                cases, deaths, recover = self.get_cases(link)
                data = json.load(f)
                data["TOTAL"]["cases"] = cases
                data["TOTAL"]["deaths"] = deaths
                data["TOTAL"]["recovers"] = recover
                cases_2 = cases
                deaths_2 = deaths
                recover_2 = recover

            with open('cases_storage.json', "w") as f:
                json.dump(data, f, indent=3)

            with open("cases_storage.json") as f:
                data = json.load(f)
                country_list = []
                for check in data['countries']:
                    country_list.append(check)

            for countries_req in country_list:
                link = f"https://www.worldometers.info/coronavirus/country/{countries_req}"

                try:
                    cases, deaths, recover = self.get_cases(link)
                    with open('cases_storage.json') as f:
                        data = json.load(f)
                        data['countries'][countries_req]['cases'] = cases
                        data['countries'][countries_req]['deaths'] = deaths
                        data['countries'][countries_req]['recovers'] = recover

                    with open('cases_storage.json', "w") as f:
                        json.dump(data, f, indent=3)

                except AttributeError:
                    print(f"No span found for {countries_req}")
            
            with open('cases_storage.json') as f:
                data = json.load(f)
                data['lastScrapped']['lastUpdateTime'] = time.time()

            with open('cases_storage.json', "w") as f:
                json.dump(data, f, indent=3)

            print('Sleeping started')
            time.sleep(2400)    

"""-------------------------------API Server-----------------------------------------"""
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
        country_upper=countryName.title()
        return{"cases": data["countries"][country_upper]["cases"],
                "deaths": data["countries"][country_upper]["deaths"],
                "recovers": data["countries"][country_upper]["recovers"]}


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