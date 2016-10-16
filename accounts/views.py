from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
#from django.shortcuts import render
#from models import *

#---------------------------------------------------
def signup(request):
    context = {
#        'latest_question_list': latest_question_list,
    }
    return render(request, 'accounts/signup.html', context)


def signup_request(request):
	context = {
#		''
	}
	return render(request, 'accounts/signup_success.html', context)
