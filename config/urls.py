"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from apps.pages.views import upload_resi
from apps.pages import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='pages/login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.index, name='index'),
    path('', include('apps.pages.urls')),
    path('', include('apps.dyn_dt.urls')),
    path('', include('apps.dyn_api.urls')),
    path('charts/', include('apps.charts.urls')),
    path("admin/", admin.site.urls),
    path('upload-resi/', upload_resi, name='upload-resi'),
    path("", include('admin_adminlte.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
