from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'communication'
urlpatterns = [
    path('<str:username>/my_messages/', views.MyDirectMessageView.as_view(), name='my_messages'),
    path('my_messages/dialogue_<str:dialogue_with>/', views.MyDialogueView.as_view(), name='my_dialogue'),
    # path('<str:username>/dm_to_<str:friend>/', views.DirectMessageView.as_view(), name='dm_to_friend'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
