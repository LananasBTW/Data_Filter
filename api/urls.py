from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('load/', views.load_file, name='load_file'),
    path('save/', views.save_file, name='save_file'),
    path('filter/', views.filter_data, name='filter_data'),
    path('sort/', views.sort_data, name='sort_data'),
    path('stats/', views.get_stats, name='get_stats'),
]