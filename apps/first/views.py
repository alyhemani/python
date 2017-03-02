from django.shortcuts import render, redirect
from django.contrib import messages
import re
import bcrypt
import datetime
from models import *
EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATE_REGEX =  re.compile(r'^(19|20)\d\d[\-\/.](0[1-9]|1[012])[\-\/.](0[1-9]|[12][0-9]|3[01])$')
today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)


# Create your views here.
def index(request):
	return render(request, 'first/index.html')

def register(request):
	if len(request.POST.get('name'))<2:
		messages.warning(request, 'Please Enter Valid Name')
		return redirect('/')
	elif len(request.POST.get('alias'))<1:
		messages.warning(request, 'Please Enter Valid Alias')
		return redirect('/')
	elif len(request.POST.get('email'))<1:
		messages.warning(request, 'Please Enter Valid Email')
		return redirect('/')
	elif len(request.POST.get('password'))<7:
		messages.warning(request, 'Please Enter Valid Password')
		return redirect('/')
	elif len(request.POST.get('confirm'))<1:
		messages.warning(request, 'Must Enter Valid Password Confirmation')
		return redirect('/')
	elif request.POST.get('password') != request.POST.get('confirm'):
		messages.warning(request, 'Password and Password Confirmation Must Match')
		return redirect('/')
	elif not EMAIL_REGEX.match(request.POST.get('email')):
		messages.warning(request, 'Please enter the Email in valid form')
		return redirect('/')
	elif not DATE_REGEX.match(request.POST.get('dob')):
		messages.warning(request, 'Please enter valid Date of Birth')
		return redirect('/')
	elif request.POST.get('dob')>unicode(today_min):
		messages.warning(request, 'Please enter valid Date of Birth')
		return redirect('/')
	else:
		user = User.objects.create(
			name = request.POST.get('name'),
			alias = request.POST.get('alias'),
			email = request.POST.get('email'),
			password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt()),
			dob = request.POST.get('dob')
			)
		request.session['user_id']=user.id		
		return redirect('/main')

def login(request):
	login = User.objects.login(request.POST)
	if login[0]:
		request.session['user_id'] = login[1].id
		return redirect('/main')
	else:
		messages.warning(request, 'No Matching User. Please Register or Enter Accurate Information')
		return redirect('/')


def main(request):
	favorited = []
	favs = Favorite.objects.filter(added_by= request.session['user_id'])
	for fav in favs:
		favorited.append(fav.quote_id.id)
	context = {
	'user': User.objects.filter(id=request.session['user_id']),
	'quotable': Quote.objects.exclude(id__in=favorited),
	'favorite': Favorite.objects.filter(added_by= request.session['user_id'])
	}
	return render(request, 'first/main.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')

def add(request):
	if len(request.POST.get('author'))<3:
		messages.warning(request, 'Please Enter Valid Author')
	elif len(request.POST.get('quote'))<10:
		messages.warning(request, 'Please Enter Valid Quote')
	else:
		Quote.objects.create(
			quote=request.POST.get('quote'),
			author= request.POST.get('author'),
			creator = User.objects.get(id=request.session['user_id']),
			)
		print request.POST.get('quote')
		print request.POST.get('author')
		print User.objects.get(id=request.session['user_id'])
	return redirect('/main')

def users(request, id):
	context = {
	'user': Quote.objects.filter(creator = id).first(),
	'count': len(Quote.objects.filter(creator = id)),
	'quotes': Quote.objects.filter(creator = id),
	}
	return render(request, 'first/users.html', context)

def favorite(request, id):
	Favorite.objects.create(
		added_by=User.objects.get(id=request.session['user_id']),
		quote_id= Quote.objects.get(id = id))
	return redirect('/main')

def remove(request, id):
	Favorite.objects.filter(id=id).delete()
	return redirect('/main')









