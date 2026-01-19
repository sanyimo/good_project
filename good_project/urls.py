from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from views.core_views import HomeView, LegalView, PrivacyView, ContactView, SearchView


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
] #+ debug_toolbar_urls()


urlpatterns += i18n_patterns ( 
    path("", HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path(_('accounts/'), include('urls.accounts_urls')),
    path(_('recipes/'), include('urls.recipes_urls')),
    path("legal/", LegalView.as_view(), name="legal"),
    path(_("privacy/"), PrivacyView.as_view(), name="privacy"),
    path(_('search/'), SearchView.as_view(), name='search'), 
    path(_("contact/"), ContactView.as_view(), name="contact"), 
)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if 'rosetta' in settings.INSTALLED_APPS:
#     urlpatterns += [
#         path('rosetta/', include('rosetta.urls')),
#     ]
