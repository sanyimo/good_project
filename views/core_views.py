from random import randint, sample
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _, get_language
from django.views.generic import FormView, TemplateView
from accounts.models import AVATAR_CHOICES, Contact
from forms.account_forms import ContactForm
from forms.recipes_forms import SearchForm
from recipes.models import Category, Recipe
from utils.search_recipes import search_recipes
from views.recipes_views import CATEGORY_IMAGES


class HomeView(TemplateView):
    template_name = "general/home.html"  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        featured_recipes = Recipe.objects.filter(featured=True).exclude(photo='').order_by('?')[:4]
        for recipe in featured_recipes:
            recipe.rotacion = randint(-5, 5) #type: ignore

        context['recipes'] = featured_recipes 
        
        all_categories = list(Category.objects.all())
        featured_categories = sample(all_categories, min(8, len(all_categories)))

        for cat in featured_categories:
            filename = CATEGORY_IMAGES.get(cat.image_code, 'default.jpg') #type: ignore
            cat.image_url = f"/static/img/{filename}" #type: ignore

        context['featured_categories'] = featured_categories
        
        user = self.request.user
        if user.is_authenticated and user.avatar == 'default.svg': #type: ignore
            context['show_avatar_modal'] = True
            
            avatar_choices = [choice for choice in AVATAR_CHOICES if choice[0] != 'default.svg']
            context['avatar_choices'] = avatar_choices
        else:
            context['show_avatar_modal'] = False
            
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context
    
class LegalView(TemplateView):
    template_name = "general/aviso-legal.html"
    
    
class PrivacyView(TemplateView):
    template_name = "general/privacy.html"
    

class SearchView(FormView):
    template_name = "general/search.html"
    form_class = SearchForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET  # clave para que form.is_valid() funcione
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        results = None
        filters_applied = []
        
        if form.is_valid():
            has_filters = any(v for k, v in form.cleaned_data.items() if v not in [None, '', []])
            if has_filters:
                results = search_recipes(form.cleaned_data)
                
            # calculamos filtros aplicados
            lang = get_language()
            for field, value in form.cleaned_data.items():
                if value in [None, '', [], False] or field == 'q':
                    continue

                # Si es un queryset, listamos sus nombres
                if hasattr(value, 'all'):
                    names = [
                        item.safe_translation_getter('name', language_code=lang).capitalize()
                        for item in value.all()
                    ]
                    filters_applied.extend(names)
                # Booleanos
                elif isinstance(value, bool) and value:
                    filters_applied.append(field.replace('_', ' ').capitalize())
                # Otros tipos (texto, número, etc.)
                elif isinstance(value, str):
                    filters_applied.append(value.capitalize())
        
        return self.render_to_response(self.get_context_data(form=form, results=results, filters_applied=filters_applied))  


class ContactView(FormView):
    template_name = "general/contact.html"
    form_class = ContactForm
    
    def get_success_url(self):
        return self.request.path 
    
    def form_valid(self, form):
        nombre = form.cleaned_data['nombre']
        email = form.cleaned_data['email']
        comentario = form.cleaned_data['comentario']
        message_content = f'{nombre} con email {email} ha enviado el siguiente comentario: {comentario}'

        Contact.objects.create(
            nombre=nombre,
            email=email,
            comentario=comentario
        )
        
        send_mail(
            'Formulario de contacto de mi web',
            message_content,
            #'sanyimo@gmail.com',
            settings.DEFAULT_FROM_EMAIL,            
            ['bastetcolin@gmail.com'],
            fail_silently=False,
        )
        
        messages.success(self.request, _("¡Gracias por tu mensaje! Te responderemos pronto."))

        return super().form_valid(form)