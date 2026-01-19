import requests
import logging
import html 
from parler.utils.context import switch_language
from utils.html_cleaner import clean_translated_html
from recipes.models import TRANSLATION_LANGS, Ingredient
from .helpers import generate_unique_slug
from recipes.models import Recipe
import os

TRANSLATE_API_URL = os.getenv("TRANSLATE_API_URL", "https://libretranslate.de/translate")

def translate_text(text, source_lang, target_lang):
    try:
        response = requests.post(
            TRANSLATE_API_URL,
            json={
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'html'
            },
            timeout=10
        )
        if response.status_code == 200:
            translated = response.json().get("translatedText", text)
            return html.unescape(translated)
        else:
            logging.warning(f"Translation error [{response.status_code}]: {response.text}")
            return text  # Devolver original si falla

    except Exception as e:
        logging.error(f"Error translating to {target_lang}: {e}")
        return text  # Devolver original si falla
    
def translate_recipe(recipe, source_lang, target_lang, fields=None, original_data=None):
    if source_lang == target_lang:
        return

    if fields is None:
        fields = ['title', 'description', 'instructions', 'tips']

     # Determinar si es create o update
    force_translate = original_data is None

    if force_translate:
        # CREATE: obtener valores originales en source_lang
        with switch_language(recipe, source_lang):
            original_data = {field: getattr(recipe, field, '') for field in fields}
    else:
        # UPDATE: solo traducir si se está editando en source_lang
        if recipe.get_current_language() != source_lang:
            # Guardar cambios en ese idioma sin traducir
            with switch_language(recipe, target_lang):
                for field in fields:
                    setattr(recipe, field, getattr(recipe, field, ''))
                recipe.save()
            return

    translated_data = {}

    for field in fields:
            new_value = getattr(recipe, field, '')
            old_value = original_data.get(field, '')

            if force_translate or new_value != old_value:
                if not new_value:
                    translated_data[field] = ''
                elif field == 'title':
                    translated_data[field] = translate_text(new_value, source_lang, target_lang)
                else:
                    translated_data[field] = clean_translated_html(translate_text(new_value, source_lang, target_lang))
            else:
                # En update, mantener traducción existente
                with switch_language(recipe, target_lang):
                    translated_data[field] = getattr(recipe, field, '')
                    
    with switch_language(recipe, target_lang):
        for field in fields:
            setattr(recipe, field, translated_data.get(field, ''))
        if 'title' in fields:
            recipe.slug = generate_unique_slug(Recipe, translated_data.get('title', ''), target_lang)
        recipe.save()

def get_or_create_translated_ingredient(ingredient, source_lang):
    with switch_language(ingredient, source_lang):
        source_name = ingredient.name
    
    for lang in TRANSLATION_LANGS:
        if lang == source_lang:
            continue

        # Cambiar idioma para asignar la traducción
        with switch_language(ingredient, lang):
            if ingredient.has_translation(lang) and  ingredient.name:
                continue
            # Traducir usando texto original
            translated_name = translate_text(source_name, source_lang, lang)

            ingredient.name = translated_name
            ingredient.slug = generate_unique_slug(Ingredient, translated_name, lang)
            ingredient.save_translations()
            ingredient.save()

    return ingredient

def translate_ingredients(recipe, source_lang, target_langs):
    for ri in recipe.recipe_ingredients.all():
        ingredient = ri.ingredient
        get_or_create_translated_ingredient(ingredient, source_lang)

def handle_translations_for_recipe(recipe, source_lang, original_data=None):
    target_langs = [lang for lang in TRANSLATION_LANGS if lang != source_lang]
    for lang in target_langs:
        translate_recipe(recipe, source_lang, lang, original_data=original_data)
    translate_ingredients(recipe, source_lang, target_langs)