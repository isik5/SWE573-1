from __future__ import unicode_literals
from django.db import models
import requests

# These are models to cache 'search for nutrition'
#--------------------------------------------------------------
class Food(models.Model):
	ndbno    = models.IntegerField(default=0)
	name     = models.CharField(max_length=200)
	category = models.CharField(max_length=200)
	def __str__(self):
		return self.name

#--------------------------------------------------------------
class Nutrient(models.Model):
	name     = models.CharField(max_length=200)
	group    = models.CharField(max_length=200)
	def __str__(self):
		return self.name

#--------------------------------------------------------------
class Nutrient_ingredient(models.Model):
	nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
	food = models.ForeignKey(Food, on_delete=models.CASCADE)
	unit = models.CharField(max_length=50)
	amount = models.FloatField(default=0)
	def __str__(self):
		return self.nutrient + '(' + self.amount + '+' + self.unit + ')'

# These are models to cache 'search by name'
#--------------------------------------------------------------
class Search_query(models.Model):
	query_string = models.CharField(max_length=100)
	def __str__(self):
		return query_string

#--------------------------------------------------------------
class Search_entry(models.Model):
	food = models.ForeignKey(Food, on_delete=models.CASCADE)
	query = models.ForeignKey(Search_query, on_delete=models.CASCADE)


def create_food_from_json(json):
	object = Food()
	object.name = json['name']
	object.category = json['group']
	object.ndbno = json['ndbno']
	object.save()
	return object

def get_food_from_json(json):
	results = Food.objects.filter(ndbno=json['ndbno'])
	if (len(results) == 0):
		return create_food_from_json(json)
	else:
		return results[0]

#This class serves as the main interface for interacting with USDA api.
#--------------------------------------------------------------
class USDA:
	api_key='No0xRSnThHjjaSlDTSWz41dyVn8dkvaJkw6TQxvO'
	def get_search_url(self, food_name):
		return 'http://api.nal.usda.gov/ndb/search/?format=json&q=' + food_name + '&max=100&offset=0&api_key=' + self.api_key
	def search_by_name(self, name):
		result = Search_query.objects.filter(query_string=name)
		if (len(result) != 0):
			return result
		else:
			url = self.get_search_url(name)
			json_response = requests.get(url).json()['list']['item']
			length = len(json_response)
			if length == 0:
				return ''
			else:
				print(length)
				objects = []
				for i in range(0, length):
					objects.append(get_food_from_json(json_response[i]))
				return objects
