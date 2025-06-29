from django.urls import path

from . import views
from .views import upload_resi

urlpatterns = [

    path('table/jawa/', views.table_jawa, name='table_jawa'),
    path('table/luar-jawa/', views.table_luar_jawa, name='table_luar-jawa'),
]
    

