import lxml
import time
import requests
from bs4 import BeautifulSoup


def main(link):
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


def total_cases():
    link = f"https://www.worldometers.info/coronavirus/"
    cases, deaths, recover = main(link)
    f = open("covid.txt", "a")
    f.write(
        f"\nTotal\ncases: {cases}\ndeaths: {deaths}\nrecover: {recover}")
    f.close()
    print(f"cases: {cases}\ndeaths: {deaths} \nrecover: {recover}")


total_cases()

"""Cases by searching country"""


def country_search(country):
    link = f"https://www.worldometers.info/coronavirus/country/{country}"
    try:
        cases, deaths, recover = main(link)
        print(f"cases: {cases}\ndeaths: {deaths} \nrecover: {recover}")
    except KeyError:
        raise ValueError(f"There is no country called {country}")


country_search('russia')
