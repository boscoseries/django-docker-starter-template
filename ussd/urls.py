from rest_framework import routers
from django.urls import path, include
from .views import USSDViewsets

router = routers.DefaultRouter()

app_name = "ussd"

router.register("callback", USSDViewsets)

urlpatterns = router.urls