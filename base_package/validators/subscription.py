from datetime import datetime, timezone

from app.exceptions import BadRequest
from base_package.schemas.tenant_subscription_history import (
    TenantSubscriptionHistorySchema,
)

def validate_current_subscription_plan_from_cache(
    tenant_subscription_history: TenantSubscriptionHistorySchema,
):
    """
    Validate Any Subscription Plan Is Active
    """

    if not tenant_subscription_history:
        raise BadRequest(detail="No active subscription")

    # local_timezone = pytz.timezone(user.tenant.timezone)
    current_date_local = datetime.now()
    if (
        datetime.fromtimestamp(
            int(tenant_subscription_history.end_timestamp), tz=timezone.utc
        ).date()
        < current_date_local.date()
    ):
        raise BadRequest(detail="Subscription has been expired")

    return tenant_subscription_history
