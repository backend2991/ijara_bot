
from django.contrib import admin
from django.urls import path

from apps.views import create_user, dashboard, succes, base, login, logout
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',create_user, name='register'),
    path('create_user/', create_user,name='create_user'),
    path('succes/', succes, name='succes'),
    path('dashboard/', dashboard, name='dashboard'),
# ===================================================================
    path('', base, name='base'),
    path('login/', login, name='login'),
    path('', logout, name='logout')

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)