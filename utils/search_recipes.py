from django.db.models import Q
from django.utils.translation import get_language
from recipes.models import Recipe

def search_recipes(cleaned_data):
    q_text = cleaned_data.get('q')
    current_lang = get_language()
    qs = Recipe.objects.all()

    # búsqueda por texto
    if q_text:
        qs = qs.filter(
            Q(translations__language_code=current_lang, translations__title__icontains=q_text) |
            Q(ingredients__translations__language_code=current_lang, ingredients__translations__name__icontains=q_text) |
            Q(category__translations__language_code=current_lang, category__translations__name__icontains=q_text)
        )

    # dificultad
    if cleaned_data.get('difficulty'):
        qs = qs.filter(difficulty=cleaned_data['difficulty'])

    # tiempo de preparación
    if cleaned_data.get('prep_time_min') is not None:
        qs = qs.filter(prep_time__gte=cleaned_data['prep_time_min'])
    if cleaned_data.get('prep_time_max') is not None:
        qs = qs.filter(prep_time__lte=cleaned_data['prep_time_max'])

    # categorías
    if cleaned_data.get('category'):
        qs = qs.filter(category__in=cleaned_data['category'])

    # ingredientes: debe contener todos los seleccionados
    if cleaned_data.get('ingredients'):
        for ing in cleaned_data['ingredients']:
            qs = qs.filter(ingredients=ing)

    # meal_types y cooking_methods
    if cleaned_data.get('meal_types'):
        qs = qs.filter(meal_types__in=cleaned_data['meal_types'])
    if cleaned_data.get('cooking_methods'):
        qs = qs.filter(cooking_methods__in=cleaned_data['cooking_methods'])

    # alérgenos: excluir recetas que contengan cualquiera de los seleccionados
    if cleaned_data.get('allergens'):
        for allergen in cleaned_data['allergens']:
            qs = qs.exclude(allergens=allergen)
            
    if cleaned_data.get('tags'):
        for tag in cleaned_data['tags']:
            qs = qs.filter(tags=tag)

    if cleaned_data.get('cuisine_type'):
        qs = qs.filter(cuisine_type__in=cleaned_data['cuisine_type'])

    return qs.distinct()