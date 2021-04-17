from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login as loginUser
from django.contrib import auth
from django.http import JsonResponse
from random import randint
from django.contrib.auth.decorators import login_required
import re


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            if re.match("[^@]+@[^@]+\.[^@]+", request.POST.get('username')):
                username = User.objects.get(email=request.POST.get('username'))

            user = authenticate(request, username=username, password=password)

            if user is None:
                return JsonResponse({"error": "Incorrect username/email or password"}, status=400)
            else:
                loginUser(request, user)
                return JsonResponse({"success": ""}, status=200)

        else:
            return render(request, 'login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                if User.objects.filter(username=username).exists():
                    error = 'This username is taken'
                    return JsonResponse({"error": error}, status=400)
                else:
                    if User.objects.filter(email=email).exists():
                        error = 'This email is already in use'
                        return JsonResponse({"error": error}, status=400)
                    else:
                        user = User.objects.create_user(username=username, password=password, email=email,
                                                        first_name=first_name, last_name=last_name)
                        user.save()
                        return JsonResponse({"success": True}, status=200)
            else:
                error = 'Your passwords don\'t match'
                return JsonResponse({"error": error}, status=400)

        else:
            return render(request, "signup.html")


def logout(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            auth.logout(request)
            return redirect('index')


def forgotPassword(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            email = request.POST.get('email')

            if User.objects.filter(email=email).exists() and email:
                code = randint(000000, 999999)

                send_mail(
                    'Password reset for Zay shop',
                    'Your code is ' + str(
                        code) + ' there has been a password reset request made to this email, if that was not '
                                'you, you can ignore this '
                                'message',
                    'zayshopmail@gmail.com',
                    [email, 'zayshopmail@gmail.com'],
                    fail_silently=False
                )
                request.session['code'] = code
                request.session['email'] = email
                return render(request, 'forgot_password.html')

            else:
                return render(request, 'email.html', {"not_exists": True})

        else:
            return render(request, 'email.html')


def resetPassword(request):
    if request.user.is_authenticated or "email" not in request.session or "code" not in request.session:
        return redirect('index')
    else:
        if request.method == "POST":
            email = request.session['email']
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            code = request.POST.get('code')

            if password == password2:

                if code == str(request.session['code']):
                    user = User.objects.get(email=email)
                    user.set_password(password)
                    user.save()
                    del request.session['code']
                    del request.session['email']
                    return render(request, 'login.html', {"success": True})

                else:
                    return render(request, 'forgot_password.html', {"error": "Incorrect code"})

            else:
                return render(request, 'forgot_password.html', {"error": "Passwords mismatch"})

        else:
            return render(request, 'forgot_password.html')


@login_required
def profile(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        avatar = request.FILES.get('avatar')
        user = request.user

        if username:
            if User.objects.filter(username=username).exists():
                return render(request, 'profile.html', {"error": "Username already exists"})
            else:
                user.username = username
                user.save()

        if email:
            if User.objects.filter(email=email).exists():
                return render(request, 'profile.html', {"error": "Email already taken"})
            else:
                user.email = email
                user.save()

        if avatar:
            user.user.avatar = avatar
            user.user.save()

        if password:
            if password == password2:
                user =  User.objects.get(pk=request.user.id)
                user.set_password(password)
                user.save()
                loginUser(request, user)
            else: 
                return render(request, 'profile.html', {"error": "passwords mismatch"})

        return render(request, 'profile.html')

    else:
        return render(request, 'profile.html')
