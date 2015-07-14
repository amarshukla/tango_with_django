from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page

def index(request):
	
	cat_dict = {'categories': Category.objects.order_by('-likes')[:5], 'boldmessage':"hello from strong bold message lol"}
	return render(request, 'rango/index.html',cat_dict)

def category(request, category_name_slug):
	try:

		context_dict={}
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name

		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)
