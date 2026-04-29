from rest_framework.routers import DefaultRouter
from .views import PaymentRecoveryViewSet

router = DefaultRouter()

router.register(
    "",
    PaymentRecoveryViewSet,
    basename="billing"
)

urlpatterns = router.urls