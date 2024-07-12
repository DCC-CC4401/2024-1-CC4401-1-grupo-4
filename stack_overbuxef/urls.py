from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register', views.register_user, name='register_user'),
    # path('logout',views.logout_user, name='logout'),
    path('forum', views.forum, name='forum'),
    path('message', views.publish_message, name='message'),
    path('admin/', admin.site.urls),
    path('consults/<int:consult_id>/', views.modalAnswers, name='answers'),
    path('makeAnswer/<int:consult_id>/', views.makeModalAnswer, name='makeAnswer'),
	path('deleteComment/<int:consult_id>/', views.deleteComment, name='deleteComment'),
	path('deleteReply/<int:reply_id>/', views.deleteReply, name='deleteReply'),
	path('tags', views.tags, name='tags'),
	path('delete_tag/<int:tag_id>/', views.deleteTag, name='delete_tag')
]