from django.urls import path,include
from django.views.generic import TemplateView
from .views import (
					HomeView,PostDetailView,
					CreateNewThread,CreateNewPost,
					InnerPostView,DeleteInnerPost,
					UpdateInnerPost,DeleteConfirmed,
					DeleteThread,UpdateVote
					)



urlpatterns = [

		path('',HomeView.as_view(),name='home'),
		path('about/', TemplateView.as_view(template_name="dashboard/about.html"),name='about'),
		path('updateVote/',UpdateVote,name='update-vote'),
		path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
		path('post/<int:pk>/deletethread',DeleteThread.as_view(),name='delete-thread'),
		path('post/<int:pk>/create_post/',CreateNewPost,name='create-post'),
		path('create_thread/',CreateNewThread.as_view(),name='create-thread'),
		path('innerpost/<int:pk>/',InnerPostView.as_view(),name='inner-post'),
		path('innerpost/<int:pk>/deletepost',DeleteInnerPost,name='delete-post'),
		path('innerpost/<int:pk>/delete_Confirmed',DeleteConfirmed,name='delete-confirmed'),
		path('innerpost/<int:pk>/updatepost',UpdateInnerPost,name='update-post'),
]