from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.conf import settings as conf_settings
import sys, os


def picture_user_directory_path(instance, filename):
    return f"user_{instance.User_data.id}/{filename}"


class Image(models.Model):
    image = models.ImageField(upload_to='temp')
    description = models.TextField("Описание к картинке", blank=True, default="")

    author = models.ForeignKey('main.User_data', on_delete=models.CASCADE)
    challenge = models.ForeignKey('main.Challenge_article', blank=True, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        if 'temp' in self.image.path:
            init_path = self.image.path

            new_img_name = 'image_' + self.author.user.username + '_' + str(self.id) + os.path.splitext(os.path.basename(init_path))[1]
            new_name = '/'.join(['images', str(self.author.pk), new_img_name])

            new_path = os.path.join(conf_settings.MEDIA_ROOT, 'images', str(self.author.pk), new_img_name)

            if not os.path.exists(os.path.dirname(new_path)):
                os.makedirs(os.path.dirname(new_path))
            
            os.rename(init_path, new_path)
            self.image.name = new_name

            super(Image, self).save(*args, **kwargs)


class User_data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    status = models.CharField("статус пользователя", max_length=500, blank=True)
    contacts = models.CharField("контакты пользователя", max_length=200)
    avatar = models.CharField("Аватар", blank=True, max_length=2500, default="", null=True)

    #challenges = models.ForeignKey('Challenge_to_User', null=True, on_delete=models.SET_NULL, blank=True)


    def __str__(self):
        return self.user.username




class Challenge_article(models.Model):
    article_title = models.CharField("название челленджа", max_length=200)
    article_description = models.TextField("описание челленджа")
    pub_date = models.DateTimeField("дата публикации") 
    start_date = models.DateTimeField("дата начала", default=datetime.now())
    recruitment_time = models.IntegerField("время челледжа (в днях)")  # in days

    avatar = models.CharField("Аватар", blank=True, max_length=2500, default="", null=True)


    #users = models.ForeignKey('Challenge_to_User', null=True, on_delete=models.SET_NULL, blank=True)

    participants = models.ManyToManyField(User_data, through="Challenge_to_User")
    #creator = models.ForeignKey(User_data, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.article_title

    def is_challenge_active(self):
        #is_recruitment = self.recruitment_time > ((timezone.now() - self.pub_date).days
        is_finished = (timezone.now() - self.start_date).days >= self.recruitment_time
        return not is_finished
        #return self.recruitment_time > ((timezone.now() - self.pub_date).seconds / 60 / 60 / 24)
    
    class Meta:
        verbose_name = "Челлендж"
        verbose_name_plural = "Челленджи" 

class Challenge_to_User(models.Model):
    challenge = models.ForeignKey(Challenge_article, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User_data, null=True, on_delete=models.SET_NULL)

    role = models.CharField(max_length=50, choices=[
                                                ('creator', 'creator'),
                                                ('participant', 'participant'),
                                                ('banned', 'banned'),
                                                ])



class Comment(models.Model):
    article = models.ForeignKey(Challenge_article, on_delete=models.CASCADE)
    author_name = models.CharField("Имя автора", max_length=200)
    comment_text = models.TextField("текст комментария")

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


