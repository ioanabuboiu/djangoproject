from django.urls import path

from . import views
from .views import MessageList

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    # path("", views.home, name="home"),
    path('<str:room>/', views.room, name="room"),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name="getMessages"),
    path("", MessageList.as_view(), name="messages"),


]
