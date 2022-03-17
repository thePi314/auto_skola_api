from django.urls import re_path as url

#from api.views.auth import AuthenticationView
from api.views.health import HealthCheckView


urlpatterns = [
    # Auth
    #url(r"^auth/?$", AuthenticationView.as_view(), name="auth"),
    url(r"^health/?$", HealthCheckView.as_view(), name='health_check')
]

