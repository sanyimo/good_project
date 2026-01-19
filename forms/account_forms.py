from django import forms
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm
from django.contrib.auth.forms import UserCreationForm
from accounts.models import AVATAR_CHOICES, CustomUser, UserProfile

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=50, label=_("Nombre"))
    email = forms.EmailField(label=_("Correo electrónico"))
    comentario = forms.CharField(max_length=1000, label=_("Comentario"), widget=forms.Textarea)
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) < 5:
            raise forms.ValidationError(_("El nombre debe tener al menos 5 caracteres"))
        return nombre

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and "prueba" in email:
            raise forms.ValidationError(_("El email no parece ser correcto"))
        return email


class CustomUserCreationForm(UserCreationForm):   
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'})
    )

    # Re-declarar password fields para poder aplicar widgets
    password1 = forms.CharField(
        label=_('Contraseña'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label=_('Repetir contraseña'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'autocomplete': 'email'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'autocomplete': 'new-password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'autocomplete': 'new-password'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Este email ya está registrado."))
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'reader'  # rol por defecto
        user.avatar = 'default.svg'
        if commit:
            user.save()
        return user


class CustomUserForm(forms.ModelForm):
    avatar = forms.ChoiceField(
        choices=AVATAR_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'avatar-radio'}),
        label=_("Avatar")
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'avatar']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['avatar'].choices = [
            choice for choice in AVATAR_CHOICES if choice[0] != 'default.svg'
        ]


class UserProfileForm(TranslatableModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control', 'placeholder': _('Cuéntanos algo sobre ti...')
            }),
        }