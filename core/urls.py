from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ExpenseViewSet, GroupViewSet, SettlementViewSet,CategoryViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'settlements', SettlementViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
