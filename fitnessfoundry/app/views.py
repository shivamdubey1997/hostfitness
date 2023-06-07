from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.views import View
from .models import Profile,Post,Uploadworkoutvideo,Bodyweight,Recepies,Video,Workout,Workoutmuscles,Thirtydayworkout
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate,login,logout
from django.utils.deprecation import MiddlewareMixin
import os
from django.shortcuts import get_object_or_404
# Create your views here.
def index(request):
    post = Post.objects.all().order_by('-id')
    productvlog = Video.objects.all().order_by('-id')
    return render(request, 'index.html',{'post':post,'productvlog':productvlog})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES['image']
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user, profile_picture=image)
        if profile:
            messages.success(request, 'Profile Created Please Login')
            return redirect("loggedin")

    return render(request,'signup.html')


def loggedin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")




    return render(request,'loggedin.html')


def Logout(request):
    logout(request)
    return redirect("loggedin")

def video(request):
    if request.method == 'POST':
        user = request.user
        video = request.FILES['video']
        videodescription = request.POST['videodescription']
        link = request.POST['link']
        profile = Profile.objects.get(user=user)
        posts = Video.objects.create(user=user, video=video, videodescription=videodescription,link=link, profile=profile)
        if posts:
            messages.success(request, 'Video Uploaded')
    return render(request,'videoupload.html')

