from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	)
from django.conf import settings

import os

class MyUserManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

def get_profile_image_filepath(self, filename):
	return f'profile_images/{self.username}/profile_image.png'

def get_default_profile_image():
	return "profile_images/dummy_image.png" # Development

class Skills(models.Model):
    name  = models.CharField(max_length=50)

    class Meta:
        verbose_name=('Skill')
        verbose_name_plural=("Skills")

    def __str__(self):
        return str(self.name)

class Profession(models.Model):
    name  = models.CharField(max_length=100)

    class Meta:
        verbose_name=('Profession')
        verbose_name_plural=("Professions")

    def __str__(self):
        return str(self.name)
    
class User(AbstractBaseUser):
		
	GENDER 					= (
								('Male','Male'),
								('Female','Female'),
								)

	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	hide_email				= models.BooleanField(default=True)
	hide_phone				= models.BooleanField(default=True)
	first_name             	= models.CharField(max_length=100, blank=True, null=True)
	middle_name             = models.CharField(max_length=100, blank=True, null=True)
	last_name             	= models.CharField(max_length=100, blank=True, null=True)
	profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, blank=True, default=get_default_profile_image)
	# country             	= CountryField(blank_label='(select country)')
	address             	= models.CharField(max_length=100, blank=True, null=True)
	phone_number        	= models.CharField(max_length=30, blank=True, null=True)
	gender              	= models.CharField(max_length=10,default='Select gender' , choices=GENDER)
	bio                 	= models.TextField(max_length=500, blank=True, null=True)
	facebook_link       	= models.URLField(max_length=130, blank=True, null=True)
	twitter_link        	= models.URLField(max_length=130, blank=True, null=True)
	profession          	= models.ManyToManyField(Profession, blank=True)
	skills              	= models.ManyToManyField(Skills, blank=True)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyUserManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_superuser

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
