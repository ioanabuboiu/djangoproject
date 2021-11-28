from msilib.schema import ListView
from chat.models import Room, Message
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView

# Create your views here.

def home(request):
    return render(request, "home.html")


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    if not Room.objects.filter(name=room).exists():
        new_room = Room.objects.create(name=room)
        new_room.save()
    return redirect("/"+room+'/?username='+username)


def send(request):
    print(request.POST['message'])
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    if request.method == 'POST':
        print("please work")
        uploaded_file = request.FILES['myfile']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        print(url)
    image = url
    if image is not None:
        new_message = Message.objects.create(value=message, user=username, room=room_id)
    else:
        new_message = Message.objects.create(value=message, user=username, room=room_id, image=image)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    messages = messages.values()
    return JsonResponse({"messages": list(messages)})


def getPosts(request):
    user = request.user
    posts = Message.objects.filter(user=user.id)
    posts = posts.values()
    return JsonResponse({"messages": list(posts)})