def uploadpost(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES['image']
        description = request.POST['description']
        profile = Profile.objects.get(user=user)
        posts = Post.objects.create(user=user, image=image, description=description, profile=profile)
        if posts:
            messages.success(request, 'Post Uploaded')
    return render(request, 'uploadposts.html')

def workouts(request):
    workout = Workout.objects.all()
    video = Uploadworkoutvideo.objects.all().order_by('-id')

    if request.method == "GET":
        st = request.GET.get('servicename')
        if st != None:
            video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    return render(request,'workouts.html',{'workout':workout,'video':video})

def uploadworkoutvideo(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        video = request.FILES['video']
        titleofvideo = request.POST['titleofvideo']
        dietdescription = request.POST['dietdescription']
        country = request.POST['country']
        day = request.POST['day']
        musclecategory = request.POST['musclecategory']
        muscle = request.POST['muscle']
        level = request.POST['level']
        uploadworkout = Uploadworkoutvideo(user=user, video=video, titleofvideo=titleofvideo,
                                           dietdescription=dietdescription
                                           , country=country, day=day,musclecategory=musclecategory, muscle=muscle, profile=profile,
                                           level=level)
        uploadworkout.save()

    return render(request,'uploadworkoutvideo.html')

def musclevideo(request,id=id):


    if id == None:
        a = 'See Videos For All Workouts'
        video = Uploadworkoutvideo.objects.all().order_by('-id')
    elif id == 1:
        a = 'For Beginner'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(level='Beginner').order_by('-id')

    elif id == 2:
        a = 'For Leg'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Leg').order_by('-id')

    elif id == 3:
        a = 'For Chest'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Chest').order_by('-id')

    elif id == 4:
        a = 'For Shoulder'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Shoulder').order_by('-id')

    elif id == 5:
        a = 'For Triceps'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Triceps').order_by('-id')

    elif id == 6:
        a = 'For Biceps'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Biceps').order_by('-id')

    elif id == 7:
        a = 'For Abs'
        post = Workoutmuscles.objects.all()[13:17]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Abs').order_by('-id')
    return render(request,'workouts.html',{'video':video,'a':a,'post':post})

def musclecategory(request,id=id):
    a = 'See Videos'
    post = Workoutmuscles.objects.all()
    video = Uploadworkoutvideo.objects.all().order_by('-id')

    if request.method == "GET":
        st = request.GET.get('servicename')
        if st != None:
            video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 1:
        a = 'For Lats'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Lats').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 2:
        a = 'For Traps'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Traps').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 3:
        a = 'For Teres Major'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Teres Major').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 4:
        a = 'For Rear Deltoid'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Rear Dealt').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 5:
        a = 'For Infrapinatus'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Infraspinatus').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                a = 'All Workouts'
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 6:
        a = 'For Quads'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Quads').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 7:
        a = 'For Glutes'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Glutes').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 8:
        a = 'For Hamstring'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Hamstring').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 9:
        a = 'For Calf'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Calf').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 10:
        a = 'For Upper Chest'
        post = Workoutmuscles.objects.all()[9:]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Chest').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 11:
        a = 'For Inner Chest'
        post = Workoutmuscles.objects.all()[9:]
        video = Uploadworkoutvideo.objects.filter(muscle='Inner Chest').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 12:
        a = 'For Lower Chest'
        post = Workoutmuscles.objects.all()[9:]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Chest').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 13:
        a = 'For Middle Chest'
        post = Workoutmuscles.objects.all()[9:]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Chest').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 14:
        a = 'For Upper Abs'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Abs').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 15:
        a = 'For Middle Abs'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Abs').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 16:
        a = 'For Lower Abs'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Abs').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 17:
        a = 'For Oblique'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Oblique').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    return render(request,'workouts.html',{'a':a,'post':post,'video':video})


def loginprofile(request,id):
    loguser = Uploadworkoutvideo.objects.get(id=id)

    profile = Profile.objects.get(user=loguser.user)
    a = Uploadworkoutvideo.objects.filter(user=loguser.user)
    bodyweight = Bodyweight.objects.filter(user=loguser.user)
    return render(request,'loginprofile.html',{'a':a,'loguser':loguser,'profile':profile,'bodyweight':bodyweight})

def userprofile(request):
    a = Uploadworkoutvideo.objects.filter(user=request.user)
    bodyweight = Bodyweight.objects.filter(user=request.user)
    return render(request,'profile.html',{'a':a,'bodyweight':bodyweight})



def favourites(request,id):
    video = Uploadworkoutvideo.objects.get(id=id)


    a = Uploadworkoutvideo.objects.filter(ping=request.user)



    if request.user in video.ping.all():
        video.ping.remove(request.user)
    else:
        video.ping.add(request.user)

    return redirect('videodetail',id=id)


def saved(request):
    video = Uploadworkoutvideo.objects.filter(ping=request.user).order_by('-id')
    return render(request,'saved.html',{'video':video})


def edit(request,id):
    video = Uploadworkoutvideo.objects.get(id=id)
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.get(user=user)
        videoedt = request.FILES["edt"]
        titleofvideo = request.POST["titleofvideo"]
        dietdescription = request.POST["dietdescription"]
        country = request.POST["country"]
        day = request.POST["day"]
        musclecategory = request.POST["musclecategory"]
        muscle = request.POST["muscle"]
        level = request.POST["level"]
        if len(videoedt) !=0:
            video.user = user
            video.profile = profile
            video.video = videoedt

            video.titleofvideo = titleofvideo
            video.dietdescription = dietdescription
            video.country = country
            video.day = day
            video.musclecategory = musclecategory
            video.muscle = muscle
            video.level = level





        video.save()
    return render(request,'edit.html',{'video':video})


def follow(request,id):
    loguser = Uploadworkoutvideo.objects.get(id=id)




    #a = Uploadworkoutvideo.objects.filter(user=loguser.user)





    if request.user not in loguser.profile.followings.all():
        loguser.profile.followings.add(request.user)




    #return render(request,'loginprofile.html',{'aa':aa,'profuser':profuser,'loguser':loguser})
    return redirect('loginprofile',id=id)

def unfollow(request,id):
    loguser = Uploadworkoutvideo.objects.get(id=id)
    #following = Profile.objects.get(user=loguser.user)
    #print(following.user)
    #profile = Uploadworkoutvideo.objects.get(id=id)




    #a = Uploadworkoutvideo.objects.filter(user=loguser.user)





    if request.user  in loguser.profile.followings.all() :
        loguser.profile.followings.remove(request.user)




    #return render(request,'loginprofile.html',{'aa':aa,'profuser':profuser,'loguser':loguser})
    return redirect('loginprofile',id=id)


def uploadbodyweight(request):
    if request.method == 'POST':
        user = request.user
        bodyvideo = request.FILES['bodyvideo']
        title = request.POST['title']
        profile = Profile.objects.get(user=request.user)

        bodyweightworkout = Bodyweight(user=user,bodyvideo=bodyvideo,title=title,profile=profile)
        bodyweightworkout.save()
    return render(request,'uploadbodyweight.html')

def selectcategory(request):
    category = Workout.objects.all()[7:]
    a = 'For All'
    workoutvideos = Uploadworkoutvideo.objects.all().order_by('-id')
    return render(request,'selectcategory.html',{'category':category,'workoutvideos':workoutvideos,'a':a})


def musclecategorylevel(request,id):

    if id == None:
        a = 'See Videos For All Workouts'
        workout = Workout.objects.all()[:7]
        video = Uploadworkoutvideo.objects.all().order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)
                a = 'For All'
        return render(request, 'beginner.html', {'a': a, 'workout': workout, 'video': video})

    elif id == 8:
        a = 'For Beginner'
        workout = Workout.objects.all()[:7]

        video = Uploadworkoutvideo.objects.filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)
                a = 'For All'
        return render(request, 'beginner.html', {'a': a, 'workout': workout, 'video': video})

    elif id == 9:
        a = 'For Intermediate'
        workout = Workout.objects.all()[:7]
        video = Uploadworkoutvideo.objects.filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)
                a = 'For All'
        return render(request, 'intermediate.html', {'a': a, 'workout': workout, 'video': video})

    elif id == 10:
        a = 'For Advance'
        workout = Workout.objects.all()[:7]
        video = Uploadworkoutvideo.objects.filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)
                a = 'For All'
        return render(request, 'advance.html', {'a': a, 'workout': workout, 'video': video})

    elif id == 11:
        a = 'For Professional'
        workout = Workout.objects.all()[:7]
        video = Uploadworkoutvideo.objects.filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)
                a = 'For All'
        return render(request,'professional.html',{'a':a,'workout':workout,'video':video})


