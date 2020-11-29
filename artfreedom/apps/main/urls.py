from django.urls import path

from . import views

app_name = "main"


urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("deletechallenge/", views.delete_challenge, name="delete"),
    #path("<int:challenge_id>/", views.challenge, name="challenge"),

]
