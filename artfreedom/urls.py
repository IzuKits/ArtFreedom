"""artfreedom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from main import views
from loginsys import views as login_views
from userprofile import views as user_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.storage import staticfiles_storage

from django.conf import settings
from django.urls import include, re_path

from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
from django.views.generic.base import TemplateView

urlpatterns = [
    path("catalog/", include("main.urls")),
    path("index/", views.index, name="index"),
    path("helper/", views.helper, name="helper"),
    path('admin/', admin.site.urls),
    #path("challenge/", include("main.urls")),
    path("challenge/<int:id>/", views.challenge, name="challenge"),
    path("challenge/participate/", views.participate, name="participate"),
    path("registration/", login_views.registration, name="registration"),
    path("login/", login_views.login, name="login"),
    path("profile/", include("userprofile.urls")),
    path("logout/", login_views.logout, name="logout"),
    path(
        'favicon.ico',
        RedirectView.as_view(url=staticfiles_storage.url('/imgs/favicon.ico'))
    ),
    path("kickuser/", views.kick_user, name='kick_user'),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
urlpatterns += [
    path('', RedirectView.as_view(url="index/", permanent=True))
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#urlpatterns += patterns('',
#   url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),)
	
urlpatterns += staticfiles_urlpatterns()