def musclevideobeginner(request,id):
    if id == None:
        a = 'See Videos For All Workouts'
        video = Uploadworkoutvideo.objects.all().order_by('-id')
    elif id == 1:
        a = 'For Back Beginner'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(level='Beginner').filter(level='Beginner').order_by('-id')

    elif id == 2:
        a = 'For Leg Beginner'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Leg').filter(level='Beginner').order_by('-id')

    elif id == 3:
        a = 'For Chest Beginner'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Chest').filter(level='Beginner').order_by('-id')

    elif id == 4:
        a = 'For Shoulder Beginner'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Shoulder').filter(level='Beginner').order_by('-id')

    elif id == 5:
        a = 'For Triceps Beginner'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Triceps').filter(level='Beginner').order_by('-id')

    elif id == 6:
        a = 'For Biceps Beginner'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Biceps').filter(level='Beginner').order_by('-id')

    elif id == 7:
        a = 'For Abs Beginner'
        post = Workoutmuscles.objects.all()[13:17]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Abs').filter(level='Beginner').order_by('-id')
    return render(request, 'beginner.html', {'video': video, 'a': a, 'post': post})





def musclecategorybeginner(request,id=id):
    a = 'See Videos'
    post = Workoutmuscles.objects.all()
    video = Uploadworkoutvideo.objects.all().order_by('-id')

    if request.method == "GET":
        st = request.GET.get('servicename')
        if st != None:
            video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 1:
        a = 'For Lats Beginner'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Lats').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 2:
        a = 'For Traps Beginner'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Traps').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 3:
        a = 'For Teres Major Beginner'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Teres Major').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 4:
        a = 'For Rear Deltoid Beginner'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Rear Dealt').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 5:
        a = 'For Infrapinatus Beginner'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Infraspinatus').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                a = 'All Workouts'
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 6:
        a = 'For Quads Beginner'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Quads').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 7:
        a = 'For Glutes Beginner'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Glutes').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 8:
        a = 'For Hamstring Beginner'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Hamstring').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 9:
        a = 'For Calf Beginner'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Calf').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 10:
        a = 'For Upper Chest Beginner'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Chest').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 11:
        a = 'For Inner Chest Beginner'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Inner Chest').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 12:
        a = 'For Lower Chest Beginner'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Chest').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 13:
        a = 'For Middle Chest Beginner'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Chest').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 14:
        a = 'For Upper Abs Beginner'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Abs').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 15:
        a = 'For Middle Abs Beginner'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Abs').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 16:
        a = 'For Lower Abs Beginner'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Abs').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 17:
        a = 'For Oblique Beginner'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Oblique').filter(level='Beginner').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    return render(request,'beginner.html',{'a':a,'post':post,'video':video})


