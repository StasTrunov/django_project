from django.shortcuts import render
from .models import Pweet, Profile, LikePweet, Comment
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



# Create your views here.

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










# class RegistrationView(CreateView):
#     form_class = PweetCreate
#     template_name = 'registration.html'
#     success_url = reverse_lazy('login')


# def create_pweet(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         content = request.POST['content']


#         if User.objects.filter(username=username).exists():
#             new_profile = Pweet.objects.create(username=username, content=content)
#             new_profile.save()
#             return redirect('/')
#         else:   
#             messages.info(request, 'This username is not exist')
#             return redirect('/signup')
        
#     else:
#         context = {'title': 'Create PRof'}
#         return render(request, 'index.html', context)




def like_post(request):
    user = request.user
    pweet_id = request.GET.get('pweet_id')

    pweet = Pweet.objects.get(id=pweet_id )

    like_filter = LikePweet.objects.filter(pweet_id=pweet_id , user=user).first()

    if like_filter == None:
        new_like = LikePweet.objects.create(pweet_id=pweet_id , user=user)
        new_like.save()
        pweet.no_of_likes = pweet.no_of_likes+1
        pweet.save()
        return redirect('/')
    else:
        like_filter.delete()
        pweet.no_of_likes = pweet.no_of_likes-1
        pweet.save()
        return redirect('/')



# class PostView(TemplateView):
#     template_name = 'index.html'

#     def like_post(self, request):
#                 data = request.POST
#                 user = request.user
#                 pweet = Pweet.objects.get(id=self.kwargs['pk'])
#                 if 'like' in data.keys():
#                     like = LikePweet.objects.filter(pweet=pweet)
#                     is_like = 0
#                     for i in like:
#                         if i.user == user:
#                             i.delete()
#                             break
#                     else:
#                         is_like = 1
#                         l = LikePweet(pweet=pweet, user=user)
#                         l.save()
#                     return JsonResponse({'like_amount': len(LikePweet.objects.filter(pweet=pweet)), 'isLike': is_like}, safe=False)
#                 if 'is_like' in data.keys():
#                     like = LikePweet.objects.filter(pweet=pweet)
#                     for i in like:
#                         if i.user == user:
#                             return JsonResponse({'like': 1}, safe=False)
#                     else:
#                         return JsonResponse({'like': 0}, safe=False)





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
    












