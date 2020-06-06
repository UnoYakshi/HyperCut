from django.urls import path

from .views import IndexView, URLView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', URLView.as_view(), name='detail')
]
