import json
from django.http.response import HttpResponse
from django.urls import reverse
from .models import Post, Profile, Follow, Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from .forms import FollowForm, LoginForm, RegisterForm, PostForm, TagForm

# Create your views here.

@login_required
def index(request):
    following = request.user.following.all()
    # print('User : ' , request.user.following)
    # return HttpResponse(status=200)
    f = [u.following_user for u in following]
    context = {
        'user' : request.user,
        'posts': Post.objects.filter(author__in = f)
    }

    return render(request, 'index.html', context=context)




def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        # password2 = form.cleaned_data.get("password2")
        birth_date = form.cleaned_data.get("birth_date")

        try:
            user = User.objects.create_user(username, email, password)
        except:
            user = None
        if user != None:
            login(request, user)
            user_profile = Profile.objects.filter(user=user)
            if(len(user_profile) > 1):
                request.session['register_error'] = 1 # 1 == True
                return render(request, "forms.html", {"form": form})
            user_profile = user_profile[0]
            user_profile.birth_date = birth_date
            user_profile.save()
            return redirect("/")
        else:
            request.session['register_error'] = 1 # 1 == True
    return render(request, "forms.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            # user is valid and active -> is_active
            # request.user == user
            login(request, user)
            return redirect("/")
        else:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] = attempt + 1
            # return redirect("/invalid-password")
            request.session['invalid_user'] = 1 # 1 == True
    return render(request, "forms.html", {"form": form})

def logout_view(request):
    logout(request)
    # request.user == Anon User
    return redirect("/login")





@login_required(login_url='login')
def profile(request):
    user_profile = request.user.profile
    following = request.user.following.all()
    followers = request.user.followers.all()
    posts = request.user.post.all()
    return render( request, 'profile.html', {'profile':user_profile, 'following':following, 'followers':followers, 'posts':posts})

@login_required(login_url='login')
def write_post_view(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = Post()
        post.author = request.user
        post.context = form.cleaned_data['context']
        post.save()
        for t in form.cleaned_data['tag']:
            post.tag.add(t)
        # for t in form.cleaned_data['tag']:
        #     t.post_set.add(post)
        #     t.save()
        return redirect("/profile/")
    return render(request, "forms.html", {"form": form})


@login_required(login_url='login')
def follow_view(request):
    following = Follow.objects.filter(follower_user__id=request.user.id)
    exclude_list = [uf.following_user.id for uf in following]
    exclude_list.append(request.user.id)
    form = FollowForm(exclude_list, data = request.POST or None)
    if form.is_valid():
        follow = Follow()
        follow.follower_user = request.user
        follow.following_user = form.cleaned_data['following_user']
        follow.save()
        return redirect("/profile/")
    return render(request, "forms.html", {"form": form})

def discover(request):
    context = {
        'tags' : Tag.objects.all()
    }
    return render(request, 'discover.html', context=context)

def discover_tag(request, name):
    context = {
        'posts' : Tag.objects.filter(name=str(name)).first().posts.all()
    }
    return render(request, 'discover_posts.html', context=context)

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if(request.POST.get('method') == 'like'):
        if(not request.user in post.likes.all()):
            post.likes.add(request.user)
            post.like_count += 1
            post.save()
        return HttpResponse(json.dumps({'like': True, 'unlike': False}), content_type="application/json", status=200)

    elif(request.POST.get('method') == 'unlike'):
        if(request.user in post.likes.all()):
            post.likes.remove(request.user)
            post.like_count -= 1
            post.save()
        return HttpResponse(json.dumps({'like': False, 'unlike': True}), content_type="application/json", status=200)

    return HttpResponse(status=400)


def add_tag_view(request):
    if(request.user.is_superuser):
        form = TagForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            for t in Tag.objects.all():
                if(t.name == name):
                    return render(request, "forms.html", {"form": form, 'message':'This tag already exist'})
            
            form.save()
            return render(request, "forms.html", {"form": form, 'message': name + ' saved successfully'})
        
        return render(request, "forms.html", {"form": form})
    else:
        return HttpResponse(status=500)