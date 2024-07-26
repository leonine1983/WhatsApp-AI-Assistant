from django.contrib import admin
from django.urls import path
from contatos import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('enviar_whatsapp/', views.enviar_whatsapp, name='enviar_whatsapp'),
    path('', views.perfil_mensage, name='perfil_mensage'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
