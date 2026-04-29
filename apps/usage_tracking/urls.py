from rest_framework.routers import DefaultRouter
from .views import UsageRecordViewSet

router = DefaultRouter()

router.register(
    "",
    UsageRecordViewSet,
    basename="usage-tracking"
)

urlpatterns = router.urls