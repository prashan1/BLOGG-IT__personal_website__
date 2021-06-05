from django.contrib.auth import login
from django.http.response import JsonResponse
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .models import Posts, Threads
from django.conf import settings
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic.list import ListView,MultipleObjectMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView,UpdateView,CreateView
from django.core.paginator import Paginator
import json
# Create your views here.
class HomeView(ListView):
	model = Threads
	template_name = 'dashboard/home.html'
	ordering=['-created_on']
	context_object_name = 'threads'
	paginate_by=5
qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
	def get_context_data(self,**kwargs):

		object_list = Threads.objects.all()
		context = super(HomeView,self).get_context_data(object_list=object_list,**kwargs)
	
		searched_data = self.request.GET.get('thread-name') or ''
		if len(searched_data)>0:
			newT = []
			for t in context['threads']:
				if t.title.startswith(searched_data) :
					newT.append( t)
			context['threads'] = newT


		context['thread_name']=searched_data

		context['latestPosts'] = Posts.objects.all().order_by('-created_on')[:5]
		context['creation'] = False
		return context

	
class PostDetailView(DetailView,MultipleObjectMixin):
	model = Threads
	template_name = 'dashboard/post_detail.html'
	paginate_by=5

	def get_context_data(self,**kwargs):
		# for pagination in deatilview using mulitpleobjectmixin
		object_list = Posts.objects.filter(belongs_to_thread=self.object)
		context = super(PostDetailView,self).get_context_data(object_list=object_list,**kwargs)
		#For right side bar
		context['latestPosts'] = Posts.objects.all().order_by('-created_on')[:5]
		context['threads'] = Threads.objects.all()
		# increasing view count of this thread
		thread = Threads.objects.filter(pk=self.kwargs['pk']).first()
		thread.total_views += 1 
		thread.save()
		context['curr_thread'] = thread
		context['creation']=False
		return context

class CreateNewThread(LoginRequiredMixin,CreateView):
	login_url = '/login/'
	model = Threads
	template_name = 'dashboard/create_thread.html'
	fields = ['title','description']

	def form_valid(self,form):
		form.instance.created_by=self.request.user
		return super().form_valid(form)
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['creation'] = True
		return context

class DeleteThread(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
	login_url = '/login/'
	model = Threads
	template_name = 'dashboard/delete_thread.html'
	fields = ['title','description']
	success_url = reverse_lazy('home')

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['threads'] = Threads.objects.all()
		return context

	def test_func(self):
		data = self.get_object()
		return self.request.user==data.created_by

@login_required()
def CreateNewPost(request,pk):

	if request.method=='POST':
		form = PostForm(request.POST)
		if form.is_valid():
			form.instance.created_by=request.user
			form.instance.belongs_to_thread_id = pk
			form.save()
			# increasing post count of this thread
			thread = Threads.objects.filter(pk=pk).first()
			thread.total_posts += 1
			thread.save()
			return redirect('post-detail',pk=pk)
	else:
		form = PostForm()
	return render(request,'dashboard/create_post.html',{'form':form,'pk':pk,'creation':True})


class InnerPostView(DetailView):
	model = Posts
	template_name = 'dashboard/innerPostView.html'

@login_required()
def DeleteInnerPost(request,pk):
	post = Posts.objects.get(pk=pk)

	if request.user != post.created_by:
		return redirect('home')
	return render(request,'dashboard/delete_post.html',{'post':post})

def DeleteConfirmed(request,pk):
	post = Posts.objects.get(pk=pk)
	curr_post = post.belongs_to_thread_id
	thread = Threads.objects.filter(pk=curr_post).first()
	thread.total_posts -= 1
	thread.save()
	post.delete()

	return redirect('post-detail',pk=curr_post)
@login_required()
def UpdateInnerPost(request,pk):
	post = Posts.objects.get(pk=pk)

	if(request.user != post.created_by):
		return redirect('home')

	if request.method == 'POST':
		form = PostForm(request.POST , instance=post)

		if form.is_valid():
			form.save()
			curr_post = post.belongs_to_thread_id
			return redirect('post-detail',pk=curr_post)
	else:
		form = PostForm(instance=post)
	return render(request,'dashboard/create_post.html',{'form':form})

def UpdateVote(request):
	data = json.loads(request.body)
	id = data['id']
	voteType = data['votetype']
	post = Posts.objects.get(id=id)
	if voteType == 'upvote':
		post.upvotes += 1
	else:
		post.upvotes -= 1 
	post.save()
	return JsonResponse('Message is transfered',safe=False)
