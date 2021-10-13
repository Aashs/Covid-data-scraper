import lxml
import time
import requests
from bs4 import BeautifulSoup

s = time.time()
req = requests.get("https://www.worldometers.info/coronavirus/")
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


    print(f"cases: {cases}\ndeaths: {deaths}\nrecover: {recover}")

else:
    print('error', req.status_code)
