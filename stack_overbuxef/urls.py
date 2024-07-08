from django.urls import include,path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register', views.register_user, name='register_user'),
    # path('logout',views.logout_user, name='logout'),
    path('forum',views.forum, name='forum'),
    path('message',views.publish_message, name='message'),
    path("admin/", admin.site.urls),
    path("select2/", include("django_select2.urls")),
]