def musclevideointermediate(request,id):
    if id == None:
        a = 'See Videos For All Workouts'
        video = Uploadworkoutvideo.objects.all().order_by('-id')
    elif id == 1:
        a = 'For Back Intermediate'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(level='Beginner').filter(level='Intermediate').order_by('-id')

    elif id == 2:
        a = 'For Leg Intermediate'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Leg').filter(level='Intermediate').order_by('-id')

    elif id == 3:
        a = 'For Chest Intermediate'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Chest').filter(level='Intermediate').order_by('-id')

    elif id == 4:
        a = 'For Shoulder Intermediate'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Shoulder').filter(level='Intermediate').order_by('-id')

    elif id == 5:
        a = 'For Triceps Intermediate'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Triceps').filter(level='Intermediate').order_by('-id')

    elif id == 6:
        a = 'For Biceps Intermediate'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Biceps').filter(level='Intermediate').order_by('-id')

    elif id == 7:
        a = 'For Abs Intermediate'
        post = Workoutmuscles.objects.all()[13:17]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Abs').filter(level='Intermediate').order_by('-id')
    return render(request, 'intermediate.html', {'video': video, 'a': a, 'post': post})




def musclecategoryintermediate(request,id=id):
    a = 'See Videos'
    post = Workoutmuscles.objects.all()
    video = Uploadworkoutvideo.objects.all().order_by('-id')

    if request.method == "GET":
        st = request.GET.get('servicename')
        if st != None:
            video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 1:
        a = 'For Lats Intermediate'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Lats').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 2:
        a = 'For Traps Intermediate'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Traps').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 3:
        a = 'For Teres Major Intermediate'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Teres Major').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 4:
        a = 'For Rear Deltoid Intermediate'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Rear Dealt').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 5:
        a = 'For Infrapinatus Intermediate'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Infraspinatus').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                a = 'All Workouts'
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 6:
        a = 'For Quads Intermediate'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Quads').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 7:
        a = 'For Glutes Intermediate'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Glutes').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 8:
        a = 'For Hamstring Intermediate'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Hamstring').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 9:
        a = 'For Calf Intermediate'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Calf').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 10:
        a = 'For Upper Chest Intermediate'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Chest').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 11:
        a = 'For Inner Chest Intermediate'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Inner Chest').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 12:
        a = 'For Lower Chest Intermediate'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Chest').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 13:
        a = 'For Middle Chest Intermediate'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Chest').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 14:
        a = 'For Upper Abs Intermediate'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Abs').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 15:
        a = 'For Middle Abs Intermediate'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Abs').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 16:
        a = 'For Lower Abs Intermediate'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Abs').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 17:
        a = 'For Oblique Intermediate'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Oblique').filter(level='Intermediate').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    return render(request,'intermediate.html',{'a':a,'post':post,'video':video})



def musclevideoinadvance(request,id):
    if id == None:
        a = 'See Videos For All Workouts'
        video = Uploadworkoutvideo.objects.all().order_by('-id')
    elif id == 1:
        a = 'For Back Advance'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(level='Beginner').filter(level='Advance').order_by('-id')

    elif id == 2:
        a = 'For Leg Advance'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Leg').filter(level='Advance').order_by('-id')

    elif id == 3:
        a = 'For Chest Advance'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Chest').filter(level='Advance').order_by('-id')

    elif id == 4:
        a = 'For Shoulder Advance'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Shoulder').filter(level='Advance').order_by('-id')

    elif id == 5:
        a = 'For Triceps Advance'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Triceps').filter(level='Advance').order_by('-id')

    elif id == 6:
        a = 'For Biceps Advance'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Biceps').filter(level='Advance').order_by('-id')

    elif id == 7:
        a = 'For Abs Advance'
        post = Workoutmuscles.objects.all()[13:17]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Abs').filter(level='Advance').order_by('-id')
    return render(request, 'advance.html', {'video': video, 'a': a, 'post': post})


def musclecategoryadvance(request,id=id):
    a = 'See Videos'
    post = Workoutmuscles.objects.all()
    video = Uploadworkoutvideo.objects.all().order_by('-id')

    if request.method == "GET":
        st = request.GET.get('servicename')
        if st != None:
            video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 1:
        a = 'For Lats Advance'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Lats').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 2:
        a = 'For Traps Advance'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Traps').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 3:
        a = 'For Teres Major Advance'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Teres Major').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 4:
        a = 'For Rear Deltoid Advance'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Rear Dealt').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 5:
        a = 'For Infrapinatus Advance'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Infraspinatus').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                a = 'All Workouts'
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 6:
        a = 'For Quads Advance'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Quads').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 7:
        a = 'For Glutes Advance'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Glutes').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 8:
        a = 'For Hamstring Advance'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Hamstring').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 9:
        a = 'For Calf Advance'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Calf').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 10:
        a = 'For Upper Chest Advance'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Chest').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 11:
        a = 'For Inner Chest Advance'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Inner Chest').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 12:
        a = 'For Lower Chest Advance'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Chest').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 13:
        a = 'For Middle Chest Advance'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Chest').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 14:
        a = 'For Upper Abs Advance'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Abs').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 15:
        a = 'For Middle Abs Advance'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Abs').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 16:
        a = 'For Lower Abs Advance'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Abs').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 17:
        a = 'For Oblique Advance'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Oblique').filter(level='Advance').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    return render(request,'advance.html',{'a':a,'post':post,'video':video})



