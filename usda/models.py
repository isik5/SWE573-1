from __future__ import unicode_literals
from django.db import transaction
from django.db import models
from add_items import *
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
        return 'http://api.nal.usda.gov/ndb/search/?format=json&q=' + food_name + '&max=399&offset=0&api_key=' + self.api_key
    def search_by_name(self, name):
        result = Search_query.objects.filter(query_string=name)
        objects = []
        if (len(result) != 0 and False):
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


def get_activity_by_id(id):
    if (PhysicalActivity.objects.count == 0):
        add_items()
    return PhysicalActivity.objects.filter(id=id)[0]


class FCD(object):
    FORMAT = "json"
    API_KEY = "No0xRSnThHjjaSlDTSWz41dyVn8dkvaJkw6TQxvO"
    API_URL = "http://api.nal.usda.gov/ndb/{}/?format={}&api_key={}"
    def __init__(self):
        super(FCD, self).__init__()

    @staticmethod
    def get_url(command):
        return FCD.API_URL.format(command, FCD.FORMAT, FCD.API_KEY)
        
    @staticmethod
    def find(name):
        """
        searchs for the given food
        
        :return: returns a list of matching food objects 
        """
        base_url = FCD.get_url("search")
        url = base_url + "&q={}".format(name)
        json_response = requests.get(url).json()["list"]["item"]
        return json_response
    
    @staticmethod
    def get_report(ndbno):
        if (ndbno < 9999):
            ndbno = '0' + str(ndbno)
        base_url = FCD.get_url("reports")
        url = base_url + "&type=f&ndbno={}".format(ndbno)
        json_response = requests.get(url).json()["report"]
        return json_response

    @staticmethod
    def get_nutrients(ndbno):
        if (ndbno < 9999):
            ndbno = '0' + str(ndbno)
        report = FCD.get_report(ndbno)
        return report["food"]["nutrients"]
    
    @staticmethod
    def get_measures(ndbno):
        nutrients = FCD.get_nutrients(ndbno)
        return set(m["label"] for n in nutrients for m in n["measures"])

def calculate_consumption(ndbno, measure, quantity):
    f = FCD()
    nutrients = f.get_nutrients(ndbno)
    intake = []
    for nutrient in nutrients:
        for i_measure in nutrient["measures"] :
            if i_measure["label"] == measure and i_measure["value"] != 0 :
                intake.append({
                        "label": nutrient["name"], 
                        "unit": nutrient["unit"], 
                        "intake": float(i_measure["value"]) * quantity
                    })

    for item in intake:
        if item["unit"] == "kcal":
           return item["intake"]
    return 0