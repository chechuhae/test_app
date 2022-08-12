# from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('creation/', views.CreationView.as_view(), name='creation'),
    path('<str:username>/password_change/',
         views.PasswordChangeView.as_view(),
         name='password_change'),
    path('login/password_reset/',
         auth_views.PasswordResetView.as_view(
             success_url=reverse_lazy('account:password_reset_done'),
             template_name='account/password_reset.html',
             subject_template_name='account/password_reset_subject.txt',
             email_template_name='account/password_reset_email.html',
         ),
         name='password_reset'),
    path('login/password_reset/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html',
             success_url=reverse_lazy('account:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('login/password_reset/password_reset_done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('login/password_reset/password_reset_complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html',
         ),
         name='password_reset_complete'),
    path('<str:username>_profile/', views.ProfileView.as_view(), name='profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
