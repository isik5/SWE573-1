from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
#from models import *

#---------------------------------------------------
def signup(request):
    context = {
#        'latest_question_list': latest_question_list,
    }
    return render(request, 'accounts/signup.html', context)

#---------------------------------------------------
def signin(request):
    context = {
    }
    return render(request, 'accounts/signin.html', context)


#---------------------------------------------------
def signin_request(request):
	context = {
	}
	username = request.POST['user']
	password = request.POST['pass']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('nutritrack:index'))
	else:
		return render(request, 'accounts/signin_failed.html', context)

#---------------------------------------------------
def signup_request(request):
	context = {
#		''
	}
	username = request.POST['user']
	password = request.POST['pass']
	mail	 = request.POST['mail']
	user = User.objects.create_user(username, mail, password)

	return render(request, 'accounts/signup_success.html', context)
