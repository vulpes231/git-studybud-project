from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm





def loginPage(request):

    page = 'login'
    # CHECK IF USER IS LOGGED IN
    if request.user.is_authenticated:
        return redirect('main')

    # GET USERNAME
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

    # CHECK IF USER EXISTS IN DB
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist!')

    # IF USER EXIST CHECK IF CREDENTIALS MATCH AN EXISTING ONE IN DB  
        user = authenticate(request, username=username, password=password)

    # IF CREDENTIALS MATCH THEN LOGIN USER TO HOMEPAGE
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'username OR password incorrect!')
    context = {'page': page}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('main')


def registerUser(request):
    page = 'register'

    # CREATE FORM INSTANCE
    form = UserCreationForm()

    # CHECK FORM METHOD
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        # CHECK IF DATA IS VALID
        if form.is_valid():
            user = form.save(commit=False)

            # CLEAN DATA AND SAVE USER TO DB
            user.username = user.username.lower()
            user.save()


            # LOGIN USER
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'An error occured during registration.')


    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)