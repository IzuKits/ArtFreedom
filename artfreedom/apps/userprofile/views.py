from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import ModelForm
from main.models import Challenge_article, Challenge_to_User, User_data, Image
from django.utils.timezone import datetime
from django import forms


# Create your views here.

def myprofile(request):
    args = {}
    if request.user.is_authenticated:
        args['username'] = request.user.username
        usr = User.objects.get(id=request.user.id)
        userdata = User_data.objects.get(user=usr)
        args['status'] = userdata.status
        args['contacts'] = userdata.contacts

        args['col_challenges'] = userdata.challenge_to_user_set.count()
        #args['challenges'] = userdata.challenge_to_user_set.all()
        challenges = get_challenges_set(userdata)
        args['challenges'] = challenges

        args['ismyprofile'] = True

        if userdata.avatar != "":
            args['avatar_url'] = userdata.avatar
        
    return render(request, "userprofile/profile.html", args)

def get_challenges_set(userdata):
        chs = userdata.challenge_to_user_set.all()
        res = []
        for c in chs:
            res.append({
            "challenge":c.challenge,
            "active":c.challenge.is_challenge_active()
            })
        return res


def profile(request, userid):
    args = {}
    if userid == request.user.id:
        return HttpResponseRedirect("/profile/")

    usr = User.objects.get(id=userid)
    userdata = User_data.objects.get(user=usr)
    args["username"] = usr.username
    args['status'] = userdata.status
    args['contacts'] = userdata.contacts
    args['col_challenges'] = userdata.challenge_to_user_set.count()
    args['challenges'] = get_challenges_set(userdata)


    if userdata.avatar != "":
        args['avatar_url'] = userdata.avatar
    args['ismyprofile'] = request.user.id == userid

    return render(request, "userprofile/profile.html", args)

def add_new_challenge(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/profile/")
    if request.method == "POST":
        start_date = datetime.strptime(request.POST['start_date'], "%Y-%m-%d")
        challenge = Challenge_article(article_title=request.POST['article_title'],
        article_description=request.POST['article_description'],
        start_date=start_date,
        recruitment_time=request.POST['recruitment_time'])
        challenge.pub_date = datetime.now()
        """form = newImage(request.POST, request.FILES)

        if form.is_valid():
            print("valid")
            image = form.save(commit=False)
            image.author = request.user.user_data
            image.save()
            challenge.avatar = image
        else:
            default = Image.objects.get(image="images/1/image_izukits_21.jpg")
            challenge.avatar = default
            print("invalid")
        """
        challenge.save()
        ch_ = Challenge_to_User(user=request.user.user_data,
            challenge=challenge, role='creator')
        ch_.save()

        return HttpResponseRedirect("/profile")
    else:
        return render(request, "userprofile/newchallenge.html")

class NewChallengeForm(ModelForm):
    class Meta:
        model = Challenge_article
        exclude = ['pub_date']

class newImage(ModelForm):
    class Meta:
        model = Image
        fields = ['image']