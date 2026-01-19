import os
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import View, CreateView

from accounts.models import AVATAR_CHOICES, UserProfile
from forms.account_forms import CustomUserCreationForm, CustomUserForm, UserProfileForm
from recipes.models import Comment, Favorite, Rating, Recipe

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login') 
    
    def form_valid(self, form):
        messages.success(self.request, _("Registro completado. Ahora puedes iniciar sesión."))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Por favor, corrige los errores."))
        return super().form_invalid(form)


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        user_form = CustomUserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        password_change_form = PasswordChangeForm(user=user)
        
        my_recipes = Recipe.objects.language(request.LANGUAGE_CODE).filter(author=user)  # type: ignore
        # Dentro de get_context_data de UserProfileView o del que maneje "Mi perfil":
        user_ratings = Rating.objects.filter(user=user).select_related("recipe").order_by("-created_at")

        favorite_qs = Favorite.objects.filter(user=user).select_related('recipe')
        last_checked = profile.last_checked_comments or now()

        my_comments = Comment.objects.filter(user=user, parent__isnull=True).select_related("recipe").order_by("-created_at")
        
        new_replies_to_my_comments = Comment.objects.filter(
            parent__user=user
        ).exclude(user=user).filter(created_at__gt=last_checked)

        replies_to_my_comments = Comment.objects.filter(
            parent__user=user
        ).exclude(user=user).select_related("recipe", "user", "parent").order_by("-created_at")

        new_comments_on_my_recipes = Comment.objects.filter(
            recipe__author=user,
            parent__isnull=True
        ).exclude(user=user).filter(created_at__gt=last_checked)

        comments_on_my_recipes = Comment.objects.filter(
            recipe__author=user,
            parent__isnull=True
        ).exclude(user=user).select_related("recipe", "user").order_by("-created_at")

        # Guardar nuevo last_checked
        profile.last_checked_comments = now()
        profile.save(update_fields=['last_checked_comments'])

        return render(request, 'accounts/user_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_change_form': password_change_form,
            'my_recipes': my_recipes,
            "my_comments": my_comments,
            "replies_to_my_comments": replies_to_my_comments,
            "comments_on_my_recipes": comments_on_my_recipes,
            "new_replies_to_my_comments": new_replies_to_my_comments,
            "new_comments_on_my_recipes": new_comments_on_my_recipes,
            "has_new_replies": new_replies_to_my_comments.exists(),
            "has_new_comments": new_comments_on_my_recipes.exists(),
            "user_ratings": user_ratings,
            "favorites": [fav.recipe for fav in favorite_qs],
            'avatar_choices': AVATAR_CHOICES,
        })

    def post(self, request):
        user = request.user
        profile, created  = UserProfile.objects.get_or_create(user=user)
        user_form = CustomUserForm(request.POST, request.FILES, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        password_change_form = PasswordChangeForm(user=user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Perfil actualizado correctamente.")) 
            return redirect('accounts:profile')

        return render(request, 'accounts/user_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_change_form': password_change_form
        })

@require_POST
@login_required
def delete_profile(request):
    user = request.user
    # Eliminar avatar si existe
    if user.avatar:
        if os.path.isfile(user.avatar.path):
            os.remove(user.avatar.path)
    user.delete()
    logout(request)
    return redirect('home')


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')  # vuelve al perfil tras cambiar
    success_message = _("Tu contraseña ha sido actualizada correctamente.")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    

@login_required
def set_avatar_view(request):
    if request.method == 'POST':
        avatar = request.POST.get('avatar')
        valid_avatars = [choice[0] for choice in AVATAR_CHOICES ]
        if avatar in valid_avatars and avatar != 'default.svg':
            user = request.user
            user.avatar = avatar
            user.save()
            messages.success(request, _("Avatar actualizado correctamente."))
        else:
            messages.error(request, _("Selección de avatar no válida."))

    return redirect('home')  