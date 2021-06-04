from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Threads(models.Model):
	title=models.CharField(max_length=100,unique=True)
	description=models.CharField(max_length=300,blank=True)
	created_by=models.ForeignKey(User,on_delete=models.CASCADE)
	total_posts = models.IntegerField(default=0)
	total_views = models.IntegerField(default=0)
	created_on=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('home')

class Posts(models.Model):
	heading=models.CharField(max_length=100)
	description=models.TextField()
	belongs_to_thread=models.ForeignKey(Threads,on_delete=models.CASCADE,blank=True,null=True)
	created_by=models.ForeignKey(User,on_delete=models.CASCADE)
	created_on=models.DateTimeField(default=timezone.now)
	upvotes = models.IntegerField(default=0)

	def __str__(self):
		return self.heading
