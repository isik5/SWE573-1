from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.template.loader import render_to_string
#from models import *
from nutritrack.pagebuilder import *
from accounts.models import UserInfo, Gender
#---------------------------------------------------
#def get_navbar(request, context):
#	return render_to_string('nutritrack/navbar.html', context, request=request)

#---------------------------------------------------
#def render_with_master(request, context, content_page):
#	context['navbar'] = get_navbar(request, context);
#	context['page_content'] = render_to_string(content_page, context, request=request)
#	return render(request, 'nutritrack/master.html', context)

#---------------------------------------------------
def logout_(request):
 	logout(request)
	return HttpResponseRedirect(reverse('nutritrack:index'))

#---------------------------------------------------
def signup(request):
	return render_with_master(request, {
		'username': 'Stranger',
	}, 'accounts/signup.html');

#---------------------------------------------------
def signin(request):
	return render_with_master(request, {
		'username' : request.user.username,
	}, 'accounts/signin.html');

#---------------------------------------------------
def signin_request(request):
	username = request.POST['user']
	password = request.POST['pass']
	context = {
		'username' : username
	}
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return render_with_master(request, context, 'accounts/signup_success.html')
	else:
		return render_with_master(request, context, 'accounts/signin_failed.html')

#---------------------------------------------------
def signup_request(request):
	context = {
#		''
	}
	username = request.POST['user']
	password = request.POST['pass']
	mail	 = request.POST['mail']
	user = User.objects.create_user(username, mail, password)

	ur = UserInfo()
	ur.user = user
	if request.POST['gender'] is 'Male':
		ur.gender = Gender.Male
	else:
		ur.gender = Gender.Female
	ur.weightInKg = request.POST['weight']
	ur.heightInCm = request.POST['height']
	ur.save()
#        registration_date = models.DateTimeField(auto_now_add=True, help_text='The date of the registratio$
#        birth_date        = models.DateTimeField(auto_now_add=True, help_text='The date of birth')

	return render_with_master(request, {
		'username' : username,
	}, 'accounts/signup_success.html');

def settings(request):
	context = {
		'user' : request.user.userinfo_set.all()[0],
		'username': request.user.username,
	}

	return render_with_master(request, context, 'accounts/settings.html');

def change(request):
	
	us = request.user.userinfo_set.all()[0]
	us.weightInKg = request.POST["weight"]
	us.heightInCm = request.POST["height"]
	us.save()
	context = {
		'username' : request.user.username,
		'user' : request.user.userinfo_set.all()[0],
	}

	context['message'] = "Changes saved"

	return render_with_master(request, context, 'accounts/settings.html');
