from __future__ import unicode_literals

from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def login(self, post):
		user = self.filter(email=post.get('email')).first()
		if user and bcrypt.hashpw(post.get('password').encode(), user.password.encode()) == user.password:
			return (True, user)
		return (False, 'notuser')
class User(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	dob = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Quote(models.Model):
	quote= models.TextField()
	author = models.CharField(max_length=100)
	creator = models.ForeignKey(User, related_name='origin')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at= models.DateTimeField(auto_now=True)

class Favorite(models.Model):
	added_by = models.ForeignKey(User, related_name='added')
	quote_id = models.ForeignKey(Quote, related_name='ids')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)