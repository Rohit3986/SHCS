from django.db import models
import datetime

from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, first_name,last_name,phone_number,email, user_type, gender,password=None, password2=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_type=user_type,
            gender = gender,
            email=self.normalize_email(email)
        )
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,last_name,phone_number,email, user_type, gender,password=None, password2=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        print(email,user_type,password)
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=self.normalize_email(email),
            password=password,
            user_type=user_type,
            gender = gender
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=25,blank=True)
    last_name = models.CharField(max_length=25,blank=True)
    phone_number = models.CharField(max_length=14,blank=True)
    email = models.EmailField(verbose_name='Email',max_length=255,unique=True,blank=True)
    gender = models.CharField(choices=(('Male','Male'),('Female','Female')),max_length=10,blank=True)
    user_type = models.CharField(choices=(('Doctor','Doctor'),('Patient','Patient'),('Handler_Team','Handler_Team')),default="Patient",max_length=17,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender','user_type']
    

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Symptom(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)