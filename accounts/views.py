from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import LoginForm, RegisterForm

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
            return redirect("/posts")
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] += 1
            # return redirect("/invalid-password")
        else:
            request.session['invalid_user'] = 1
    return render(request, "forms.html", {"form": form})


def logout_view(request):
    logout(request)  # request.user == anonymous
    return redirect("/login")
