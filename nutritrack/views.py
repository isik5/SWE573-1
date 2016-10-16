from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from nutritrack.pagebuilder import *

#from django.shortcuts import render
#from models import *


#---------------------------------------------------
def index(request):
	context = {
		'username' : request.user.username,
	}
	if (request.user.is_authenticated):
		return render_with_master(request, context, 'nutritrack/index.html')
	else:
		return render_with_master(request, context, 'nutritrack/welcome.html')
