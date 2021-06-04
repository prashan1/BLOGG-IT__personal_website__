from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView,DeleteView,UpdateView,FormView
from django.views.generic.detail import DetailView
from .forms import UserDiscription
# Create your views here.
class Register(FormView):
	form_class = UserCreationForm
	template_name = 'user/register.html'
	success_url = reverse_lazy('login')

	def form_valid(self,form):
		form.save()
		return super(Register,self).form_valid(form)

	def get(self,*args,**kwargs):
		if self.request.user.is_authenticated:
			return redirect('home')
		return super(Register,self).get(*args,**kwargs)

class Login(LoginView):
	template_name = 'user/login.html'

	def get(self,*args,**kwargs):
		if self.request.user.is_authenticated:
			return redirect('home')
		return super(Login,self).get(*args,**kwargs)
