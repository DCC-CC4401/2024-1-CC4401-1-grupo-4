from django.urls import path
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register', views.register_user, name='register_user'),
    # path('logout',views.logout_user, name='logout'),
    path('forum', views.forum, name='forum'),
    path('message', views.publish_message, name='message'),
	path('profile', views.profile, name='profile'),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)