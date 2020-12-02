from rest_framework import routers
from .views import UserViewsets

router = routers.DefaultRouter()

app_name = "user"

router.register("", UserViewsets)

urlpatterns = router.urls