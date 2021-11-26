from bs4 import BeautifulSoup
import time
import requests
import json

with open('config.json') as f:
    data = json.load(f)

"""Getting data on what to scrape"""


def get_cases(link):
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


def all_countrys():
    source = requests.get(
        "https://www.worldometers.info/coronavirus/#countries")
    soup = BeautifulSoup(source.text, "lxml")
    countries = {country.text: {}
                 for country in soup.find_all('a', class_='mt_a')}
    with open("cases_storage.json", "w") as f:
        json.dump({"countries": countries}, f, indent=4)
# all_countrys()


'''Loads cases in json'''


def all_countrys_cases():
    while True:
        with open("cases_storage.json") as f:
            link = f"https://www.worldometers.info/coronavirus/"
            cases, deaths, recover = get_cases(link)
            data = json.load(f)
            data["TOTAL"]["cases"] = cases
            data["TOTAL"]["deaths"] = deaths
            data["TOTAL"]["recovers"] = recover
            cases_2 = cases
            deaths_2 = deaths
            recover_2 = recover
            if start_increase == True:
                data["TOTAL"]["increase-today"]["cases"] = cases_2-cases

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
                cases, deaths, recover = get_cases(link)
                with open('cases_storage.json') as f:
                    data = json.load(f)
                    data['countries'][countries_req]['cases'] = cases
                    data['countries'][countries_req]['deaths'] = deaths
                    data['countries'][countries_req]['recovers'] = recover

                with open('cases_storage.json', "w") as f:
                    json.dump(data, f, indent=3)

            except AttributeError:
                print(f"No span found for {countries_req}")
        time.sleep(10)
        start_increase = True


all_countrys_cases()
