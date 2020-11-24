from django.urls import path

from . import views

app_name = "main"


urlpatterns = [
    path("", views.catalog, name="catalog"),
    #path("<int:challenge_id>/", views.challenge, name="challenge"),

]
