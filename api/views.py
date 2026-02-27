from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Q, Count, Sum
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model
from .models import (
    FiscalYear, Sector, DataCategory, Place,
    EconomicDataProgressUser, EconomicDataEntry,
    UserRelatedOffice, ReportType, NepaliMonth, UserNotification, StatusChoices
)

# Get the User model (from authentication app)
User = get_user_model()

from .serializers import (
    UserSerializer, FiscalYearSerializer, SectorSerializer,
    DataCategorySerializer, PlaceSerializer, EconomicDataProgressUserSerializer,
    EconomicDataEntrySerializer, UserRelatedOfficeSerializer,
    ReportTypeSerializer, NepaliMonthSerializer, UserNotificationSerializer,
    ProvinceSerializer, DistrictSerializer, MunicipalitySerializer,
    EconomicDataProgressUserDetailSerializer, CustomTokenObtainPairSerializer
)
from nepali_address.models import Province, District, Municipality


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT view that uses staff_code instead of username"""
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['staff_code', 'first_name', 'last_name', 'email', 'username']
    filterset_fields = ['role', 'is_active', 'is_staff']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user statistics (admin only)"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        stats = {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'by_role': {
                'admin': User.objects.filter(role='admin').count(),
                'maker': User.objects.filter(role='maker').count(),
                'checker': User.objects.filter(role='checker').count(),
            }
        }
        return Response(stats)


class FiscalYearViewSet(viewsets.ModelViewSet):
    queryset = FiscalYear.objects.all()
    serializer_class = FiscalYearSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['year']
    filterset_fields = ['status']
    ordering_fields = ['year', 'created_at']
    ordering = ['-year']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(
            status=StatusChoices.PENDING,
            approved_by=None,
            approved_at=None
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a fiscal year (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        fiscal_year = self.get_object()
        fiscal_year.status = StatusChoices.APPROVED
        fiscal_year.approved_by = request.user
        fiscal_year.approved_at = timezone.now()
        fiscal_year.save()
        
        serializer = self.get_serializer(fiscal_year)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a fiscal year (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        fiscal_year = self.get_object()
        fiscal_year.status = StatusChoices.REJECTED
        fiscal_year.approved_by = request.user
        fiscal_year.approved_at = timezone.now()
        fiscal_year.save()
        
        serializer = self.get_serializer(fiscal_year)
        return Response(serializer.data)


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['status', 'has_different_report']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(
            status=StatusChoices.PENDING,
            approved_by=None,
            approved_at=None
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a sector (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        sector = self.get_object()
        sector.status = StatusChoices.APPROVED
        sector.approved_by = request.user
        sector.approved_at = timezone.now()
        sector.save()
        
        serializer = self.get_serializer(sector)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a sector (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        sector = self.get_object()
        sector.status = StatusChoices.REJECTED
        sector.approved_by = request.user
        sector.approved_at = timezone.now()
        sector.save()
        
        serializer = self.get_serializer(sector)
        return Response(serializer.data)


class DataCategoryViewSet(viewsets.ModelViewSet):
    queryset = DataCategory.objects.all()
    serializer_class = DataCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'remarks']
    filterset_fields = ['sector', 'parent', 'status', 'is_summable']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(
            status=StatusChoices.PENDING,
            approved_by=None,
            approved_at=None
        )

    @action(detail=False, methods=['get'])
    def by_sector(self, request):
        """Get categories by sector by filtering out the parent categories"""
        sector_id = request.query_params.get('sector_id')
        if not sector_id:
            return Response({'error': 'sector_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        categories = DataCategory.objects.filter(sector_id=sector_id)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a category (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        category = self.get_object()
        category.status = StatusChoices.APPROVED
        category.approved_by = request.user
        category.approved_at = timezone.now()
        category.save()
        
        serializer = self.get_serializer(category)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a category (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        category = self.get_object()
        category.status = StatusChoices.REJECTED
        category.approved_by = request.user
        category.approved_at = timezone.now()
        category.save()
        
        serializer = self.get_serializer(category)
        return Response(serializer.data)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['state']
    ordering_fields = ['name']
    ordering = ['name']


class EconomicDataProgressUserViewSet(viewsets.ModelViewSet):
    queryset = EconomicDataProgressUser.objects.all()
    serializer_class = EconomicDataProgressUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['fiscal_year', 'sector', 'province', 'district', 'status', 'is_completed', 'user']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = EconomicDataProgressUser.objects.all()
        user = self.request.user
        
        # Makers can only see their own entries
        if user.role == 'maker':
            queryset = queryset.filter(Q(user=user) | Q(contributors=user)).distinct()
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EconomicDataProgressUserDetailSerializer
        return EconomicDataProgressUserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(
            status=StatusChoices.PENDING,
            approved_by=None,
            approved_at=None
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a progress entry (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        progress = self.get_object()
        
        # Check if any entries are rejected
        rejected_entries = progress.economic_entries.filter(status=StatusChoices.REJECTED)
        if rejected_entries.exists():
            return Response(
                {'error': 'Cannot approve progress with rejected entries'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Approve all entries
        progress.economic_entries.update(
            status=StatusChoices.APPROVED,
            approved_by=request.user,
            approved_at=timezone.now()
        )
        
        # Approve progress
        progress.status = StatusChoices.APPROVED
        progress.approved_by = request.user
        progress.approved_at = timezone.now()
        progress.save()
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a progress entry (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        progress = self.get_object()
        progress.status = StatusChoices.REJECTED
        progress.approved_by = request.user
        progress.approved_at = timezone.now()
        progress.save()
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark progress as completed"""
        progress = self.get_object()
        if progress.user != request.user and request.user not in progress.contributors.all():
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        progress.is_completed = True
        progress.save()
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data)


