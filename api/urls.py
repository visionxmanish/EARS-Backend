from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, FiscalYearViewSet, SectorViewSet, DataCategoryViewSet,
    PlaceViewSet, EconomicDataProgressUserViewSet, EconomicDataEntryViewSet,
    UserRelatedOfficeViewSet, ReportTypeViewSet, NepaliMonthViewSet,
    UserNotificationViewSet, ProvinceViewSet, DistrictViewSet,
    MunicipalityViewSet, DashboardAPIView, CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'fiscal-years', FiscalYearViewSet, basename='fiscal-year')
router.register(r'sectors', SectorViewSet, basename='sector')
router.register(r'data-categories', DataCategoryViewSet, basename='data-category')
router.register(r'places', PlaceViewSet, basename='place')
router.register(r'economic-data-progress', EconomicDataProgressUserViewSet, basename='economic-data-progress')
router.register(r'economic-data-entries', EconomicDataEntryViewSet, basename='economic-data-entry')
router.register(r'user-related-offices', UserRelatedOfficeViewSet, basename='user-related-office')
router.register(r'report-types', ReportTypeViewSet, basename='report-type')
router.register(r'nepali-months', NepaliMonthViewSet, basename='nepali-month')
router.register(r'notifications', UserNotificationViewSet, basename='notification')
router.register(r'provinces', ProvinceViewSet, basename='province')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'municipalities', MunicipalityViewSet, basename='municipality')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]


