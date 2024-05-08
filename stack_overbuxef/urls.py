from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register', views.register_user, name='register_user'),
    # path('logout',views.logout_user, name='logout'),
    # path('forum',views.logout_user, name='forum'),
    path('message',views.publish_message, name='message'),
]