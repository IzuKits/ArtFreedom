 
from django.urls import path

from . import views

app_name = "userprofile"


urlpatterns =[
    path("", views.myprofile, name="myprofile"),
    path("user<int:userid>/", views.profile, name="profile"),
    path("newchallenge/", views.add_new_challenge, name="add_new_challenge"),
]