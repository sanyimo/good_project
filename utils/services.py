import unicodedata
from django.utils.text import slugify

def normalize_text(text: str) -> str:
    """Normaliza un texto: sin tildes, minúsculas, sin espacios extra."""
    text = text.strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text

def generate_unique_slug(model, value, language_code):
    clean_value = normalize_text(value)
    base_slug = slugify(clean_value, allow_unicode=False)
    slug = base_slug
    counter = 1
    while model.objects.language(language_code).filter(translations__slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug