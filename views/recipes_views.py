import random
from django.db import transaction
from django.db.models import Avg, Count
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.translation import gettext_lazy as _, get_language
from django.shortcuts import get_object_or_404, render,  redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import ValidationError
from parler.utils.context import switch_language
from recipes.models import TRANSLATION_LANGS, Category, Comment,  Favorite,  Rating, Recipe, CuisineType
from forms.recipes_forms import RecipeForm, CommentForm, get_recipe_ingredient_formset
from utils.helpers import format_quantity, get_current_theme_slugs, process_ingredients_formset, save_photo_if_exists, save_recipe_object
from utils.translation import   handle_translations_for_recipe


class RecipeListView(ListView):
    model = Recipe
    template_name = 'core/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Top recetas mejor valoradas (average_rating anotado)
        top_recipes = (
            Recipe.objects
            .annotate(avg_rating=Avg('ratings__score'))
            .filter(avg_rating__gte=4)
            .order_by('-avg_rating')[:10]
        )
        context['top_recipes'] = top_recipes

        # Recetas recientes (las más nuevas)
        recent_recipes = Recipe.objects.all().order_by('-created_at')[:10]
        context['recent_recipes'] = recent_recipes

        # Recetas fáciles (por campo difficulty)
        easy_recipes = Recipe.objects.filter(difficulty='easy').order_by('?')[:10]
        context['easy_recipes'] = easy_recipes

        # Cocina más popular según número de recetas
        popular_cuisine = (
            CuisineType.objects
            .annotate(num_recipes=Count('recipes'))
            .order_by('-num_recipes')
            .first()
        )
        context['popular_cuisine'] = popular_cuisine
        
        if popular_cuisine:
            cuisine_recipes = Recipe.objects.filter(cuisine_type=popular_cuisine).order_by('?')[:10]
        else:
            cuisine_recipes = []
        context['cuisine_recipes'] = cuisine_recipes
        
        # Popular = recetas más favoritas
        popular_recipes = (
            Recipe.objects
            .annotate(num_favorites=Count('favorited_by'))
            .filter(num_favorites__gt=0)
            .order_by('?')[:10]
        )
        context['popular_recipes'] = popular_recipes
        
        language = get_language()

        current_theme_slugs = get_current_theme_slugs()
        
        from recipes.signals import translations
        theme_names = []
        for slug in current_theme_slugs:
            if slug in translations.get(language, {}).get('themes', {}):
                theme_name = translations[language]['themes'][slug]
                theme_names.append(theme_name)
        
        actualidad_recipes = Recipe.objects.none()
        
        if current_theme_slugs:
            actualidad_recipes = (
                Recipe.objects.filter(
                    themes__translations__name__in=theme_names,
                    themes__translations__language_code=language
                )
                .distinct()
                .order_by('?')[:10]
            )
        
        context['actualidad_recipes'] = actualidad_recipes
        context['theme_name'] = theme_names[0] if theme_names else translations[language]['themes'].get(current_theme_slugs[-1], '')

        return context

