from email import message
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
# from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='signin')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='signin')
def settings(request):
    return render(request, 'setting.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()

            # log user in and redirect to setting page
            user_login = auth.authenticate(username = username, password = password)
            auth.login(request, user_login)
            # create a Profile object for the new user

            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id=user_model.id)
            new_profile.save()
            return redirect('settings')
        else:
            messages.info(request, 'Password not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            return redirect('/')
        else:
            messages.info(request, 'Wrong username or password')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
