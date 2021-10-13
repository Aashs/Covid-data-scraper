import request as r


class CountryNotFound(s):
	pass

class CovidClient:
	def __init__(self):
		self.country=""
		
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
		if self._data() is False:
			raise CountryNotFound("No such Country Found!!")
			return False
		else:
			return True
	
	
	def cases(self):
		data = self._data()
		active = data['active']
		critical = data['critical']
		total = data['cases']
		return {'total':total,'active':active,'critical':critical}
		
		
		
		
