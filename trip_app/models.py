from django.db import models
import re

# Create your models here.
class LoginManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be longer than 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be longer than 2 characters"
        email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email.match(post_data['email']):
            errors['email'] = 'Enter valid Email'
        result = User.objects.filter(email=post_data['email'])
        if len(post_data['password']) < 8:
            errors['password'] = "Password is too short!"
        if post_data['password'] != post_data['cPassword']:
            errors['cPassword'] = "Passwords do not match!"
        elif post_data['password'] != post_data['cPassword']:
            errors['cPassword'] = "Password Match"
        return errors

    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['dest']) < 2:
            errors['destination'] = "Destionation must be longer than 2 characters"

        if (post_data['start']) == "":
            errors['start_date'] = "Enter a proper date"

        if (post_data['end']) == "":
            errors['end_date'] = "Enter a proper date"
        
        if len(post_data['plan']) < 10:
            errors['plan'] = "Plan must be longer than 10 characters"
        return errors

    def edit_validator(self, post_data):
        errors = {}

        if len(post_data['new_dest']) < 2:
            errors['destination'] = "Destionation must be longer than 2 characters"

        if (post_data['new_start']) == "":
            errors['start_date'] = "Enter a proper date"

        if (post_data['new_end']) == "":
            errors['end_date'] = "Enter a proper date"
        
        if len(post_data['new_plan']) < 10:
            errors['plan'] = "Plan must be longer than 10 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.CharField(max_length=255)
    trip_details = models.ForeignKey(User, related_name='my_trip', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()
