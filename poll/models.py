# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.utils.translation import gettext as _
from core.models import CustomUser
from django.db.models.manager import Manager
from django.core.exceptions import ValidationError
from tagging_autocomplete_tagit.models import TagAutocompleteTagItField


class PublishedManager(Manager):
	def get_query_set(self):
		return super(PublishedManager, self).get_query_set().filter(is_published=True)

class Poll(models.Model):
	title = models.CharField(max_length=250, verbose_name=_('question'))
	date = models.DateField(verbose_name=_('date'), default=datetime.date.today)
	is_published = models.BooleanField(default=True, verbose_name=_('is published'))
	submitter = models.ForeignKey(CustomUser, null=True, blank=True, default=None, related_name='submissions')
	answered_by = models.ManyToManyField(CustomUser, null=True, blank=True, default=None, related_name = 'answered')
	objects = models.Manager()
	published = PublishedManager()
	tags = TagAutocompleteTagItField(max_tags=False)
	
	class Meta:
		ordering = ['-date']
		verbose_name = _('poll')
		verbose_name_plural = _('polls')

	def __unicode__(self):
		return self.title

	def get_vote_count(self):
		return Vote.objects.filter(poll=self).count()
	vote_count = property(fget=get_vote_count)

    #def get_cookie_name(self):
        #return str('poll_%s' % (self.pk))


class Item(models.Model):
	poll = models.ForeignKey(Poll)
	value = models.CharField(max_length=250, verbose_name=_('value'))
	pos = models.SmallIntegerField(default='0', verbose_name=_('position'))
	selected_by = models.ManyToManyField(CustomUser, null=True, blank=True, default=None, related_name = 'selection')
	pick = models.BigIntegerField(default = '0')

	class Meta:
		verbose_name = _('answer')
		verbose_name_plural = _('answers')
		ordering = ['pos']

	def addvote(self):
		self.pick+=1
		self.save()
		return self
		
	def __unicode__(self):
		return u'%s' % (self.value,)

	def get_vote_count(self):
		return Vote.objects.filter(item=self).count()

	def get_vote_count_male(self):
		return self.selected_by.filter(gender="male").count()

	def get_vote_count_female(self):
		return self.selected_by.filter(gender="female").count()
		
	vote_count = property(fget=get_vote_count)
	vote_count_male = property(fget=get_vote_count_male)
	vote_count_female = property(fget=get_vote_count_female)

class Vote(models.Model):
	poll = models.ForeignKey(Poll, verbose_name=_('poll'))
	item = models.ForeignKey(Item, verbose_name=_('voted item'))
	ip = models.IPAddressField(verbose_name=_('user\'s IP'))
	customusers = models.ManyToManyField(CustomUser)
	datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('vote')
		verbose_name_plural = _('votes')

	def __unicode__(self):
		return u'%s' % (self.item.value,)

