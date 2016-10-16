from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
#from django.shortcuts import render
#from models import *


#---------------------------------------------------
def index(request):
    context = {
#        'latest_question_list': latest_question_list,
    }
    return render(request, 'nutritrack/index.html', context)