class EconomicDataEntryViewSet(viewsets.ModelViewSet):
    queryset = EconomicDataEntry.objects.all()
    serializer_class = EconomicDataEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['progress', 'category', 'status']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve an entry (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        entry = self.get_object()
        entry.status = StatusChoices.APPROVED
        entry.approved_by = request.user
        entry.approved_at = timezone.now()
        entry.save()
        
        serializer = self.get_serializer(entry)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject an entry (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        entry = self.get_object()
        rejected_reason = request.data.get('rejected_reason', '')
        entry.status = StatusChoices.REJECTED
        entry.approved_by = request.user
        entry.approved_at = timezone.now()
        entry.rejected_reason = rejected_reason
        entry.save()
        
        serializer = self.get_serializer(entry)
        return Response(serializer.data)


class UserRelatedOfficeViewSet(viewsets.ModelViewSet):
    queryset = UserRelatedOffice.objects.all()
    serializer_class = UserRelatedOfficeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['office']
    filterset_fields = ['status']
    ordering_fields = ['office', 'created_at']
    ordering = ['office']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(
            status=StatusChoices.PENDING,
            approved_by=None,
            approved_at=None
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve an office (admin/checker only)"""
        if request.user.role not in ['admin', 'checker']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        office = self.get_object()
        office.status = StatusChoices.APPROVED
        office.approved_by = request.user
        office.approved_at = timezone.now()
        office.save()
        
        serializer = self.get_serializer(office)
        return Response(serializer.data)


class ReportTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReportType.objects.all()
    serializer_class = ReportTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class NepaliMonthViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NepaliMonth.objects.all()
    serializer_class = NepaliMonthSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_first_half']
    ordering_fields = ['month']
    ordering = ['month']


class UserNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = UserNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserNotification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        UserNotification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})


# Address API Views
class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['province']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class MunicipalityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['district']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


# Dashboard API
class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'fiscal_years': [],
            'sector_list': [],
            'report_type_list': [],
            'summary': {},
            'sector_totals': {},
            'system_metrics': {
                'cpu': 45,
                'memory': 60,
                'disk': 30,
                'network': 25
            }
        }

        if user.role == 'admin':
            data['summary'] = {
                'total_users': User.objects.count(),
                'active_sectors': Sector.objects.filter(status=StatusChoices.APPROVED).count(),
                'total_entries': EconomicDataProgressUser.objects.count(),
            }
        elif user.role == 'maker':
            data['summary'] = {
                'my_entries': EconomicDataProgressUser.objects.filter(user=user).count(),
                'pending': EconomicDataProgressUser.objects.filter(user=user, status=StatusChoices.PENDING).count(),
                'approved': EconomicDataProgressUser.objects.filter(user=user, status=StatusChoices.APPROVED).count(),
                'rejected': EconomicDataProgressUser.objects.filter(user=user, status=StatusChoices.REJECTED).count(),
            }
        elif user.role == 'checker':
            data['summary'] = {
                'pending': EconomicDataProgressUser.objects.filter(status=StatusChoices.PENDING).count(),
                'reviewed_today': EconomicDataProgressUser.objects.filter(
                    approved_by=user,
                    approved_at__date=timezone.now().date()
                ).count(),
                'approved': EconomicDataProgressUser.objects.filter(status=StatusChoices.APPROVED).count(),
                'rejected': EconomicDataProgressUser.objects.filter(status=StatusChoices.REJECTED).count(),
            }

        # Get lists
        data['fiscal_years'] = list(FiscalYear.objects.filter(status=StatusChoices.APPROVED).values_list('year', flat=True))
        data['sector_list'] = list(Sector.objects.filter(status=StatusChoices.APPROVED).values_list('name', flat=True))
        data['report_type_list'] = list(ReportType.objects.all().values_list('name', flat=True))

        # Sector totals
        sector_totals = EconomicDataProgressUser.objects.values('sector__name').annotate(
            total=Count('id')
        )
        data['sector_totals'] = {item['sector__name']: item['total'] for item in sector_totals}

        return Response(data)
