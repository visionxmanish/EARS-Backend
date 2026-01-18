from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import (
    FiscalYear, Sector, DataCategory, Place, 
    EconomicDataProgressUser, EconomicDataEntry, 
    UserRelatedOffice, ReportType, NepaliMonth, UserNotification
)
from nepali_address.models import Province, District, Municipality

# Get the User model (from authentication app)
User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that uses staff_code instead of username"""
    username_field = 'staff_code'

    def validate(self, attrs):
        # Rename 'username' to 'staff_code' for the authentication
        if 'username' in attrs:
            attrs['staff_code'] = attrs.pop('username')
        elif 'staff_code' not in attrs:
            raise serializers.ValidationError('staff_code is required')
        
        data = super().validate(attrs)
        return data


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'province']


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ['id', 'name', 'district']


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'staff_code', 'username', 'email', 'first_name', 
            'middle_name', 'last_name', 'full_name', 'phone_number', 
            'role', 'is_active', 'is_staff', 'gender', 'profile_picture', 'user_related_offices', 'user_provinces', 'user_districts', 'user_municipalities',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserRelatedOfficeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = UserRelatedOffice
        fields = [
            'id', 'office', 'status', 'created_by', 'created_by_name',
            'approved_by', 'approved_by_name', 'approved_at', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class FiscalYearSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = FiscalYear
        fields = [
            'id', 'year', 'status', 'created_by', 'created_by_name',
            'approved_by', 'approved_by_name', 'approved_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'approved_by', 'created_at', 'updated_at']


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = ['id', 'name', 'description']


class NepaliMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = NepaliMonth
        fields = ['id', 'month', 'is_first_half']


class SectorSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Sector
        fields = [
            'id', 'name', 'description', 'image', 'image_url', 
            'has_different_report', 'status', 'created_by', 'created_by_name',
            'approved_by', 'approved_by_name', 'approved_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'approved_by', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class DataCategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = DataCategory
        fields = [
            'id', 'sector', 'sector_name', 'name', 'parent', 'parent_name',
            'is_summable', 'unit', 'remarks', 'related_office', 'status',
            'created_by', 'created_by_name', 'approved_by', 'approved_by_name',
            'approved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'state']


class EconomicDataEntrySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = EconomicDataEntry
        fields = [
            'id', 'progress', 'category', 'category_name', 'value', 'capacity',
            'status', 'approved_by', 'approved_by_name', 'approved_at',
            'rejected_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EconomicDataProgressUserSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    fiscal_year_name = serializers.CharField(source='fiscal_year.year', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    municipality_name = serializers.CharField(source='municipality.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    report_type_name = serializers.CharField(source='report_type.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    contributors_list = serializers.SerializerMethodField()
    economic_entries = EconomicDataEntrySerializer(many=True, read_only=True)
    
    class Meta:
        model = EconomicDataProgressUser
        fields = [
            'id', 'user', 'user_name', 'contributors', 'contributors_list',
            'is_completed', 'fiscal_year', 'fiscal_year_name', 'province', 
            'province_name', 'district', 'district_name', 'municipality',
            'municipality_name', 'sector', 'sector_name', 'report_type',
            'report_type_name', 'status', 'approved_by', 'approved_by_name',
            'approved_at', 'economic_entries', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_contributors_list(self, obj):
        return [{'id': u.id, 'name': u.get_full_name()} for u in obj.contributors.all()]


class UserNotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = UserNotification
        fields = [
            'id', 'user', 'user_name', 'message', 'link', 'is_read',
            'required_roles', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# Nested serializers for detailed views
class EconomicDataProgressUserDetailSerializer(EconomicDataProgressUserSerializer):
    economic_entries = EconomicDataEntrySerializer(many=True, read_only=True)
