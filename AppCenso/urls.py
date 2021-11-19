from django.urls import path
from .views import VistaDireccion, VistaPersona, VistaVivienda, VistaFeedback, VistaPersona2
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('direccion/',VistaDireccion,name = "direccion"),
    path('persona/',VistaPersona,name = "persona"),
    path('persona2/',VistaPersona2,name = "persona2"),
    path('vivienda/',VistaVivienda,name = "vivienda"),
    path('feedback/',VistaFeedback,name = "feedback"),
]



urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)