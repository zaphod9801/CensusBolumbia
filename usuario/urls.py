from django.urls import path
from .views import login, registro
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .forms import loginForm

urlpatterns = [
    path('registro/',registro,name = "registro"),
    path('',login,name = "login"),
    path('quit/',LogoutView.as_view(template_name='login.html'),name = "quit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)