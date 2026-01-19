from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.conf import settings


AVATAR_CHOICES = [
    ('apple.svg', _('Manzana')),
    ('asparagus.svg', _('Espárrago')),
    ('bacon.svg', _('Bacon')),
    ('banana.svg', _('Plátano')),
    ('beet.svg', _('Remolacha')),
    ('bread.svg', _('Pan')),
    ('cabbage.svg', _('Col')),
    ('celery.svg', _('Apio')),
    ('cheese.svg', _('Queso')),
    ('cherry.svg', _('Cereza')),
    ('cupcake.svg', _('Magdalena')),
    ('default.svg', _('Avatar por defecto')),
    ('eggs.svg', _('Huevos')),
    ('garlic.svg', _('Ajo')),
    ('hamburger.svg', _('Hamburguesa')),
    ('hazelnut.svg', _('Avellana')),
    ('honey.svg', _('Miel')),
    ('hops.svg', _('Lúpulo')),
    ('kiwi.svg', _('Kiwi')),
    ('kohlrabi.svg', _('Colinabo')),
    ('leek.svg', _('Puerro')),
    ('lettuce.svg', _('Lechuga')),
    ('macaron.svg', _('Macaron')),
    ('melon.svg', _('Melón')),
    ('milk.svg', _('Leche')),
    ('nachos.svg', _('Nachos')),
    ('nut.svg', _('Nuez')),
    ('octopus.svg', _('Pulpo')),
    ('pancake.svg', _('Tortita')),
    ('peanuts.svg', _('Cacahuetes')),
    ('pear.svg', _('Pera')),
    ('peas.svg', _('Guisantes')),
    ('pie.svg', _('Tarta')),
    ('pineapple.svg', _('Piña')),
    ('pizza.svg', _('Pizza')),
    ('plum.svg', _('Ciruela')),
    ('pomegranate.svg', _('Granada')),
    ('potato.svg', _('Patata')),
    ('radish.svg', _('Rábano')),
    ('raspberry.svg', _('Frambuesa')),
    ('sesame.svg', _('Sésamo')),
    ('steak.svg', _('Filete')),
    ('strawberry.svg', _('Fresa')),
    ('taco.svg', _('Taco')),
    ('tapas.svg', _('Tapas')),
    ('thanksgiving.svg', _('Acción de gracias')),
    ('tomato.svg', _('Tomate')),
    ('watermelon.svg', _('Sandía')),
]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=[('reader', 'Reader'), ('author', 'Author')], default='reader')
    avatar = models.CharField(max_length=100, choices=AVATAR_CHOICES, default='default.svg')
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        try:
            
            old_avatar = CustomUser.objects.get(pk=self.pk).avatar
        except CustomUser.DoesNotExist:
            old_avatar = None

        super().save(*args, **kwargs)

    def get_avatar_url(self):
        return f'{settings.MEDIA_URL}avatars/{self.avatar or "default.svg"}'


class UserProfile(TranslatableModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    last_checked_comments = models.DateTimeField(null=True, blank=True)
    translations = TranslatedFields(
        bio = models.TextField(blank=True, null=True),
    )
    

class Contact(models.Model):
    nombre = models.CharField(
        verbose_name=_('Nombre'),
        max_length=50
    )
    email = models.EmailField(
        verbose_name=_('Email')
    )
    comentario = models.TextField(
        verbose_name=_('Comentario que ha dejado en la web')
    )
    created_at = models.DateTimeField(
        verbose_name=_('Fecha y hora de creación'),
        default=timezone.now
    )
    contactado = models.BooleanField(
        verbose_name=_('¿Se ha contactado con él?'),
        default=False
    )

    def __str__(self):
        return self.nombre