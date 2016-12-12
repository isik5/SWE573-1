from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from nutritrack.pagebuilder import *

#from django.shortcuts import render
from models import USDA, Food, FCD
from accounts.models import Consumation


#---------------------------------------------------
def foodsearch(request):
	context = {
		'username' : request.user.username,
	}
	if (request.user.is_authenticated):
		return render_with_master(request, context, 'usda/search.html')
	else:
		return redirect('accounts:signup')

#---------------------------------------------------
def searchrequest(request):
	context = {
		'username' : request.user.username,
	}
	if (request.user.is_authenticated):
		u = USDA()
		objects = []
		try:
			objects = u.search_by_name(request.POST['fname'])
			context['objects'] = objects
			context['results_size'] = len(objects)
		except KeyError:
			print('Exception')
		print (context)
		return render_with_master(request, context, 'usda/search.html')
	else:
		return redirect('accounts:signup')


def render_details(request, context):
	if (request.user.is_authenticated):
		return render_with_master(request, context, 'usda/details.html')
	else:
		return redirect('accounts:signup')

def details(request):
	context = {
			'username' : request.user.username,
	}
	u = USDA()
	f = FCD()
	result = Food.objects.filter(ndbno=request.GET['ndbno'])[0]
	context['food'] = result
	context['nutrients'] = f.get_nutrients(result.ndbno)
	context['measures'] = f.get_measures(result.ndbno)

	return render_details(request, context);


def	eat(request):
	ndbno = request.POST['ndbno']
	unit = request.POST['unit']
	value = request.POST['fname']
	context = {
			'username' : request.user.username,
			'message' : 'Food saved.',
	}
	u = USDA()
	f = FCD()
	result = Food.objects.filter(ndbno=ndbno)[0]
	context['food'] = result
	context['nutrients'] = f.get_nutrients(result.ndbno)
	context['measures'] = f.get_measures(result.ndbno)

	c = Consumation(food=result, user=request.user, unit=unit, amount=value)
	c.save()
	
	return render_details(request, context);


