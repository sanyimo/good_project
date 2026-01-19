from parler.managers import TranslatableQuerySet
from parler.utils.context import switch_language
from django.db import models
from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.utils.text import slugify
from django.urls import reverse_lazy
from parler.managers import TranslatableManager
    
TRANSLATION_LANGS = ['es', 'en', 'it', 'ca', 'hu', 'pt']

class RecipeQuerySet(TranslatableQuerySet):
    def with_average_rating(self):
        return self.annotate(average_rating=Avg('ratings__score'))
    
    def top_rated(self, min_score=4):
        return self.with_average_rating().filter(average_rating__gte=min_score)
    
    def recent(self, limit=5):
        return self.order_by('-created_at')[:limit]
    
    def by_difficulty(self, difficulty):
        return self.filter(difficulty=difficulty)
    
    def with_tag(self, tag_slug):
        return self.filter(tags__slug=tag_slug)
    
    def by_cuisine(self, cuisine_slug):
        return self.filter(cuisine_type__translations__slug=cuisine_slug)
    
    def published(self):
        return self.active_translations().filter(is_published=True)


class RecipeManager(TranslatableManager):
    def get_queryset(self) -> 'RecipeQuerySet':
        return RecipeQuerySet(self.model, using=self._db)
    
    def with_average_rating(self) -> 'RecipeQuerySet':
        return self.get_queryset().with_average_rating()
    
    def top_rated(self, min_score=4) -> 'RecipeQuerySet':
        return self.get_queryset().top_rated(min_score)
    
    def recent(self, limit=5) -> 'RecipeQuerySet':
        return self.get_queryset().recent(limit)
    
    def by_difficulty(self, difficulty) -> 'RecipeQuerySet':
        return self.get_queryset().by_difficulty(difficulty)
    
    def with_tag(self, tag_slug) -> 'RecipeQuerySet':
        return self.get_queryset().with_tag(tag_slug)
    
    def by_cuisine(self, cuisine_slug) -> 'RecipeQuerySet':
        return self.get_queryset().by_cuisine(cuisine_slug)
    
    def published(self) -> 'RecipeQuerySet':
        return self.get_queryset().published()

    
class CuisineType(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100),
        slug=models.SlugField(max_length=200, blank=True, null=True, allow_unicode=True),
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Sin tipo de cocina"
    
    class Meta:
        verbose_name = _('Tipo de cocina')
        verbose_name_plural = _("Tipos de cocina")


class MealType(TranslatableModel):
    slug = models.SlugField(unique=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=100)
    ) # desayuno, almuerzo, cena, snack

    def save(self, *args, **kwargs):
        if not self.slug:
            name = self.safe_translation_getter('name', any_language=True) or ''
            base_slug = slugify(str(name))
            slug = base_slug
            counter = 1
            ModelClass = self.__class__
            qs = ModelClass.objects.get_queryset()
            while qs.translated(slug=slug).exclude(pk=self.pk).exists():  # type: ignore
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return str(self.safe_translation_getter('name', any_language=True) or "Sin tipo de comida")

class Difficulty(models.TextChoices):
    EASY = 'easy', _('Fácil')
    MEDIUM = 'medium', _('Medio')
    HARD = 'hard', _('Difícil')
    
    
class Tag(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=50),
        slug = models.SlugField(max_length=100, blank=True, null=True, allow_unicode=True)
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Sin etiqueta'

    class Meta:
        verbose_name = _("Etiqueta")
        verbose_name_plural = _("Etiquetas")
        
        
class Theme(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100),
        slug = models.SlugField(max_length=100, unique=True, allow_unicode=True),
        description = models.TextField(blank=True),
    )

    class Meta:
        verbose_name = _("Tema")
        verbose_name_plural = _("Temas")

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Sin tema'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        # Generar los slugs faltantes por idioma
        for lang_code, _ in self.get_available_languages():
            with switch_language(self, lang_code):
                if not self.slug and self.name: # type: ignore
                    self.slug = slugify(self.name, allow_unicode=True) # type: ignore
                    super().save(update_fields=['slug'])
    
       
