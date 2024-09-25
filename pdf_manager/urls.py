from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download_pdf, name='download_pdf'),
    path('pdf_parser/', views.pdf_parser, name='pdf_parser'),
    path('regex_extractor/', views.regex_extractor, name='regex_extractor'),
]