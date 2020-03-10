from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wall import views
from django.contrib.auth.models import User
from knox import views as knox_views
from wall.views import Regsitration, Login



# Create a router and register our viewsets with it.
router = DefaultRouter()


router.register(r'message', views.MessageViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api/auth', include('knox.urls')),
    path('register', Regsitration.as_view()),
    path('login', Login.as_view())
]
