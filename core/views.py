from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from datetime import date, datetime
from social_auth import __version__ as version
from social_auth.utils import setting
from poll.models import Poll, Item
from pprint import pprint
from social_auth.models import UserSocialAuth
from core.models import CustomUser
from facepy import GraphAPI
from django.db.models import Q
from django.conf import settings

def landing(request):
	if request.user.is_authenticated():
		uservalues = CustomUser.objects.values('name', 'fb_id')
		print request.user
		newuser, created = CustomUser.objects.get_or_create(username = request.user.username,fb_id = request.user.social_auth.get(provider='facebook').extra_data["id"],)
		newuser.fb_access_token = request.user.social_auth.get(provider='facebook').extra_data["access_token"]
		if created == True:
			newuser.populate_graph_info()
		graph = GraphAPI(newuser.fb_access_token)
		graphinfo = graph.get('me/')
		graphinfo["access_token"] = newuser.fb_access_token
		print newuser.birthday
		userdob = date(day=newuser.birthday.day, month = newuser.birthday.month, year =  newuser.birthday.year) #Lazy - should just make birthday a DateField
		if date.today().day > userdob.day:
			if date.today().month > userdob.month:
				age = date.today().year - userdob.year
			else:
				age = date.today().year - userdob.year - 1
		#newuser.age = age
		newuser.check_friends()
		try:
			nextpoll = Poll.objects.filter(~Q(answered_by = newuser))[:1].get()
			nextitems = Item.objects.filter(poll = nextpoll)
		except:
			return redirect('profile')
		return redirect('poll/polls')
		#return render_to_response("poll/result.html", {
			#'nextpoll':nextpoll,
			#'nextitems': nextitems,
			#'graphinfo':graphinfo,
			#}, context_instance=RequestContext(request))
	else:
		print request
		return render_to_response("landing.html")

@login_required
def profile(request):
	user = CustomUser.objects.get(username = request.user.username)
	user.populate_graph_info()
	user.save()
	print user.birthday
	uservotes = user.vote_set.all()
	print uservotes
	pollcount = Poll.objects.all().count()
	print "questions you submit:"
	print user.submissions.all()
	print "questions you answered:"
	print user.answered.all()
	for p in Poll.objects.all():
		print p.tags
	return render_to_response("profile.html", {'user': user, 'pollcount':pollcount,'APP_ID': settings.FACEBOOK_APP_ID}, context_instance = RequestContext(request))


		
@login_required
def done(request):
	graphinfo = GraphAPI(request.user.fb_access_token).get('me/')
	print graphinfo
	"""Login complete view, displays user data"""
	ctx = {
		'version': version,
		'last_login': request.session.get('social_auth_last_login_backend'),
		'graphinfo': graphinfo,
		}
	return render_to_response('poll/polls.html', ctx, RequestContext(request))


def error(request):
	"""Error view"""
	messages = get_messages(request)
	return render_to_response('error.html', {'version': version,
	'messages': messages},
	RequestContext(request))


def logout(request):
	"""Logs out user"""
	auth_logout(request)
	return redirect('landing')


def form(request):
	if request.method == 'POST' and request.POST.get('username'):
		name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
		request.session['saved_username'] = request.POST['username']
		backend = request.session[name]['backend']
		return redirect('socialauth_complete', backend=backend)
	return render_to_response('form.html', {}, RequestContext(request))


def form2(request):
	if request.method == 'POST' and request.POST.get('first_name'):
		request.session['saved_first_name'] = request.POST['first_name']
		name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
		backend = request.session[name]['backend']
		return redirect('socialauth_complete', backend=backend)
	return render_to_response('form2.html', {}, RequestContext(request))