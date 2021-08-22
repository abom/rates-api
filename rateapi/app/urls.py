from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

VERSION = "1"

urlpatterns = [
    path(f"api/v{VERSION}/quotes/", views.rate_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)
