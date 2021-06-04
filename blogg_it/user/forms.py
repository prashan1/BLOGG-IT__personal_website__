from django.contrib.auth.models import User
from django import forms

class UserDiscription(forms.ModelForm):
	email= forms.EmailField()

	class Meta:
		models = User
		fields = ['username','email']
