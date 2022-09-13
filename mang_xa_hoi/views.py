from email import message
# from email.mime import image
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate
from django.contrib import messages
# from django.http import HttpResponse
from .models import Friends, Profile, Post, LikePost
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.


@login_required(login_url='signin')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_friend_list = []
    feed = []

    user_friend = Friends.objects.filter(friend=request.user.username)

    for user in user_friend:
        user_friend_list.append(user.user)
    for usernames in user_friend_list:
        feed_list = Post.objects.filter(user=usernames)

        feed.append(feed_list)

    feed_list = list(chain(*feed))

    # user suggestions starts
    all_users = User.objects.all()
    user_friend_all = []

    for user in user_friend:
        user_list = User.objects.get(username=user.user)
        user_friend_all.append(user_list)

    new_suggestions_list = [x for x in list(
        all_users) if (x not in list(user_friend_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(
        new_suggestions_list) if(x not in list(current_user))]
    random.shuffle(final_suggestions_list)
    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'home.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    friend = request.user.username
    user = pk

    if Friends.objects.filter(friend=friend, user=user).first():
        button_text = 'UnFriend'
    else:
        button_text = 'Add Friend'

    user_friend = len(Friends.objects.filter(user=pk))
    user_friend2 = len(Friends.objects.filter(friend=pk))
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_friend': user_friend,
        'user_friend2': user_friend2,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def addfriend(request):
    if request.method == 'POST':
        friend = request.POST['friend']
        user = request.POST['user']

        if Friends.objects.filter(friend=friend, user=user).first():
            delete_friend = Friends.objects.get(friend=friend, user=user)
            delete_friend.delete()
            return redirect('/profile/'+user)
        else:
            new_friend = Friends.objects.create(friend=friend, user=user)
            new_friend.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id=ids)
            username_profile_list.append(profile_lists)
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'username': username, 'user_profile': user_profile, 'username_profile_list': username_profile_list})


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(
        post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(
            post_id_id=post_id, username=username)
        new_like.save()

        post.liked = post.liked+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.liked = post.liked-1
        post.save()
        return redirect('/')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image'):
            image = user_profile.profileImg
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            # email= request.POST['email']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileImg = image
            user_profile.firstName = firstName
            user_profile.lastName = lastName
            # User.objects.update(first_name=firstName, last_name=lastName)
            # user.first_name = firstName
            # user.last_name = lastName
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            # email= request.POST['email']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileImg = image
            user_profile.firstName = firstName
            user_profile.lastName = lastName
            # User.objects.update(first_name=firstName, last_name=lastName)
            # user.first_name = firstName
            # user.last_name = lastName
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            # User.save()
            # User.objects.update(email = email)
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})


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
            user_login = auth.authenticate(
                username=username, password=password)
            auth.login(request, user_login)
            # create a Profile object for the new user

            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(
                user=user_model, id=user_model.id)
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
            login(request, user)
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
