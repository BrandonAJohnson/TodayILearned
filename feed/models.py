from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	text = models.CharField(max_length=240)
	title = models.CharField(max_length=80, null=True)
	details = models.TextField(null=True)
	date = models.DateTimeField(auto_now=True)
	tag = models.CharField(max_length=32, null=True)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE, # when user is deleted, delete posts
	)

	def __str__(self):
		return self.text[0:100]
