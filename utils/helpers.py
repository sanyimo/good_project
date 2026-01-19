from fractions import Fraction
from datetime import date, timedelta
from django.utils.timezone import now
from parler.utils.context import switch_language
from utils.services import generate_unique_slug
from utils.translation import get_or_create_translated_ingredient, handle_translations_for_recipe
from recipes.models import Ingredient, Recipe
from django.utils.translation import get_language

def format_quantity(qty):
    qty_float = float(qty)  # Convertir Decimal a float para usar is_integer()
    if qty_float.is_integer():
        return str(int(qty_float))
    frac = Fraction(qty_float).limit_denominator(8)
    if frac.numerator == 0:
        return '0'
    if frac.numerator > frac.denominator:
        whole = frac.numerator // frac.denominator
        remainder = Fraction(frac.numerator % frac.denominator, frac.denominator)
        if remainder == 0:
            return str(whole)
        return f"{whole} {remainder}"
    else:
        return str(frac)

# ejemplo
format_quantity(2.5)  # '2 1/2'
format_quantity(0.5)  # '1/2'
format_quantity(0.25) # '1/4'
format_quantity(1.0)  # '1'

def save_recipe_object(form, request, is_update=False):
    recipe = form.save(commit=False)
    recipe.author = request.user
    
    source_lang = get_language()[:2]
    recipe.set_current_language(source_lang)

    if not is_update and request.user.role == 'reader':  # type: ignore
       request.user.role = 'author'   # type: ignore
       request.user.save()
       
    # Guardar datos originales si es update (para traducciones diferenciales)
    original_data = None
    if is_update:
        original_data = {
            field: getattr(recipe, field)
            for field in ['title', 'description', 'instructions', 'tips']
        }

    if not is_update or 'title' in form.changed_data:
        recipe.slug = generate_unique_slug(Recipe, recipe.title, source_lang)
        
    recipe.save()
    form.save_m2m()
    
    # Generar traducciones y slugs para otros idiomas
    handle_translations_for_recipe(recipe, source_lang, original_data=original_data)
    return recipe

def save_photo_if_exists(obj, form):
    photo = form.cleaned_data.get('photo')
    if photo:
        obj.photo = photo
        obj.save()
        
def process_ingredients_formset(formset, source_lang):
    for form_ingredient in formset:
        if form_ingredient.cleaned_data and not form_ingredient.cleaned_data.get('DELETE', False):
            name = (form_ingredient.cleaned_data.get('ingredient_name') or '').strip()
            if not name:
                continue
            ingredient = Ingredient.objects.filter(translations__name=name).first()
            if not ingredient:
                ingredient = Ingredient.objects.create()
                with switch_language(ingredient, source_lang):
                    setattr(ingredient, "name", name)
                    setattr(ingredient, "slug", generate_unique_slug(Ingredient, name, source_lang))
                    ingredient.save()
            
            get_or_create_translated_ingredient(ingredient, source_lang)
            form_ingredient.instance.ingredient = ingredient

def calcular_pascua(year):
    """Algoritmo de Meeus para calcular la fecha de Pascua (domingo)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def get_current_theme_slugs():
    today = now().date()
    year = today.year
    slugs = []

    # Fechas muy señaladas (1 mes antes)
    fechas_mes = {
        'navidad': date(year, 12, 25),
        'halloween': date(year, 10, 31),
        'nochevieja': date(year, 12, 31),
    }
    for slug, fecha in fechas_mes.items():
        if fecha - timedelta(days=30) <= today <= fecha:
            slugs.append(slug)

    # Fechas puntuales (1 semana antes)
    fechas_semana = {
        'san-valentin': date(year, 2, 14),
        'dia-del-padre': date(year, 3, 19),
        'dia-de-la-madre': date(year, 5, 5),
    }
    for slug, fecha in fechas_semana.items():
        if fecha - timedelta(days=7) <= today <= fecha:
            slugs.append(slug)

    # Fechas móviles:
    pascua = calcular_pascua(year)

    # Carnaval → 47 días antes de Pascua (Lunes de Carnaval)
    carnaval = pascua - timedelta(days=47)
    if carnaval - timedelta(days=30) <= today <= carnaval:
        slugs.append('carnaval')

    # Semana Santa → semana antes de Pascua
    semana_santa = pascua - timedelta(days=7)
    if semana_santa - timedelta(days=30) <= today <= pascua:
        slugs.append('semana-santa')

    # Estaciones
    primavera_start = date(year, 3, 21)
    verano_start = date(year, 6, 21)
    otono_start = date(year, 9, 23)
    invierno_start = date(year, 12, 21)

    if primavera_start <= today < verano_start:
        estacion ='primavera'
    elif verano_start <= today < otono_start:
        estacion = 'verano'
    elif otono_start <= today < invierno_start:
        estacion = 'otono'
    else:
        # si no está en primavera/verano/otoño, es invierno.
        estacion = 'invierno'
        
    slugs.append(estacion) #estacion siempre la última
    return slugs