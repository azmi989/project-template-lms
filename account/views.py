from django.conf import settings
from django.contrib.auth import (login, authenticate, logout)
from django.http import HttpResponse
from django.shortcuts import (render, redirect)

from .models import User
from .forms import (RegistrationForm, UserAuthenticationForm, UserUpdateForm)


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticate as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('/')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'user/register.html', context)


def user_view(request, *args, **kwargs):
    context = {}
    username = kwargs.get("username")

    print(username)
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse("Something went wrong.")
    if user:
        context['id'] = user.id
        context['email'] = user.email
        context['username'] = user.username
        context['first_name'] = user.first_name
        context['middle_name'] = user.middle_name
        context['last_name'] = user.last_name
        context['address'] = user.address
        context['profile_image'] = user.profile_image
        context['is_active'] = user.is_active
        context['is_staff'] = user.is_staff
        context['is_superuser'] = user.is_superuser
        context['hide_email'] = user.hide_email
        context['hide_phone'] = user.hide_phone
        context['phone_number'] = user.phone_number
        context['gender'] = user.gender
        context['bio'] = user.bio
        context['facebook_link'] = user.facebook_link
        context['twitter_link'] = user.twitter_link
        context['profession'] = user.profession
        context['skills'] = user.skills
    return render(request, "user/user.html", context)


def edit_user_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    username = kwargs.get("username")
    user = User.objects.get(username=username)
    if user.username != request.user.username:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = UserUpdateForm(request.POST, request.FILES,
                              instance=request.user)
        if form.is_valid():
            form.save()
            new_username = form.cleaned_data['username']
            return redirect("account:view", username=user.username)
        else:
            form = UserUpdateForm(request.POST, instance=request.user,
                                  initial={
                                      "id": user.pk,
                                      "email": user.email,
                                      "username": user.username,
                                      "first_name": user.first_name,
                                      "middle_name": user.middle_name,
                                      "last_name": user.last_name,
                                      "address": user.address,
                                      "profile_image": user.profile_image,
                                      "is_active": user.is_active,
                                      "is_staff": user.is_staff,
                                      "is_superuser": user.is_superuser,
                                      "hide_email": user.hide_email,
                                      "hide_phone": user.hide_phone,
                                      "phone_number": user.phone_number,
                                      "gender": user.gender,
                                      "bio": user.bio,
                                      "facebook_link": user.facebook_link,
                                      "twitter_link": user.twitter_link,
                                      "profession": user.profession,
                                      "skills": user.skills,
                                  }
                                  )
            context['form'] = form
    else:
        form = UserUpdateForm(
            initial={
                "id": user.pk,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "middle_name": user.middle_name,
                "last_name": user.last_name,
                "address": user.address,
                "profile_image": user.profile_image,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "hide_email": user.hide_email,
                "hide_phone": user.hide_phone,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "bio": user.bio,
                "facebook_link": user.facebook_link,
                "twitter_link": user.twitter_link,
                "profession": user.profession,
                "skills": user.skills,
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "user/edit_user.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("/")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("/")

    else:
        form = UserAuthenticationForm()

    context['login_form'] = form

    return render(request, "user/login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect
