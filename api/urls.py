from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from api.views import MealViewSet,RatingViewSet

router=routers.DefaultRouter()
router.register('meals',MealViewSet)
router.register('ratings',RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
