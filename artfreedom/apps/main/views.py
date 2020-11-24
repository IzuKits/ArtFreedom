from django.shortcuts import render
from .models import Challenge_article, Comment, Challenge_to_User, User_data
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.utils import timezone
from enum import Enum, auto
from math import ceil

def catalog(request):
    latest_challenges_list = []#Challenge_article.objects.order_by("-pub_date")[:5]
    if request.GET:
        page = request.GET['page']
    else:
        page = 1
    try:
        items_on_page = 3
        challenges = Challenge_article.objects.order_by("-pub_date")[(int(page) - 1) * items_on_page:items_on_page * int(page)]
        max_page = ceil(Challenge_article.objects.count() / items_on_page)
        for ch in challenges:
            dic = {
                'name':ch.article_title,
                'start_date':ch.start_date,
                'recruitment_time':ch.recruitment_time,
                'users_count':Challenge_to_User.objects.filter(challenge=ch).count(),
                'id':ch.id,
                'challenge_status':get_challenge_status(ch).value,
                'challenge_status_en':get_challenge_status(ch).name,
            }

            if ch.avatar:
                dic['avatar'] = ch.avatar.image.url
            latest_challenges_list.append(dic)

    except:
        raise Http404("Страница не найдена")

    #challanges = 
    return render(request, "main/catalog.html",{
        "latest_challenges_list":latest_challenges_list,
            'page': {
                "current_page":page,
                "last_page":max_page,
            },})

def participate(request):
    id = request.GET["challenge"]
    ch = Challenge_article.objects.get(id=id)
    user = User_data.objects.get(user=request.user)

    link = Challenge_to_User(user=user, challenge=ch, role="participant")
    link.save()

    return HttpResponse(request.GET["challenge"])

def index(request):
    return render(request, "main/index.html")

def helper(request):
    return render(request, "main/help.html")
    
    
def detail(request, challenge_article_id):
    try:
        a = Challenge_article.objects.get(id = challenge_article_id)
    except:
        raise Http404("Статья не найдена")
    return render(request, "main/details.html", {"article": a})

def challenge(request, id):
    args = {}
    ch = Challenge_article.objects.get(id=id)
    args['pub_date'] = ch.pub_date
    args['start_date'] = ch.start_date
    args['recruitment_time'] = ch.recruitment_time
    args['creator'] = ch.challenge_to_user_set.get(role='creator').user
    args['title'] = ch.article_title
    args['description'] = ch.article_description
    args['avatar_url'] = ch.avatar.image.url
    args['participants'] = ch.challenge_to_user_set.all()
    args['challenge_status'] = get_challenge_status(ch).value
    args['challenge_status_en'] = get_challenge_status(ch).name
    args['id'] = id
    if request.user.is_authenticated:
        user = User_data.objects.get(user=request.user)
        isparticipated = Challenge_to_User.objects.filter(challenge=ch, user_id=user.id).count()
        args['isparticipated'] =  not (isparticipated == 0)
    else:
        args['isparticipated'] =  False


    return render(request, "main/challenge.html", args)




def get_challenge_status(challenge):
    """ if (
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


class ChallengeStatus (Enum):
    recruitment = "Идет набор"
    active = "Активный"
    finished = "Завершен"


