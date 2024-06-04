from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'tables', TableViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'bills', BillViewSet)
router.register(r'tables_restaurants', TablesRestaurantViewSet)

urlpatterns = router.urls