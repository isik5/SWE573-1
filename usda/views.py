from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from nutritrack.pagebuilder import *
from accounts.models import UserInfo, Sport

#from django.shortcuts import render
from models import USDA, Food, FCD
from usda.add_items import PhysicalActivity
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
def activitysearch(request):
	context = {
		'username' : request.user.username,
	}
	if (request.user.is_authenticated):
		return render_with_master(request, context, 'usda/activity.html')
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
		return render_with_master(request, context, 'usda/search.html')
	else:
		return redirect('accounts:signup')


#---------------------------------------------------
def searchactivityrequest(request):
	context = {
		'username' : request.user.username,
	}
	if (request.user.is_authenticated):
		objects = []
		try:
			objects = PhysicalActivity.objects.filter(name__regex=request.POST['fname'])
			context['objects'] = objects
			context['results_size'] = len(objects)
		except KeyError:
			print('Exception')
		return render_with_master(request, context, 'usda/activity.html')
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


def activity_details(request):
	if (request.user.is_authenticated):
		objects = []
		try:
			context = {
				'username' : request.user.username,
			}
			objects = PhysicalActivity.objects.filter(id=request.GET['ndbno'])[0]
			context['object'] = objects
		except KeyError:
			print('Exception')
		return render_with_master(request, context, 'usda/activity_details.html')
	else:
		return redirect('accounts:signup')


def activity_apply(request):
	if (request.user.is_authenticated):
		objects = []
		us = UserInfo.objects.filter(user=request.user)[0]
		try:
			hours = float(request.POST['hours']);
			objects = PhysicalActivity.objects.filter(id=request.POST['activity'])[0]
			cal = 45.83 / 100 * 2.2 * us.weightInKg * objects.METS * hours

			Sport(cals=cal, hours=hours, activity=objects, user=request.user).save()
			
			context = {
				'username' : request.user.username,
				'message' : 'Sport saved. (' + str(cal) + " calories)",
			}
			context['object'] = objects
		except KeyError:
			print('Exception')
		return render_with_master(request, context, 'usda/activity_details.html')
	else:
		return redirect('accounts:signup')