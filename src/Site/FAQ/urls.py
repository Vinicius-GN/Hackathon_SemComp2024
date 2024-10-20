from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('faqapp.urls')),  # Direciona a URL raiz para as URLs do faqapp
]
