from django.urls import path

from .views import IndexView, URLView, ShortURLRedirectView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:short_url>/', ShortURLRedirectView.as_view(), name='redirect'),
    path('<int:pk>/', URLView.as_view(), name='detail')
]
