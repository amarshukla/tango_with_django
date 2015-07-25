from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def main(request):
    logout(request)
    request.session.set_test_cookie()
    return render(request, 'rango/main.html')

def do_login(request):
    if request.method == 'POST':
        username = request.POST.get('log')
        password = request.POST.get('pwd')
        user = authenticate(username = username, password = password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango')
            else:
                return HttpResponse('your account is disabled')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse('Invalid login details provided, please re-check.')
    else:
        return render(request, 'rango/main.html', {})
def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
    #return HttpResponseRedirect('http://127.0.0.1:8000/')
    return render(request, 'http://127.0.0.1:8000/')


@login_required
def index(request):
    
    if not request.user.is_authenticated():
        return render(request, 'rango/main.html')

    most_viewed_pages={'pages':[]}
    cat = Category.objects.all()
    most_viewed_pages['pages'].append(Page.objects.filter(category__in=cat).order_by('-views')[:5])
    cat_dict = {'categories': Category.objects.order_by('-likes')[:5], 'boldmessage':"hello from strong bold message lol",'name':'amarshukla'}
    cat_dict.update(most_viewed_pages)
    return render(request, 'rango/index.html',cat_dict)

def category(request, category_name_slug):
	try:

		context_dict={}
		
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		context_dict['category_name_slug'] = category_name_slug
		pages = Page.objects.filter(category=category).order_by('-views')[:5]
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)

def hey(request, name):
	name = {'name':name}
	return render(request, 'rango/test.html',name)

def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors()
	else:
		form = CategoryForm()
		cat_list = Category.objects.all()
	return render(request, 'rango/add_category.html',{'form':form,'category':cat_list})

def add_page(request, category_name_slug):
	try:
		cat_list = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat_list = None
	context_dict = {}
	context_dict['cat_list'] = cat_list
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			page = form.save(commit=False)
			try:
				cat = Category.objects.get(name=category_name_slug)
				page.category = cat
			except Category.DoesNotExist:
				return render_to_response( 'rango/add_page.html',
                                          context_dict,
                                          context)
			page.views = 0
			page.save()
			return category(request, category_name_slug)
		else:
			print form.errors()
	else:
		form = PageForm()
	context_dict['category_name_url']= category_name_slug
	context_dict['category_name'] =  category_name_slug
	context_dict['form'] = form
	return render(request, 'rango/add_page.html', context_dict)

def register(request):

    if request.session.set_test_cookie_worked():
        print "SET cookie worked"
        request.session.delete_test_cookie()
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def listUsers(request):
	users = UserProfile.objects.all()
	return render(request, 'rango/listUsers.html',{'users':users})

def userDetail(request):
	user_name = request.GET.getlist('username')   #to get username parameter value from http url. 
	for i in user_name:
		user_name = i
	user_detail = UserProfile.objects.get(user__username__iexact=user_name)
	print 'amar',user_name
	return render(request, 'rango/userDetail.html',{'detail':user_detail})