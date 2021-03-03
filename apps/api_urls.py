# Third Party Stuff
from django.urls import path
from rest_framework.routers import DefaultRouter

# Talana Stuff
from apps.base.api.routers import SingletonRouter
from apps.raffle.api import GetWinner
from apps.users.api import CurrentUserViewSet
from apps.users.auth.api import AuthViewSet

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register("auth", AuthViewSet, basename="auth")
singleton_router.register("me", CurrentUserViewSet, basename="me")

urlpatterns = [
    path("get_winner", GetWinner.as_view(), name="get_winner"),
]

# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns += default_router.urls + singleton_router.urls
