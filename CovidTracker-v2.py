import requests as r


class CountryNotFound(Exception):
	pass

class CovidClient:
	def __init__(self):
		self.country=""
		self.total_cases=""
		self.total_death=""
		self.total_recover=""
		self.total_tests=""
		self.active=""
		self.critical=""
		self.today_cases=""
		self.today_deaths=""
		
		
	def _data(self):
		"""Internal Function to load data"""
		s = r.get(f"https://corona.lmao.ninja/v3/covid-19/countries/{self.country}")
		try:
			s.json()['message']
			return False
		except KeyError:
			return s.json()
		
	def load_country(self,country:str):
		self.country=country
		d = self._data()
		if self._data() is False:
			raise CountryNotFound("No such Country Found!!")
			return False
		else:
			self.total_cases=d['cases']
			self.total_death=d['deaths']
			self.total_recover=d['recovered']
			self.total_tests=d['tests']
			self.active = d['active']
			self.critical = d['critical']
			self.today_deaths = d['todayDeaths']
			self.today_cases = d['todayCases']
			self.today_recover=d['todayRecovered']
			self.percent_cases=int(d['oneCasePerPeople'])/int(d['population'])*100
			self.percent_death=int(d['oneDeathPerPeople'])/int(d['population'])*100
			self.percent_test=int(d['oneTestPerPeople'])/int(d['population'])*100
			self.population=d['population']
			self.flag_url=d['countryInfo']['flag']
			self.country_id=d['countryInfo']['_id']
			return True
