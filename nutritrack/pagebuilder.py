from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.template.loader import render_to_string
#from models import *


#---------------------------------------------------
def get_navbar_buttons(request, context):
	if  (request.user.is_authenticated):
	     return render_to_string('nutritrack/navbar_user_buttons.html', context, request=request)
	else:
	     return render_to_string('nutritrack/navbar_stranger_buttons.html', context, request=request)

#---------------------------------------------------
def get_navbar(request, context):
	context['navbar_buttons'] = get_navbar_buttons(request, context)
        return render_to_string('nutritrack/navbar.html', context, request=request)

#---------------------------------------------------
def render_with_master(request, context, content_page):
        context['navbar'] = get_navbar(request, context);
        context['page_content'] = render_to_string(content_page, context, request=request)
        return render(request, 'nutritrack/master.html', context)


