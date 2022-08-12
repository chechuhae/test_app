# from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

app_name = 'testApp'
urlpatterns = [
    path('', views.FirstView.as_view(), name='index'),
    path('profile/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.to_main, name='home'),
    path('<str:username>/my_questions/', views.MyQuestionView.as_view(), name='my_questions'),
    path('<str:username>/my_questions/add_question/', views.AddQuestionView.as_view(), name='add_question'),
    path('<str:username>/my_questions/<int:pk>/add_choice/',
         views.AddChoiceView.as_view(),
         name='add_choice'),
    path('<str:username>/my_questions/<int:pk>/update_question/',
         views.UpdateMyQuestionView.as_view(),
         name='update_question'),
    path('<str:username>/my_questions/<int:pk>/delete_question/',
         views.DeleteMyQuestionView.as_view(),
         name='delete_question'),
    path('<str:username>/my_questions/<int:pk>/update_choice/',
         views.UpdateChoiceView.as_view(),
         name='update_choice'),
    path('<str:username>/my_questions/<int:pk>/delete_choice/',
         views.DeleteChoiceView.as_view(),
         name='delete_choice'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
