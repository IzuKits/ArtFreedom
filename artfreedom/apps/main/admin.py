from django.contrib import admin

from .models import Challenge_article, Comment, User_data, Image, Challenge_to_User

admin.site.register(Challenge_article)
admin.site.register(Comment)
admin.site.register(User_data)
admin.site.register(Image)
admin.site.register(Challenge_to_User)
