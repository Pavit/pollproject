# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.db import transaction
from django.utils import simplejson
#from utils import set_cookie
from poll.models import *
from django.db.models import Q
from core.models import CustomUser
from poll.forms import *
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

def vote(request, poll_pk):
	try:
		poll = Poll.objects.get(pk=poll_pk)
		print poll
	except:
		return HttpResponse('Wrong parameters', status=400)
	item_pk = request.POST.get("item", False)
	print item_pk
	if not item_pk:
		return HttpResponse('Wrong parameters', status=400)
	try:
		item = Item.objects.get(pk=item_pk)
	except:
		return HttpResponse('Wrong parameters', status=400)


	print "made it to last part of vote method"
	vote = Vote.objects.create(
		poll=poll,
		ip=request.META['REMOTE_ADDR'],
		#user=CustomUser.objects.get(username = request.user.username),
		item=item,
	)
	user = request.user
	print type(user)
	print type(request.user)
	if request.user.is_authenticated():
		grabuser = CustomUser.objects.get(username = request.user.username)
	else:
		grabuser = CustomUser.objects.filter(first_name = 'Anonymous')[:1].get()
		
	vote.customusers.add(grabuser)
	voteditem = vote.item
	voteditem.selected_by.add(grabuser)
	grabuser.save()
	poll.answered_by.add(grabuser)
	poll.save()
	vote.save()
	try:
		nextpoll = Poll.objects.filter(~Q(answered_by = grabuser))[:1].get()
		nextitems = Item.objects.filter(poll=nextpoll)
	except:
		print "except"
		if request.user.is_authenticated():
			return redirect('profile')
		else:
			return HttpResponse('Anonymous User, you have answered all questions! Sign up to submit new questions!', status=400)

	items = Item.objects.filter(poll=poll)
	print "polls answered:"
	return render_to_response("poll/result.html", {
		'poll': poll,
		'items': items,
		'nextpoll': nextpoll,
		'nextitems': nextitems,
		}, context_instance=RequestContext(request))

def polls(request, poll_pk=None):
	if poll_pk == None:
		print request.method
		if request.user.is_authenticated():
			user = CustomUser.objects.get(username = request.user.username)
			nextpoll = Poll.objects.filter(~Q(answered_by = user))[:1].get()
		else:
			user = CustomUser(first_name='Anonymous', last_name='User')
			user.save()
			nextpoll = Poll.objects.filter(~Q(answered_by = user))[:1].get()
	else:
		nextpoll = Poll.objects.get(id = poll_pk)
	return render_to_response("poll/polls.html", {
	'nextpoll':nextpoll,
	}, context_instance=RequestContext(request))
	
def poll(request, poll_pk):
	print request.method
	if request.user.is_authenticated():
		user = CustomUser.objects.get(username = request.user.username)
		nextpoll = Poll.objects.filter(~Q(answered_by = user))[:1].get()
	else:
		user = CustomUser(first_name='Anonymous', last_name='User')
		user.save()
		nextpoll = Poll.objects.filter(~Q(answered_by = user))[:1].get()
		print nextpoll
	return render_to_response("poll/polls.html", {
		'nextpoll':nextpoll,
		}, context_instance=RequestContext(request))


from random import randint

def skip(request, nextpoll_pk):
	skippedpoll_pk = nextpoll_pk
	if request.user.is_authenticated():
		user = CustomUser.objects.get(username = request.user.username)
		nextpoll = Poll.objects.filter(~Q(id=skippedpoll_pk)).filter(~Q(answered_by = user)).order_by('?')[:1].get()
	else:
		user = CustomUser.objects.filter(first_name = "Anonymous")[:1].get()
		nextpoll = Poll.objects.filter(~Q(id=skippedpoll_pk)).order_by('?')[:1].get()
	nextitems = Item.objects.filter(poll=nextpoll)
	return render_to_response("poll/result.html", {
		'nextpoll': nextpoll,
		'nextitems': nextitems,
		}, context_instance=RequestContext(request))
		
def result(request, poll_pk):
	print request.method
	if poll_pk:
		try:
			poll = Poll.objects.get(pk=poll_pk)
			getuser = CustomUser.objects.get(username = request.user.username)
			nextpoll = Poll.objects.filter(~Q(answered_by = grabuser))[:1].get()
			nextitems = Item.objects.filter(poll=nextpoll)
			items = Item.objects.filter(poll=poll)
			print nextpoll
		except:
			poll = None
			items = []
	else:
		poll = None
		items = []
		nextpoll = Poll.objects.all()[0]
		nextitems = Item.objects.filter(poll = nextpoll)
	return render_to_response("poll/result.html", {
		'poll': poll,
		'items': items,
		'nextpoll': nextpoll,
		'nextitems': nextitems,
		}, context_instance(RequestContext(request)))


from poll.forms import *
from django.core.context_processors import csrf
from django.template import RequestContext # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet

def addpoll(request):
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = False

	ItemFormSet = formset_factory(ItemForm, max_num=5, formset=RequiredFormSet)
	user = CustomUser.objects.get(username = request.user.username)
	if request.method == 'POST': # If the form has been submitted...
		getuser = CustomUser.objects.get(username = request.user.username)
		print "this poll should be assigned to: %s" %getuser
		poll_form = PollForm(request.POST) # A form bound to the POST data
		# Create a formset from the submitted data
		item_formset = ItemFormSet(request.POST, request.FILES)
		if poll_form.is_valid() and item_formset.is_valid():
			print "made it past valid check"
			poll = poll_form.save(commit=False)
			poll.submitter = getuser
			poll.save()
			#print poll.customuser.username
			for form in item_formset.forms:
				item = form.save(commit=False)
				item.poll = poll
				item.pos = 0
				item.save()
				print item
			
			return redirect('profile')
	else:
		poll_form = PollForm()
		item_formset = ItemFormSet()

	c = {'poll_form': poll_form,
	'item_formset': item_formset,
	'user': user,
	}
	c.update(csrf(request))

	return render_to_response('poll/addpoll.html', c)
