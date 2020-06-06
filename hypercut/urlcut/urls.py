from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from .views import IndexView, URLView, ShortURLRedirectView, AllURLsView, RemoveURLView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    re_path(r'^(?P<short_url>[0-9a-zA-Z]+)/$', ShortURLRedirectView.as_view(), name='redirect'),
    path('detail/<int:pk>/', URLView.as_view(), name='detail'),
    path('all-list/', AllURLsView.as_view(), name='all-list'),
    path('rm/<int:pk>/', csrf_exempt(RemoveURLView.as_view()), name='remove')
]
