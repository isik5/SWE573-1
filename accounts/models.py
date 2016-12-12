from django.db import models
from django.contrib.auth.models import User
from usda.models import Food
from usda.add_items import *

# Create your models here.

class Gender(object):
	Male	= 0
	Female	= 1
	NA	= 2


class UserInfo(models.Model):
	user		  = models.ForeignKey(User)
	registration_date = models.DateTimeField(auto_now_add=True, help_text='The date of the registration')
	birth_date        = models.DateTimeField(auto_now_add=True, help_text='The date of birth')
	gender		  = models.IntegerField(default=0)
	weightInKg	  = models.IntegerField(default=70)
	heightInCm	  = models.IntegerField(default=180)

	def __str__(self):
		return "Info (" + self.user.username + ")"

class Consumation(models.Model):
	user  = models.ForeignKey(User)
	food  = models.ForeignKey(Food)
	date  = models.DateTimeField(auto_now_add=True, help_text='Consumation date')
	amount = models.FloatField(default=0)
	unit = models.CharField(max_length=50)
	def __str__(self):
		return "Consumation (" + self.user.username + " " + self.date.strftime('%Y-%m-%d %H:%M') + ", " + str(self.amount) + " " + self.unit + ")"

class Sport(models.Model):
	user  = models.ForeignKey(User)
	date  = models.DateTimeField(auto_now_add=True, help_text='Consumation date')
	cals  = models.IntegerField(default=0)
	activity = models.ForeignKey(PhysicalActivity)
	hours = models.FloatField(default=0)
	def __str__(self):
		return "Sport (" + self.activity.name + " " + str(self.hours) + " hours)"


