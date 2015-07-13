from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	context_dict = {'boldmessage':"hello from strong bold message lol"}
	return render(request, 'rango/index.html',context_dict)
