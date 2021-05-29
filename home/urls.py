from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("task",views.task,name="task"),
    path("fixed",views.fixed,name="fixed"),
    path("schedular",views.schedular,name="schedular"),
]