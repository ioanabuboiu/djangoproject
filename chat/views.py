from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm

# Create your views here.


def home(request):
    return render(request, "home.html")


def room(request, room):
    username = request.user.username
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.user.username
    if not Room.objects.filter(name=room).exists():
        new_room = Room.objects.create(name=room)
        new_room.save()
    return redirect("/" + room + '/?username=' + username)


def send(request):
    print(request.POST['message'])
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']
    print(username)
    if request.method == 'POST':
        new_message = Message.objects.create(value=message, user=request.user, room=room_id)
        new_message.save()
    #     print("please work")
    #     uploaded_file = request.FILES['myfile']
    #     fs = FileSystemStorage()
    #     name = fs.save(uploaded_file.name, uploaded_file)
    #     url = fs.url(name)
    #     print(url)
    # image = url
    # if image is not None:
    #     new_message = Message.objects.create(value=message, user=username, room=room_id)
    # else:
    #     new_message = Message.objects.create(value=message, user=username, room=room_id, image=image)
    # new_message.save()
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


class MessageList(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = context['messages'].filter(user=self.request.user)
        return context


User = get_user_model()

# Create your views here.
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            user = User.objects.create_user(username, email, password)
        except:
            user = None
        if user is not None:
            login(request, user)  # request.user == user
            return redirect("/login")
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] += 1
            # return redirect("/invalid-password")
        else:
            request.session['invalid_user'] = 1
    return render(request, "forms.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)  # request.user == user
            return redirect("/")
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] += 1
            # return redirect("/invalid-password")
        else:
            request.session['invalid_user'] = 1
    return render(request, "forms.html", {"form": form})


def logout_view(request):
    logout(request)  # request.user == anonymous
    return redirect("/login")

