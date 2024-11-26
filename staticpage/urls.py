from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getData/', views.getData, name='getData'),
    path('updatePageSize/', views.update_page_size, name='updatePageSize'),
    path('getUrls/', views.getUrls, name='getUrls'),
    path('getOriginText/', views.getOriginText, name='getOriginText'),
    path('askAI/', views.askAI, name='askAI'),
    path('outPutResult/', views.outPutResult, name='outPutResult'),
    path('download/', views.download_file, name='download_file'),  # /download/
]