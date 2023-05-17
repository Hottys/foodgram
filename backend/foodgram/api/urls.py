from django.urls import include, path

from api.v1.urls import v1_urlpatterns

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]