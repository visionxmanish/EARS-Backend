# This file is intentionally minimal - we import models from the existing project
# All models are defined in the existing project's apps (authentication, reports)
# This allows the API to use the same database tables

# Import models from existing project
from reports.models import (
    StatusChoices, FiscalYear, Sector, DataCategory, Place,
    EconomicDataProgressUser, EconomicDataEntry,
    UserRelatedOffice, Report_Type, NepaliMonth, UserNotification
)
from authentication.models import User

# Alias Report_Type to ReportType for consistency
ReportType = Report_Type

# Re-export for convenience
__all__ = [
    'User', 'StatusChoices', 'FiscalYear', 'Sector', 'DataCategory', 'Place',
    'EconomicDataProgressUser', 'EconomicDataEntry',
    'UserRelatedOffice', 'ReportType', 'NepaliMonth', 'UserNotification'
]

