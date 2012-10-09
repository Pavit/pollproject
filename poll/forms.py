from poll.models import * # Change as necessary
from django.forms import ModelForm
from django import forms
from captcha.fields import ReCaptchaField
from tagging_autocomplete_tagit.widgets import TagAutocompleteTagIt
class PollForm(ModelForm):
	title= forms.CharField(label = "", required = False)
	captcha = ReCaptchaField(attrs = {'theme': 'white'})
	
	class Meta:
		model = Poll
		exclude = ("is_published", "date", "customuser",)

class ItemForm(ModelForm):
	value = forms.CharField(label = "")
	
	class Meta:
		model = Item
		exclude = ('poll', 'pos',"selected_by", "pick")

