from django.shortcuts import render
from .models import Pweet, Profile, LikedPweet, Comment
from django.contrib.auth.models import User
from .forms import PweetCreate, ImageCreate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm,AdminPasswordChangeForm
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from pathlib import Path
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse



# Create your views here.

@csrf_exempt
def index(request):

        if request.method == 'POST':

            form = PweetCreate(request.POST)

            if form.is_valid():
                content = form.cleaned_data['content']
                username = request.user
                profile = Profile.objects.get(user=username)
                new_pweet = Pweet(user=username, content=content, profile=profile)
                new_pweet.save()
                return redirect('/')
                    
        else:
            form = PweetCreate()
            pweets = Pweet.objects.all()
            context = {'pweets': pweets, 'title': 'Home', 'form': form}
            return render(request, 'index.html', context)
        

        if request.method == "PUT":
            data = json.loads(request.body)
            pweet_id = data.get("pweet_id")
            like = data.get("like")
            if like:
                pweet = Pweet.objects.get(id=pweet_id)
                user=User.objects.get(id=request.user.id)
                if user in pweet.likes.all():
                    l = LikedPweet.objects.get(pweet_owner=pweet.owner,pweet=pweet,liker=user)
                    l.delete()
                    pweet.likes.remove(user)
                    pweet.save()
                    print(pweet.likes.count())
                    return JsonResponse({"like":"etshal","likes_count":str(pweet.likes.count())},status=200)
                else:
                    pweet.likes.add(user)
                    l = LikedPweet(post_owner=pweet.owner,post=pweet,liker=user)
                    l.save()
                    print(pweet.likes.count())
                    pweet.save()
                    return JsonResponse({"like":"like et7aet","likes_count":str(pweet.likes.count())},status=200)

        else:
            return JsonResponse({"error":"Your request Falied"})



def profile(request, pk):

    user_object = User.objects.get(id=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_pweets = Pweet.objects.filter(user=user_object)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_pweets': user_pweets,
    }





    return render(request, 'profile.html', context)





@csrf_exempt
def delete(request,pweet_id):
    if request.method == "DELETE":
        pweet = Pweet.objects.get(id=pweet_id)
        pweet.delete()
        return HttpResponseRedirect(reverse("profile"))
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)









def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        bio = request.POST['bio']

        # form = ImageCreate(request.POST)
        if password == password2:
            # if User.objects.get(user=username):
            #     messages.info(request, 'Username Taken')
            #     return redirect('signup')
            # else:
                
                    user = User.objects.create_user(username=username,  password=password)
                    auth.login(request, user)
                    user.save()

                    #log user in and redirect to settings page
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)
                    #create a Profile object for the new user
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, bio=bio)
                    new_profile.save()
                        
                    return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
            
        
    else:
        # form = ImageCreate()
        context = { 'title': 'SignUp Page'}
        return render(request, 'signup.html', context)
    



def signin(request):
    context = { 'title': 'SignIn Page'}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html', context)
    












