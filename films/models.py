from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):
	title = models.CharField(max_length=100)
	slug = models.CharField(max_length=100)
	date_out = models.CharField(max_length=100)
	synopsis = models.TextField()
	genre = models.CharField(max_length=100)
	format_type = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True)
	thumb = models.ImageField(null=True,blank=True,upload_to='media')
	author = models.ForeignKey(User,default=None,on_delete=models.CASCADE)

	

	def __str__(self):
		return self.title
