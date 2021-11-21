from django.urls import path
from .views import VistaDireccion, VistaPersona, VistaVivienda, VistaFeedback, EnviarDireccion, EnviarPersona, EnviarVivienda, EnviarFeedback, ImprimirDatos
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('direccion/',VistaDireccion,name = "direccion"),
    path('enviarDireccion/',EnviarDireccion,name = "enviarDireccion"),
    
    path('persona/',VistaPersona,name = "persona"),
    path('enviarPersona/',EnviarPersona,name = "enviarPersona"),
    
    path('vivienda/',VistaVivienda,name = "vivienda"),
    path('enviarVivienda/',EnviarVivienda,name = "enviarVivienda"),
    
    path('feedback/',VistaFeedback,name = "feedback"),
    path('enviarFeedback/',EnviarFeedback,name = "enviarFeedback"),
    
    path('consulta/',ImprimirDatos,name = "consulta"),
]



urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)