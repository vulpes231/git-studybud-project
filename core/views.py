from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from django.contrib.auth.decorators import login_required


from .forms import RoomForm, UserForm, MyUserCreationForm


# MAIN PAGE
def main(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))



    context = {'rooms':rooms, 'topics': topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'core/main.html', context)


# SHOW ROOM
def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    

    # create comment
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


    context = {'room': room, 'messages': messages, 'participants':participants}
    return render(request, 'core/room.html', context)


# USER PROFILE

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = user.message_set.all()

    context = {'user':user, 'rooms': rooms, 'topics':topics, 'room_messages': room_messages}
    return render(request, 'core/profile.html', context)


# CREATE ROOM
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('main')

    context = { 'form': form }
    return render(request, 'core/room_form.html', context)



# UPDATE ROOM
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # CHECK IF ITS THE AUTHOR 
    if request.user != room.host:
        return HttpResponse("You're can only moderate your rooms!!")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('main')

    return render(request, 'core/room_form.html', {'form': form})


# DELETE ROOM
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    # CHECK IF ITS THE AUTHOR 
    if request.user != room.host:
        return HttpResponse("Not allowed!!")


    if request.method == "POST":
        room.delete()
        return redirect('main')
    return render(request, 'core/delete.html', {'obj': room})


def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')



# DELETE MESSAGES
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    # CHECK IF ITS THE AUTHOR 
    if request.user != message.user:
        return HttpResponse("Not allowed")


    if request.method == "POST":
        message.delete()
        return redirect('main')
    return render(request, 'core/delete.html', {'obj': message})


# UPDATE USER
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)


    context = {'form':form}
    return render(request, 'core/update-user.html', context)