def musclevideoinprofessional(request,id):
    if id == None:
        a = 'See Videos For All Workouts'
        video = Uploadworkoutvideo.objects.all().order_by('-id')
    elif id == 1:
        a = 'For Back Professional'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(level='Beginner').filter(level='Professional').order_by('-id')

    elif id == 2:
        a = 'For Leg Professional'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Leg').filter(level='Professional').order_by('-id')

    elif id == 3:
        a = 'For Chest Professional'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Chest').filter(level='Professional').order_by('-id')

    elif id == 4:
        a = 'For Shoulder Professional'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Shoulder').filter(level='Professional').order_by('-id')

    elif id == 5:
        a = 'For Triceps Professional'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Triceps').filter(level='Professional').order_by('-id')

    elif id == 6:
        a = 'For Biceps Professional'
        post = Workoutmuscles.objects.all()[17:]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Biceps').filter(level='Professional').order_by('-id')

    elif id == 7:
        a = 'For Abs Professional'
        post = Workoutmuscles.objects.all()[13:17]
        video = Uploadworkoutvideo.objects.filter(musclecategory='Abs').filter(level='Professional').order_by('-id')
    return render(request, 'professional.html', {'video': video, 'a': a, 'post': post})



def musclecategoryprofessional(request,id=id):
    a = 'See Videos'
    post = Workoutmuscles.objects.all()
    video = Uploadworkoutvideo.objects.all().order_by('-id')

    if request.method == "GET":
        st = request.GET.get('servicename')
        if st != None:
            video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 1:
        a = 'For Lats Professional'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Lats').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 2:
        a = 'For Traps Professional'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Traps').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 3:
        a = 'For Teres Major Professional'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Teres Major').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 4:
        a = 'For Rear Deltoid Professional'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Rear Dealt').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 5:
        a = 'For Infrapinatus Professional'
        post = Workoutmuscles.objects.all()[:5]
        video = Uploadworkoutvideo.objects.filter(muscle='Infraspinatus').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                a = 'All Workouts'
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 6:
        a = 'For Quads Professional'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Quads').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 7:
        a = 'For Glutes Professional'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Glutes').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 8:
        a = 'For Hamstring Professional'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Hamstring').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 9:
        a = 'For Calf Professional'
        post = Workoutmuscles.objects.all()[5:9]
        video = Uploadworkoutvideo.objects.filter(muscle='Calf').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 10:
        a = 'For Upper Chest Professional'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Chest').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 11:
        a = 'For Inner Chest Professional'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Inner Chest').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 12:
        a = 'For Lower Chest Professional'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Chest').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 13:
        a = 'For Middle Chest Professional'
        post = Workoutmuscles.objects.all()[9:13]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Chest').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 14:
        a = 'For Upper Abs Professional'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Upper Abs').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 15:
        a = 'For Middle Abs Professional'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Middle Abs').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 16:
        a = 'For Lower Abs Professional'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Lower Abs').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    if id == 17:
        a = 'For Oblique Professional'
        post = Workoutmuscles.objects.all()[13:]
        video = Uploadworkoutvideo.objects.filter(muscle='Oblique').filter(level='Professional').order_by('-id')
        if request.method == "GET":
            st = request.GET.get('servicename')
            if st != None:
                video = Uploadworkoutvideo.objects.filter(titleofvideo__icontains=st)

    return render(request,'professional.html',{'a':a,'post':post,'video':video})


def videodetail(request,id):
    video = Uploadworkoutvideo.objects.filter(id=id)[0]

    #b = random.randint(1,1000)

    randomvideo = Uploadworkoutvideo.objects.all()
    vidview = video.viewss + 1
    video_up = Uploadworkoutvideo.objects.filter(id=id).update(viewss=vidview)

    #randomvideoall = random.choice(randomvideo)
    return render(request,'videodetail.html',{'video':video,'randomvideo':randomvideo })