def recipe_detail(request, slug):
    current_lang = get_language()
    try:
        recipe = Recipe.objects.prefetch_related(
            'recipe_ingredients__ingredient',
            'recipe_ingredients__unit',
            'meal_types',
            'cooking_methods',
            'tags',
            'themes',
            'allergens',
            'ratings',
        ).select_related(
            'author',
            'category',
            'cuisine_type'
        ).get(translations__slug=slug)
    except Recipe.DoesNotExist:
        raise Http404(_("Receta no encontrada en el idioma actual."))
    
    with switch_language(recipe, current_lang):
        translated_slug = recipe.slug #type: ignore

    if translated_slug and translated_slug != slug:
        return redirect('recipes:recipe_detail', slug=translated_slug)

    # Traducciones seguras
    title = recipe.safe_translation_getter("title", any_language=True)
    description = recipe.safe_translation_getter("description", any_language=True)
    instructions = recipe.safe_translation_getter("instructions", any_language=True)
    tips = recipe.safe_translation_getter("tips", any_language=True)

    # Ingredientes traducidos
    ingredients = []
    for ri in recipe.recipe_ingredients.all():  # type: ignore
        ingredients.append({
            'quantity': format_quantity(ri.quantity),
            'unit': ri.unit,
            'ingredient_name': ri.ingredient.safe_translation_getter("name", any_language=True)
        })
    total_votes = recipe.ratings.count() # type: ignore
    average = recipe.ratings.aggregate(avg=Avg('score'))['avg'] or 0
    full_slices = int(average)  # trozos completos
    half_slice = 1 if (average - full_slices) >= 0.5 else 0
    empty_slices = 5 - full_slices - half_slice

    recommended_recipes = []
    if recipe.category:
        recommended_recipes = Recipe.objects.filter(
            category=recipe.category
        ).exclude(id=recipe.id).order_by('?')[:4] # type: ignore
    
    is_favorited = False
    selected_rating = None
    if request.user.is_authenticated:
        is_favorited = recipe.favorited_by.filter(user=request.user).exists()  # type: ignore
        rating = recipe.ratings.filter(user=request.user).first()  # type: ignore
        selected_rating = rating.score if rating else None
        
    context = {
        'recipe': recipe,
        'title': title,
        'description': description,
        'instructions': instructions,
        'tips': tips,
        'image': recipe.photo,
        'ingredients': ingredients,
        'author': recipe.author,
        'category': recipe.category,
        'cuisine_type': recipe.cuisine_type,
        'prep_time': recipe.prep_time,
        'cook_time': recipe.cook_time,
        'servings': recipe.servings,
        'difficulty': recipe.get_difficulty_display(), # type: ignore
        'meal_types': recipe.meal_types.all(),
        'tags': recipe.tags.all(),
        'themes': recipe.themes.all(),
        'cooking_methods': recipe.cooking_methods.all(),
        'allergens': recipe.allergens.all(),
        'slug_translated': recipe.safe_translation_getter('slug', any_language=True),
        'average_rating': recipe.average_rating,
        'total_time': recipe.total_time,
        'total_votes': total_votes,
        'full_slices': range(full_slices),
        'half_slice': half_slice,
        'empty_slices': range(empty_slices),
        'recommended_recipes': recommended_recipes,
    }

    comment_form = CommentForm()
    comments = recipe.comments.select_related('user').filter(parent__isnull=True)  # type: ignore

    context.update({
        'comments': comments,
        'comment_form': comment_form,
        'is_favorited': is_favorited,
        'selected_rating': selected_rating,
    })

    return render(request, 'core/recipe_detail.html', context)


CATEGORY_INTROS = {
    1: _(
        "Descubre recetas de carnes jugosas y sabrosas, ideales para quienes "
        "aman un buen plato contundente."
    ),
    2: _(
        "Saborea lo mejor del mar con nuestros platos de pescados y mariscos, "
        "frescos, delicados y llenos de tradición."
    ),
    3: _( 
        "Deléitate con nuestras recetas de pasta, cargadas de sabor y hechas "
        "para disfrutar en cualquier ocasión."
    ),
    4: _(
        "Siente el calor de nuestras sopas y cremas, reconfortantes y hechas "
        "con ingredientes naturales."
    ),
    5: _(
        "Prueba nuestras ensaladas frescas y coloridas, perfectas para comidas "
        "ligeras y llenas de vida."
    ),
    6: _(
        "Date un capricho con nuestros postres irresistibles, el broche de oro "
        "para cualquier comida especial."
    ),
    7: _(
        "Explora nuestra selección de arroces, desde las recetas clásicas que "
        "te reconfortan hasta las más creativas para sorprender a todos."
    ),
    8: _(
        "Descubre recetas vegetarianas llenas de sabor, color y creatividad, "
        "para comer bien y saludable."
    ),
}

CATEGORY_IMAGES = {
    1: 't-bone.webp',
    2: 'pescado.webp',
    3: 'pasta.webp',
    4: 'sopa-campesina.webp',
    5: 'ensalada-mediterranea.webp',
    6: 'postres.webp',
    7: 'arroz-salteado.webp',
    8: 'calabacines.webp',
}

