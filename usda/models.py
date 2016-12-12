from __future__ import unicode_literals
from django.db import transaction
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
		return self.query_string

#--------------------------------------------------------------
class Search_entry(models.Model):
	food = models.ForeignKey(Food, on_delete=models.CASCADE)
	query = models.ForeignKey(Search_query, on_delete=models.CASCADE)

#--------------------------------------------------------------
def create_food_from_json(json):
	object = Food()
	object.name = json['name']
	object.category = json['group']
	object.ndbno = json['ndbno']
	return object

#--------------------------------------------------------------
food_to_save = []
def get_food_from_json(json):
	results = Food.objects.filter(ndbno=json['ndbno'])
	if (len(results) == 0):
		obj = create_food_from_json(json)
		food_to_save.append(obj)
		return obj
	else:
		return results[0]

#-------------------------------------------------------------
@transaction.atomic
def save_foods():
	for item in food_to_save:
		item.save()

#--------------------------------------------------------------

@transaction.atomic
def register_for_queries(objects, name):
	object = Search_query()
	object.query_string = name
	object.save()
	length = len(objects)
	result_objects = []
	for i in range(0, length):
		entry = Search_entry()
		entry.query = object
		no = objects[i]['ndbno']
		entry.food = Food.objects.filter(ndbno=no)[0]
		entry.save()
		result_objects.append(entry)
	return result_objects

#This class serves as the main interface for interacting with USDA api.
#--------------------------------------------------------------
class USDA:
	api_key='No0xRSnThHjjaSlDTSWz41dyVn8dkvaJkw6TQxvO'
	def get_search_url(self, food_name):
		return 'http://api.nal.usda.gov/ndb/search/?format=json&q=' + food_name + '&max=100&offset=0&api_key=' + self.api_key
	def search_by_name(self, name):
		result = Search_query.objects.filter(query_string=name)
		objects = []
		if (len(result) != 0):
			objects = result[0].search_entry_set.all()
		else:
			url = self.get_search_url(name)
			jsonobj = requests.get(url).json()
			json_response = jsonobj['list']['item']
			length = len(json_response)
			for i in range(0, length):
				get_food_from_json(json_response[i])
			save_foods()
			objects = register_for_queries(json_response, name)
		print('No exception')
		print (len(objects))
		return objects






