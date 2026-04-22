from django.urls import path
from . import views

urlpatterns = [
    path('',              views.index,       name='index'),
    path('about/',        views.about,       name='about'),
    path('education/',    views.education,   name='education'),
    path('results/',      views.results,     name='results'),
    path('admission/',    views.admission,   name='admission'),
    path('media/',        views.media_hub,   name='media_hub'),
    path('news/',         views.news_list,   name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('gallery/',      views.gallery,     name='gallery'),
    path('contacts/',     views.contacts,    name='contacts'),
    path('healthz/',      views.healthz,     name='healthz'),
]