class CategoryDetailView(ListView):
    model = Recipe
    template_name = "core/category_detail.html"
    context_object_name = "recipes"

    def get_queryset(self):
        slug = self.kwargs['slug']
        language = self.request.LANGUAGE_CODE #type: ignore

        # Obtenemos la categoría traducida según el idioma
        category = get_object_or_404(
            Category.objects.language(language), #type: ignore
            translations__slug=slug
        )
        self.category = category  # guardamos para el context

        return Recipe.objects.language(language).filter( #type: ignore
            category=category,
            photo__isnull=False
        ).exclude(photo='')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["intro"] = CATEGORY_INTROS.get(self.category.image_code, "")
        
        filename = CATEGORY_IMAGES.get(self.category.image_code, 'default.jpg')
        context["category_image_url"] = f"/static/img/optimized/{filename}"
        context["hide_page_title"] = True
        
        return context
    

class RecipeCreateView(LoginRequiredMixin,CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'core/recipe_create.html'    
    success_url = reverse_lazy('recipes:recipe_detail')
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        RecipeIngredientFormSet= get_recipe_ingredient_formset(extra=3)

        if 'ingredient_formset' in kwargs:
            context['ingredient_formset'] = kwargs['ingredient_formset']
        else:
            context['ingredient_formset'] = RecipeIngredientFormSet(prefix="ingredients") 

        return context       

    @transaction.atomic
    def form_valid(self, form):
        RecipeIngredientFormSet = get_recipe_ingredient_formset(extra=3)
        
        self.object = save_recipe_object(form, self.request) 

        save_photo_if_exists(self.object, form)

        formset = RecipeIngredientFormSet(self.request.POST, instance=self.object, prefix="ingredients")
        if not formset.is_valid():
            return self.form_invalid(form, formset)

        process_ingredients_formset(formset, get_language()[:2])
        formset.save()
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'redirect_url': str(self.get_success_url()),
                'message': _("Receta creada con éxito."),
                'status': 'success',
            })

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        url = reverse_lazy('recipes:recipe_detail', kwargs={'slug': self.object.slug})
        return url
   
    def form_invalid(self, form, formset=None):
        RecipeIngredientFormSet = get_recipe_ingredient_formset(extra=3)
    
        formset = formset or RecipeIngredientFormSet(self.request.POST, instance=form.instance, prefix="ingredients")
        context = self.get_context_data(form=form, ingredient_formset=formset)
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors_html = render_to_string('_includes/_form_errors.html', context, request=self.request)
            return JsonResponse({
                'status': 'error',
                'errors_html': errors_html,
                'message': _("Por favor, corrige los errores del formulario."),
            }, status=400)
           
        return self.render_to_response(context)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'core/recipe_update.html'
    
    def get_ingredient_formset(self):
        RecipeIngredientFormSet = get_recipe_ingredient_formset(extra=0)

        if hasattr(self, '_ingredient_formset'):
            return self._ingredient_formset

        if self.request.method == 'POST':
            self._ingredient_formset = RecipeIngredientFormSet(self.request.POST, instance=self.object, prefix="ingredients")
        else:
            self._ingredient_formset = RecipeIngredientFormSet(instance=self.object, prefix="ingredients")

        return self._ingredient_formset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['ingredient_help_text'] = _('Asegúrate de no dejar campos vacíos. Si sobran, elimínalos con el botón "Cancelar".')
        context['ingredient_formset'] = self.get_ingredient_formset()
        return context
        
    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            obj = Recipe.objects.language(self.request.LANGUAGE_CODE).get(translations__slug=slug) #type: ignore
        except Recipe.DoesNotExist:
            raise Http404(_("Receta no encontrada"))
        return obj

    def form_valid(self, form):
        original_data = {field: getattr(self.get_object(), field) for field in ['title', 'description', 'instructions', 'tips']}

        self.object = save_recipe_object(form, self.request, is_update=True)

        formset = self.get_ingredient_formset()

        if not formset.is_valid():
            return self.form_invalid(form, formset)
        
        process_ingredients_formset(formset, get_language()[:2])
        formset.save()

        handle_translations_for_recipe(self.object, get_language()[:2], original_data=original_data)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': _("Receta actualizada con éxito."),
                'redirect_url': reverse_lazy('recipes:recipe_detail', kwargs={'slug': self.object.slug}),
            })
        
        # Para peticiones normales (no AJAX) añadimos el mensaje a Django
        messages.success(self.request, _("Receta actualizada con éxito."))

    def get_success_url(self):
        url = reverse_lazy('recipes:recipe_detail', kwargs={'slug': self.object.slug})
        return url

    def form_invalid(self, form, formset=None):

        context = self.get_context_data(form=form)
        if formset:
            context['ingredient_formset'] = formset
            
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors_html = render_to_string('_includes/_form_errors.html', context, request=self.request)
            return JsonResponse({
                'status': 'error',
                'errors_html': errors_html,
                'message': _("Por favor, corrige los errores del formulario."),
            }, status=400)
        
        return self.render_to_response(context)
        
    def test_func(self):
        obj = self.get_object()
        result = obj.author == self.request.user  #type: ignore
        return result


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:recipe_list')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        # Buscamos el objeto usando el slug en la tabla de traducciones (django-parler)
        return get_object_or_404(
            Recipe.objects.language(self.request.LANGUAGE_CODE),  # type: ignore
            translations__slug=slug
        )
        
    def delete(self, request, *args, **kwargs):
        current_lang = translation.get_language()

        response = super().delete(request, *args, **kwargs)
        with translation.override(current_lang):
            messages.success(request, _("🗑️ Receta eliminada correctamente."))
        return response

    def test_func(self):
        recipe = self.get_object()
        return recipe.author == self.request.user #type: ignore

