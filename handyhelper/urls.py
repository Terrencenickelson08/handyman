"""handyhelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from myapp  import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.showAllJobs),
    path('logout', views.logout),
    path('dashboard', views.home),
    path('createjob', views.createjob),
    path('addjob', views.explainjob),
    path("addtofaves/<int:job_id>", views.addtofaves),
    path('editfaves/<int:job_id>', views.editfaves, name = "editpage"),
    path('showjob/<int:job_id>', views.showjob),
    path('delete/<int:job_id>', views.delete),
    path('updateposting/<int:job_id>',views.updateposting),
    path('removejob/<int:job_id>', views.removejob)
   
]
