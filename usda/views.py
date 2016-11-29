from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from nutritrack.pagebuilder import *

#from django.shortcuts import render
from models import USDA


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
