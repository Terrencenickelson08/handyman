from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q


def index(request):
    return render(request, "index.html")

def register(request):
    errorsFromModelsValidator = User.objects.registration_validator(request.POST)
    if len(errorsFromModelsValidator)>0:
        for key, value in errorsFromModelsValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        password  = request.POST['password']
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash1)
        user = User.objects.create(firstname = request.POST['firstname'], lastname = request.POST['lastname'], email = request.POST['email'], password=hash1.decode())
 
        request.session['id'] =user.id
    return redirect('/dashboard')

def login (request):
    errorsFromLoginValidator = User.objects.login_validator(request.POST) 
    if len(errorsFromLoginValidator) >0:
        for key, value in errorsFromLoginValidator.items():
             messages.error(request, value)
        return redirect("/")
    # context ={
    #     "loggedinuser": User.objects.filter(email = request.POST['email'])[0]
    # }
    user = User.objects.filter(email = request.POST['email'])[0]
    request.session['id']= User.objects.filter(email = request.POST['email'])[0].id
    return redirect("/dashboard")


def showAllJobs(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['id'])
        context ={
            'loggedinuser': User.objects.get(id = request.session['id']),
            'alljobs': Job.objects.exclude(fav_jobs = user),
            'favjobs': Job.objects.filter(fav_jobs = user),
}
    return render(request, 'dashboard.html', context)
                       

def explainjob(request):
    return render(request, "addjob.html")

def createjob(request):
    errorsFromModelsValidator = Job.objects.job_validator(request.POST)
    loggedinuser = User.objects.get(id = request.session['id'])
    if len(errorsFromModelsValidator) > 0:
        for key, value in errorsFromModelsValidator.items():
            messages.error(request, value)
        return redirect("/addjob")
    job = Job.objects.create (title = request.POST['title'], description = request.POST['description'], address = request.POST['address'], poster = loggedinuser)
    return redirect("/dashboard")

def showjob(request, job_id):
    job = Job.objects.get(id = job_id)
    user = User.objects.get(id = request.session['id'])
    context = {
        "job": job,
        "loggedinuser":user,

    }
    return render(request, "view.html", context)

def addtofaves(request,job_id):
    loggedinuser = User.objects.get(id = request.session['id'])
    this_job = Job.objects.get(id =job_id)
    this_job.fav_jobs.add(loggedinuser)
    context ={
        "loggedinuser": loggedinuser,
        "this_job": this_job
    }
    return redirect("/dashboard")


def editfaves(request,job_id):
    job = Job.objects.get(id = job_id)
    context={
        "job":job
    }
    return render(request, "edit.html", context)

def updateposting(request, job_id):
    job = Job.objects.get(id = job_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    job_to_edit = Job.objects.get (id=job_id)
    job_to_edit.title = request.POST["title"]
    job_to_edit.description = request.POST["description"]
    job_to_edit.address = request.POST["address"]
    job_to_edit.save()
    return redirect ("/dashboard")


def removejob(request, job_id):
    this_job = Job.objects.get(id = job_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    loggedinuser.saved_jobs.remove(this_job)
    
    return redirect("/dashboard")


def delete(request,job_id):
    job_to_delete = Job.objects.get(id =job_id)
    job_to_delete.delete()
    return redirect('/dashboard')


def home(request):
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")



# Create your views here.