def bodyvideodetail(request, id):
    video = Bodyweight.objects.filter(id=id)[0]

    # b = random.randint(1,1000)

    randomvideo = Bodyweight.objects.all()
    vidview = video.viewss + 1
    video_up = Bodyweight.objects.filter(id=id).update(viewss=vidview)

    # randomvideoall = random.choice(randomvideo)
    return render(request, 'videodetail.html', {'video': video, 'randomvideo': randomvideo})



def bodyweightworkouts(request):
    bodyweightworkout = Bodyweight.objects.all().order_by('-id')
    if request.method == "GET":
        st = request.GET.get('servicenamebodyweight')
        if st != None:
            bodyweightworkout = Bodyweight.objects.filter(title__icontains=st)
    return render(request,'bodyweightworkouts.html',{'bodyweightworkout':bodyweightworkout})


def productprofile(request,id):
    productpostid = Post.objects.get(id=id)
    productpost = Post.objects.filter(user=productpostid.user)
    productvlog = Video.objects.filter(user=productpostid.user)
    #print(productpostid.user)
    #videoid = Video.objects.get(id=id)
    #videopost = Post.objects.filter(user=videoid.user)
    #videovlog = Video.objects.filter(user=videoid.user)
    return render(request,'productprofile.html',{'productpost':productpost,'productvlog':productvlog,'productpostid':productpostid})



def productprofilevlog(request,id):
    productpostid = Video.objects.get(id=id)
    productpost = Post.objects.filter(user=productpostid.user)
    productvlog = Video.objects.filter(user=productpostid.user)
    #print(productpostid.user)
    #videoid = Video.objects.get(id=id)
    #videopost = Post.objects.filter(user=videoid.user)
    #videovlog = Video.objects.filter(user=videoid.user)
    return render(request,'productprofile.html',{'productpost':productpost,'productvlog':productvlog,'productpostid':productpostid})

def userprodprofile(request):
    productpost = Post.objects.filter(user=request.user)
    productvlog = Video.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    return render(request,'productprofile.html',{'productpost':productpost,'productvlog':productvlog,'profile':profile})



def thirtydayhomepage(request):
    thirtydayvideo = Thirtydayworkout.objects.filter(day='Day1').order_by('-id')
    thirtydaypin = Thirtydayworkout.objects.filter(pinthdworkout=request.user).order_by('-id')
    if request.method == "GET":
        st = request.GET.get('servicenamethirtyday')
        if st != None:
            thirtydayvideo = Thirtydayworkout.objects.filter(user__username__icontains=st)
    return render(request,'thirtydayhomepage.html',{'thirtydayvideo':thirtydayvideo,'thirtydaypin':thirtydaypin})




def thirtyday(request,id):


    thirtydayvideo = Thirtydayworkout.objects.get(id=id)
    thirtydayworkout = Thirtydayworkout.objects.filter(user = thirtydayvideo.user )
    #thirtydayworkout = Thirtydayworkout.objects.all().order_by('-id')


    return render(request,'thirtyday.html',{'thirtydayworkout':thirtydayworkout,'thirtydayvideo':thirtydayvideo})






def uploadthirtyday(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        video = request.FILES['video']
        tdwvideotitle = request.POST['tdwvideotitle']
        videodescriptionfortdw = request.POST['videodescriptionfortdw']
        day = request.POST['day']
        uploadworkthirtydayout = Thirtydayworkout(user=user,video=video,tdwvideotitle=tdwvideotitle,videodescriptionfortdw=videodescriptionfortdw,
                                                  day=day,profile=profile)
        uploadworkthirtydayout.save()

    return render(request,'uploadthirtyday.html')



def pinworkout(request,id):
    thirtyday = Thirtydayworkout.objects.get(id=id)
    #following = Profile.objects.get(user=loguser.user)
    #print(following.user)
    #profile = Uploadworkoutvideo.objects.get(id=id)




    #a = Uploadworkoutvideo.objects.filter(user=loguser.user)





    if request.user  in thirtyday.pinthdworkout.all():
        thirtyday.pinthdworkout.remove(request.user)
    else:
        thirtyday.pinthdworkout.add(request.user)




    #return render(request,'loginprofile.html',{'aa':aa,'profuser':profuser,'loguser':loguser})
    return redirect('thirtyday',id=id)











