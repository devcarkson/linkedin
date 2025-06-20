from django.urls import path
from . import views
from . views import *
from django.views.i18n import set_language

urlpatterns = [
    path('', views.index, name='index'),
    path('set_language/', set_language, name='set_language'),
    # path('', include('core.urls')),
]