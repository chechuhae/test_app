from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'friends'
urlpatterns = [
    path('<str:username>/my_friend_list/',
         views.MyFriendList.as_view(),
         name='my_friend_list'),
    path('<str:username>/my_friend_request/',
         views.MyFriendRequestList.as_view(),
         name='my_friend_request'),
    path('<str:username>/my_sent_request/',
         views.MySentFriendRequestList.as_view(),
         name='my_sent_request'),
    path('<str:username>/my_friend_request/<int:pk>/decline_friend_request',
         views.DeclineFriendRequestView.as_view(),
         name='decline_friend_request'),
    path('<str:username>/my_friend_list/<int:pk>/accept_friend_request',
         views.AcceptFriendRequestView.as_view(),
         name='accept_friend_request'),
    path('<str:username>/my_friend_request/<int:pk>/delete_friend',
         views.DeleteFriendView.as_view(),
         name='delete_friend'),
    path('user_search/',
         views.AllUsersSearchView.as_view(),
         name='user_search'),
    path('send_friend_request/<int:pk>',
         views.SendFriendRequestUserView.as_view(),
         name='send_friend_request'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
