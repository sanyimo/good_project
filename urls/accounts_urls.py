from django.urls import path, reverse_lazy
from views.accounts_views import RegisterView, UserProfileView, delete_profile, CustomPasswordChangeView, set_avatar_view
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _

app_name = 'accounts'

urlpatterns = [
    path(_('register/'), RegisterView.as_view(), name='register'),
    path(_('login/'), auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path(_('logout/'), auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path(_('set-avatar/'), set_avatar_view, name='set_avatar'),
    path(_('profile/'), UserProfileView.as_view(), name='profile'),
    path(_('profile/delete/'), delete_profile, name='delete_profile'),
    path(_('profile/password-change/'), CustomPasswordChangeView.as_view(), name='password_change'),
    path(_('password-reset/'), auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]