@login_required
def rate_recipe(request, slug):
    recipe = get_object_or_404(Recipe.objects.language(request.LANGUAGE_CODE), translations__slug=slug) #type: ignore
    
    try:
        rating_value = int(request.POST.get("rating", 0))
    except (ValueError, TypeError):
        messages.error(request, _("Valoración inválida."))
        return redirect("recipes:recipe_detail", slug=slug)

    if rating_value < 1 or rating_value > 5:
        messages.error(request, _("La puntuación debe estar entre 1 y 5."))
        return redirect("recipes:recipe_detail", slug=slug)
    
    if recipe.author == request.user:
        messages.error(request, _("No puedes valorar tu propia receta."))
        return redirect("recipes:recipe_detail", slug=slug)

    # Actualiza o crea la valoración
    Rating.objects.update_or_create(
        recipe=recipe,
        user=request.user,
        defaults={"score": rating_value}
    )
    
    messages.success(request, _(f"⭐ Valoraste con {rating_value} estrella(s)."))
    return redirect("recipes:recipe_detail", slug=slug)


@login_required
def add_comment(request, slug):
    recipe = get_object_or_404(
        Recipe.objects.language(request.LANGUAGE_CODE), #type: ignore
        translations__slug=slug
    )
    
    parent_id = request.POST.get("parent_id")
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id)

    form = CommentForm(request.POST, user=request.user, recipe=recipe, parent=parent)

    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.parent = parent

            try:
                comment.full_clean()
                comment.save()
                messages.success(request, _("🗨️ Comentario añadido correctamente."))
            except ValidationError as e:
                for msg in e.messages:
                    messages.error(request, msg)
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error) #type: ignore

    return redirect('recipes:recipe_detail', slug=slug)


def random_recipe_json(request):
    recipes = Recipe.objects.all()
    if recipes.exists():
        recipe = random.choice(recipes)
        return JsonResponse({
            "title": recipe.title, #type: ignore
            "image_url": recipe.photo.url,
            "url": recipe.get_absolute_url(),
        })
    return JsonResponse({"error": "No recipes available."}, status=404)

@require_POST
@login_required
def toggle_favorite(request):
    slug = request.POST.get("slug")
    if not slug:
        return JsonResponse({"error": "Missing slug"}, status=400)

    try:
        recipe = get_object_or_404(Recipe, translations__slug=slug)
    except Exception as e:
        return JsonResponse({"error": "Recipe not found or error: " + str(e)}, status=404)

    user = request.user

    try:
        favorite, created = Favorite.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            favorite.delete()
            return JsonResponse({"status": "removed"})
        else:
            return JsonResponse({"status": "added"})
    except Exception as e:
        return JsonResponse({"error": "Database error: " + str(e)}, status=500)