from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from enum import Enum

from app.models import TenantSubscriptionStatus


class TenantSubscriptionStatus(Enum):
    ACTIVE = "active"
    IN_ACTIVE = "in_active"
    PENDING = "pending"
    DELETED = "deleted"

class TenantSubscriptionHistorySchema(BaseModel):
    id: UUID
    tenant_id: Optional[UUID]
    subscription_plan_id: UUID
    price_month_rupee: Decimal
    price_month_dollar: Decimal
    price_month_dirham: Decimal | None
    price_year_rupee: Decimal
    price_year_dollar: Decimal
    price_year_dirham: Decimal | None
    details: Optional[Dict[str, Any]]
    plan_payment_type: Optional[str]
    plan_price_type: Optional[str]
    invoice_number: Optional[int]
    start_timestamp: Optional[str]
    ios_purchase_transaction_id: Optional[str]
    ios_purchase_original_transaction_id: Optional[str]
    end_timestamp: Optional[str]
    paid_via: Optional[str] = "stripe"
    stripe_subscription_id: Optional[str]
    stripe_invoice_id: Optional[str]
    status: TenantSubscriptionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
