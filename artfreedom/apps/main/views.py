from django.shortcuts import render, redirect
from .models import Challenge_article, Comment, Challenge_to_User, User_data
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.contrib import auth
from django.utils import timezone
from enum import Enum, auto
from math import ceil
from .forms import ChallengesFilterForm
from django.contrib import messages



def catalog(request):
    latest_challenges_list = []  # Challenge_article.objects.order_by("-pub_date")[:5]
    if request.GET.get("page", False):
        page = request.GET["page"]
    else:
        page = 1
    try:
        form_filter = ChallengesFilterForm(request.GET)
        challenges = Challenge_article.objects
        if form_filter.is_valid():
            if not form_filter.is_duration_filter_empty():
                if form_filter.cleaned_data['duration_max'] == None:
                    challenges = challenges.filter(recruitment_time__gte=form_filter.cleaned_data['duration_min'])
                else:
                    start = form_filter.cleaned_data['duration_min']
                    fin = form_filter.cleaned_data['duration_max']
                    challenges = challenges.filter(recruitment_time__range=(start, fin))

        challenges = challenges.order_by("-pub_date")
        for ch in challenges:
            dic = {
                "name": ch.article_title,
                "start_date": ch.start_date,
                "recruitment_time": ch.recruitment_time,
                "users_count": Challenge_to_User.objects.filter(challenge=ch).count(),
                "id": ch.id,
                "challenge_status": get_challenge_status(ch).value,
                "challenge_status_en": get_challenge_status(ch).name,
            }

            if ch.avatar != "":
                dic["avatar_url"] = ch.avatar
            latest_challenges_list.append(dic)

    except Exception as e:
        return HttpResponseNotFound()

    if form_filter.is_status_filter_empty():
        latest_challenges_list = list(filter(
            is_challenge_has_status(form_filter.cleaned_data['status1'],
            form_filter.cleaned_data['status2'], form_filter.cleaned_data['status3']),
            latest_challenges_list
        ))
    items_on_page = 2
    max_page = ceil(len(latest_challenges_list) / items_on_page)

    latest_challenges_list = latest_challenges_list[
            (int(page) - 1) * items_on_page : items_on_page * int(page)
        ]
    return render(
        request,
        "main/catalog.html",
        {
            "latest_challenges_list": latest_challenges_list,
            "page": {
                "current_page": page,
                "last_page": max_page,
            },
            "filter_form": form_filter,
        },
    )

def  is_challenge_has_status(recruitment, active, finished):
    def func (challenge):
        status = challenge['challenge_status_en']
        if ((status == 'recruitment') & recruitment):
            print("recruitment")
            return True
        elif ((status == 'active') & active):
            print("active")
            return True
        elif ((status == 'finished') & finished):
            print("finish")
            return True
    return func



def participate(request):
    id = request.GET["challenge"]
    ch = Challenge_article.objects.get(id=id)
    user = User_data.objects.get(user=request.user)

    link = Challenge_to_User(user=user, challenge=ch, role="participant")
    link.save()

    return HttpResponse(request.GET["challenge"])


def index(request):
    count = Challenge_article.objects.count()
    return render(request, "main/index.html", {'challenges_count':count})


def helper(request):
    return render(request, "main/help.html")


def detail(request, challenge_article_id):
    try:
        a = Challenge_article.objects.get(id=challenge_article_id)
    except:
        raise HttpResponseNotFound()
    return render(request, "main/details.html", {"article": a})


def challenge(request, id):
    args = {}
    try:
        ch = Challenge_article.objects.get(id=id)
    except:
        return HttpResponseNotFound()
    args["pub_date"] = ch.pub_date
    args["start_date"] = ch.start_date
    args["recruitment_time"] = ch.recruitment_time
    args["creator"] = ch.challenge_to_user_set.get(role="creator").user
    args["title"] = ch.article_title
    args["description"] = ch.article_description
    args["avatar_url"] = ch.avatar
    args["participants"] = ch.challenge_to_user_set.all()
    args["challenge_status"] = get_challenge_status(ch).value
    args["challenge_status_en"] = get_challenge_status(ch).name
    args["id"] = id
    if request.user.is_authenticated:
        user = User_data.objects.get(user=request.user)
        isparticipated = Challenge_to_User.objects.filter(
            challenge=ch, user_id=user.id
        ).count()
        args["isparticipated"] = not (isparticipated == 0)
        if isparticipated != 0:
            args["user_role"] = ch.challenge_to_user_set.get(user=user).role

    else:
        args["isparticipated"] = False

    return render(request, "main/challenge.html", args)


def get_challenge_status(challenge):
    """if (
    timezone.now() >= challenge.start_date
    and (timezone.now() - challenge.start_date).days >= challenge.recruitment_time
    ):
    """
    if (timezone.now() - challenge.start_date).days >= challenge.recruitment_time:
        return ChallengeStatus.finished
    elif timezone.now() >= challenge.start_date:
        return ChallengeStatus.active
    else:
        return ChallengeStatus.recruitment


def delete_challenge(request):
    if request.POST:
        Challenge_article.objects.get(id=request.POST["id"]).challenge_to_user_set.all().delete()
        Challenge_article.objects.get(id=request.POST["id"]).delete()
        return redirect('/catalog/')
    else:
        return HttpResponseNotFound()

class ChallengeStatus(Enum):
    recruitment = "Идет набор"
    active = "Активный"
    finished = "Завершен"
