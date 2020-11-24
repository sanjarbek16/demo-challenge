from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Challenge, FinishChallenge, Joined, Invitation
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ChallengeForm, FinishChallengeForm
from activities.utils import create_action
from django.db.models import Count
from activities.models import Activity, Action
import json
from django.views.decorators.csrf import csrf_protect



# challenge detail page
def detail(request, slug):
    challenge = get_object_or_404(Challenge, slug=slug)
    if request.method == 'POST':
        finish_form = FinishChallengeForm(data=request.POST, files=request.FILES)
        if finish_form.is_valid():
            new_finish = finish_form.save(commit=False)
            new_finish.challenge = challenge
            new_finish.profile = request.user.profile
            new_finish.save()
            messages.success(request, 'You finished the challenge successfully')
            finish_form = FinishChallengeForm()
    else:
        finish_form = FinishChallengeForm()


    return render(request, 'challenges/detail.html', {'challenge': challenge, 'finish_form': finish_form})



# adding books to favourites
@ajax_required
@require_POST
@login_required
def join_challenge(request):
    action = request.POST.get('action')
    challenge_id = request.POST.get('id')
    try:
        challenge = Challenge.objects.get(id=challenge_id)
        profile = request.user.profile
        if action == 'join':
            Joined.objects.get_or_create(profile=profile, challenge=challenge)
        else:
            Joined.objects.filter(profile=profile, challenge=challenge).delete()
        return JsonResponse({'status': 'ok'})
    except:
        return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})



def list(request):
    challenges = Challenge.objects.all()
    paginator = Paginator(challenges, 12)
    page = request.GET.get('page')
    try:
        challenges = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        challenges = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        challenges = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'challenges/challenges.html',
                      {'challenges': challenges})
    return render(request,
                  'challenges/list.html',
                   {'challenges': challenges,})


@login_required
def challenge_create(request):
    """
    View for creating a Book.
    """
    if request.method == 'POST':
        # form is sent
        form = ChallengeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # form data is valid
            challenge = form.save(commit=False)
            challenge.user = request.user
            challenge.save()
            form.save_m2m()
            messages.success(request, 'Challenge created successfully')
            create_action(request.user, 'created a challenge', challenge)
            # redirect to new created item detail view
            return redirect(challenge.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ChallengeForm()

    return render(request, 'challenges/create.html', {'form': form,})


def leaderboard(request, slug):
    challenge = get_object_or_404(Challenge, slug=slug)
    results = FinishChallenge.objects.filter(challenge=challenge).order_by('score')
    paginator = Paginator(results, 10)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        results = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'challenges/leaderboard.html',
                      {'results': results})

    return render(request, 'challenges/leaderboard_list.html', {'challenge': challenge, 'results':results})


@ajax_required
@require_POST
@login_required
def challenge_invite(request):
    user_id = request.POST.get('id')
    challenge_id = request.POST.get('challenge')
    action = request.POST.get('action')
    if user_id and challenge_id and action:
        try:
            inv_to = User.objects.get(id=user_id)
            challenge = Challenge.objects.get(id=challenge_id)
            if action == 'invite':
                Invitation.objects.get_or_create(inv_from=request.user,
                                              inv_to=inv_to, challenge=challenge)
                request.user.profile.notify_invited(challenge, inv_to)
            else:
                Invitation.objects.filter(inv_from=request.user,
                                       inv_to=inv_to, challenge=challenge).delete()
                request.user.profile.unotify_invited(challenge, inv_to)
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})


def invite_following(request, slug):
    user = request.user
    challenge = get_object_or_404(Challenge, slug=slug)
    invited_users = []
    if Invitation.objects.filter(challenge=challenge, inv_from=user).exists():
        old_invitations = Invitation.objects.filter(challenge=challenge, inv_from=user)
        for invitation in old_invitations:
            invited_users.append(invitation.inv_to)
    followings = user.following.all()
    paginator = Paginator(followings, 20)
    page = request.GET.get('page')
    try:
        followings = paginator.page(page)
    except PageNotAnInteger:
        followings = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        followings = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'challenges/invite_following.html', {'user':user, 'followings':followings, 'challenge':challenge, 'invited_users':invited_users})
    return render(request, 'challenges/invite.html', {'user':user, 'followings':followings, 'challenge':challenge, 'invited_users':invited_users})



@login_required
def create_challenge(request):
    """
    View for creating a Book.
    """
    if request.method == 'POST':
        # form is sent
        form = ChallengeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # form data is valid
            challenge = form.save(commit=False)
            challenge.user = request.user
            challenge.save()
            form.save_m2m()
            messages.success(request, 'Challenge created successfully')
            create_action(request.user, 'created a challenge', challenge)
            # redirect to new created item detail view
            return redirect(challenge.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ChallengeForm()

    return render(request, 'challenges/create.html', {'form': form,})

