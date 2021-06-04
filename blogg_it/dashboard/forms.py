from django import forms 
from .models import Posts, Threads

class PostForm(forms.ModelForm):
	class Meta:
		model = Posts
		fields = ['heading','description'] 