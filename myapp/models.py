from django.db import models
import re
import bcrypt
import datetime



class UserManager(models.Manager):
    def registration_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        usersWithEmail = User.objects.filter(email = postData['email'])
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['firstname']) < 3:
            errors["firstname"] = "Firstname should be at least 2 characters"
        if len(postData['lastname']) < 3:
            errors["lastname"] = "Lastname should be at least 2 characters"
        if len(postData['email']) < 3:
            errors["emailblank"] = "Email is required"
        if len(usersWithEmail) >0:
            errors['emailTaken'] = "Email is taken already "
        if not EMAIL_REGEX.match(postData['email']):   
            errors['emailpattern'] = ("Invalid email address")
        if len(postData['password']) < 3:
            errors["passwordlength"] = "Password must be atleast 3 characters"
        if postData['confirmpassword'] != postData['password']:
            errors["pwmatch"] = "Password and confirm password must match"
        print (errors)
        return errors

    def login_validator(self, postData):
        usersWithEmail = User.objects.filter(email=postData['email'])
        
        errors = {}
        if len(postData['email']) <1:
            errors['emailrequired'] = "you must enter an email"
        if len(postData['password']) <1:
            errors['passwordrequired'] = "you must enter a password" 
        if len(usersWithEmail) <1:
            errors['emailNotFound'] = "email is not registered"
        else: 
            user = usersWithEmail[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("password match")
            else:
                print("failed password")
                errors['passwordInvalid'] = "The password is incorrect"
        print(errors)
        return errors


class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['title'])<1:
            errors['titlerequired'] = "You must state the title of the job "
        if len(postData['description'])<1:
            errors['descriptionrequired'] = "You must enter a description"
        if len(postData['address'])<1:
            errors['addressrequired'] = "You must enter a location"
        return errors

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE, null=True)
    fav_jobs = models.ManyToManyField (User, related_name="saved_jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
