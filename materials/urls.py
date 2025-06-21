from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('upload/', views.upload_material, name='upload'),
    path('list/', views.material_list, name='list'),
]