class Recipe(TranslatableModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes', related_query_name='recipes')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='recipes')
    cooking_methods = models.ManyToManyField('CookingMethod', blank=True, related_name='recipes')
    allergens = models.ManyToManyField('Allergen', blank=True, related_name='recipes')
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    
    prep_time = models.PositiveIntegerField(help_text=_('Tiempo de preparación en minutos'))
    cook_time = models.IntegerField(default=0, blank=True, null=False, help_text=_('Tiempo de cocción en minutos'))
    servings = models.PositiveIntegerField(help_text=_('Número de porciones'), default=1)
    meal_types = models.ManyToManyField(MealType, blank=True, related_name='recipes')
    cuisine_type = models.ForeignKey(CuisineType, null=True, blank=True, on_delete=models.SET_NULL, related_name='recipes')
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes')
    photo = models.ImageField(upload_to='recipes/photos/', blank=True, null=True)
    themes = models.ManyToManyField(Theme, blank=True, related_name='recipes')
    featured = models.BooleanField(default=False, verbose_name=_("Destacada"))

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes'
    )
    
    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        slug=models.SlugField(max_length=200, blank=True, null=True, allow_unicode=True),
        description=HTMLField(blank=True),
        tips = HTMLField(blank=True),
        instructions=models.TextField(blank=True),
    )
    source_lang = models.CharField(
        max_length=5,
        choices=[(lang, lang) for lang in TRANSLATION_LANGS],
        default='es', 
    )
    
    created_at = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Fecha de actualización'), auto_now=True)
    
    objects: RecipeManager = RecipeManager()

    class Meta:
        verbose_name = _("Receta")
        verbose_name_plural = _("Recetas")
        ordering = ['-created_at']

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)
    
    def get_absolute_url(self):
        return reverse_lazy("recipes:recipe_detail", kwargs={"slug": self.safe_translation_getter('slug', any_language=True)})
        
    @property
    def average_rating(self):
        if hasattr(self, 'avg_rating'):
            return self.avg_rating or 0 # type: ignore
        
        if hasattr(self, '_average_rating_cache'):
            return self._average_rating_cache
        
        avg = self.ratings.aggregate(avg_score=Avg('score'))['avg_score'] or 0  # type: ignore
        self._average_rating_cache = avg
        return avg

    @property
    def total_time(self):
        prep = self.prep_time or 0
        cook = self.cook_time or 0
        return prep + cook
    
    @property
    def total_votes(self):
        return self.ratings.count() # type: ignore

    @property
    def ingredients_list(self):
        return self.recipe_ingredients.select_related('ingredient', 'unit').order_by('order') # type: ignore
 
    
class Category(TranslatableModel):
    image_code = models.IntegerField(null=True, blank=True, unique=True)

    translations = TranslatedFields(
        slug=models.SlugField(max_length=200, blank=True, null=True, allow_unicode=True),
        name=models.CharField(max_length=100)
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Sin categoría"
    
    class Meta:
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")
        #ordering = ['name']


class CookingMethod(TranslatableModel):
    translations = TranslatedFields(
        slug=models.SlugField(max_length=200, blank=True, null=True, allow_unicode=True),
        name=models.CharField(max_length=100)
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Sin preparación"
    
    class Meta:
        verbose_name = _("Tipo de preparación")
        verbose_name_plural = _("Tipos de preparación")
        

class Allergen(TranslatableModel):
    translations = TranslatedFields(
        slug=models.SlugField(max_length=200, blank=True, null=True, allow_unicode=True),
        name=models.CharField(max_length=100)
    )

    icon = models.ImageField(upload_to='allergens/icons/', blank=True, null=True)
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Sin alérgeno"
    
    class Meta:
        verbose_name = _("Alérgeno")
        verbose_name_plural = _("Alérgenos")


class Ingredient(TranslatableModel):
    category = models.ForeignKey(
        'IngredientCategory', 
        null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name='ingredients'
    )
    translations = TranslatedFields(
        slug=models.SlugField(max_length=200, blank=True, null=True, allow_unicode=True),
        name=models.CharField(max_length=100)
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Sin ingrediente"
    
    class Meta:
        verbose_name = _("Ingrediente")
        verbose_name_plural = _("Ingredientes")


class IngredientCategory(TranslatableModel):
    slug = models.SlugField(unique=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=100)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            name = self.safe_translation_getter('name', any_language=True) or ''
            base_slug = slugify(str(name))
            slug = base_slug
            counter = 1
            ModelClass = self.__class__
            qs = ModelClass.objects.get_queryset()
            while qs.translated(slug=slug).exclude(pk=self.pk).exists():  # type: ignore
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.safe_translation_getter('name', any_language=True) or "Sin categoría")
    

class Unit(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=50)
    )

    abbreviation = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Sin unidad"
    class Meta:
        verbose_name = _("Unidad")


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='ingredient_recipes')

    quantity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL, related_name='recipe_ingredients')

    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Ingrediente")
        verbose_name_plural = _("Ingredientes")
        ordering = ['order']
        unique_together = ('recipe', 'ingredient')

    def __str__(self) -> str:
        unit_name = self.unit.safe_translation_getter('name', any_language=True) if self.unit else ''
        return f"{self.quantity or ''} {unit_name} {self.ingredient}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _(f"Comentario de {self.user} en {self.recipe}")

    class Meta:
        verbose_name = _("Comentario")
        ordering = ['-created_at']
        
    def is_reply(self):
        return self.parent is not None
    
    def clean(self):
        if len(self.content) < 10:
            raise ValidationError(_("El comentario debe tener al menos 10 caracteres."))
        if len(self.content) > 300:
            raise ValidationError(_("El comentario debe tener menos de 300 caracteres."))


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    SCORE_CHOICES = [(i, str(i)) for i in range(1,6)]
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)  # por ejemplo 1 a 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Valoración")
        unique_together = ('user', 'recipe') 

    def __str__(self):
        return f"{self.score} estrellas por {self.user} en {self.recipe}"

    def clean(self):
        if self.score < 1 or self.score > 5:
            raise ValidationError(_("La puntuación debe estar entre 1 y 5."))
        if self.recipe.author == self.user:
            raise ValidationError(_("No puedes valorar tu propia receta."))
        
        
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user} favorito {self.recipe}"