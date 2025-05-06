from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

from app.models import UserStatusEnum, TenantStatusEnum


class TenantStatusEnum(Enum):
    DELETED = "deleted"
    ACTIVE = "active"
    INACTIVE = "inactive"
    NOT_VERIFIED = "not_verified"

# Tenant Schema
class TenantSchema(BaseModel):
    id: UUID
    company_name: str
    company_logo: Optional[str]
    company_size: Optional[str]
    company_location: Optional[str]
    company_country: Optional[str]
    industry: Optional[str]
    workspace_name: Optional[str]
    domain: Optional[str]
    is_subdomain: bool = True
    website: Optional[str]
    currency: str
    date_format: str
    time_format: str
    tax_number: Optional[str]
    time_zone: str
    account_owner_handle: Optional[str]
    solutions_interested: Optional[str]
    language: Optional[str]
    financial_year_start: Optional[str]
    status: TenantStatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserStatusEnum(Enum):
    DELETED = "deleted"
    ACTIVE = "active"
    INACTIVE = "inactive"
    NOT_VERIFIED = "not_verified" 


# User Schema
class UserSchema(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    email: Optional[EmailStr]
    phone_number: Optional[str]
    password: Optional[str]
    country_code: Optional[str]
    image: Optional[str]
    designation: Optional[str]
    primary_language: Optional[str] = "en"
    is_account_owner: bool = False
    otp: Optional[str]
    otp_expiry_at: Optional[datetime]
    account_type_id: Optional[UUID]
    status: UserStatusEnum
    updated_by: Optional[UUID]
    created_by: Optional[UUID]
    # created_at: datetime
    # updated_at: datetime
    login_time: Optional[datetime]
    last_login_time: Optional[datetime]

    class Config:
        from_attributes = True
