from django.db import models
from django.contrib.auth.models import User

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
