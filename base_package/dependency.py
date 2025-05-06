from fastapi import Request, Depends, Response
from jose import JWTError, jwt
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AuthorizationError
from app.settings import settings
from app.db.database import get_db
from app.exceptions import BadRequest
from base_package.validators.subscription import validate_current_subscription_plan_from_cache
from base_package.utils.cache import (
    get_or_set_user_cached_data,
    get_or_set_tenant_cached_data,
    get_or_set_tenant_subscription_history_cached_data,
    get_or_set_account_type_cached_data,
)


async def check_user_permission(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
) -> Dict:
    """
    Checks user permissions based on various conditions like user status,
    tenant status, subscription status, and user access to the API endpoint.

    Args:
        request (Request): The request object used to extract the user details.

    Returns:
        dict: A dictionary containing user_id and tenant_id if all checks pass.

    Raises:
        HTTPException: If any of the permission checks fail.
    """
    # Get user details from request
    user_details = await get_user_details_from_request(request)

    user_id = user_details["user_id"]
    tenant_id = user_details["tenant_id"]

    user = await get_or_set_user_cached_data(f"user:{user_id}")
    cookies = [{
        "key": "access_token",
        "value": "",
        "max_age": 0,
        "httponly": True,
        "secure": True,
        "samesite": "None",
    }]

    if user.status.value != "active":
        raise BadRequest(
            detail="User is not active",
            cookies=cookies
        )

    # If User Account Type Updated Auto Logout
    if not user.is_account_owner and not user.account_type_id:
        raise BadRequest(detail="Accoun type has been changed", cookies=cookies)

    tenant = await get_or_set_tenant_cached_data(f"tenant:{tenant_id}")

    # Check if the tenant is active
    if tenant.status.value != "active":
        raise BadRequest(detail="Tenant is not active", cookies=cookies)

    # Check if the subscription is active
    tenant_subscription_history = (
        await get_or_set_tenant_subscription_history_cached_data(
            f"tenant_subscription:{tenant_id}"
        )
    )
    validate_current_subscription_plan_from_cache(tenant_subscription_history)

    # user = await db.get(User, user_id)
    user_details["user_primary_language"] = user.primary_language
    user_details["tenant_date_format"] = tenant.date_format
    user_details["tenant_time_format"] = tenant.time_format
    user_details["is_account_owner"] = user.is_account_owner

    # Check if the workspace is active
    # TODO

    user_details["user_account_type_id"] = (
        user.account_type_id if not user.is_account_owner else ""
    )

    # Cache Account Type Permissions
    allowed_modules_and_permissions = await get_or_set_account_type_cached_data(
        db, user
    )
    user_details["allowed_modules_and_permissions"] = allowed_modules_and_permissions

    # Check if user has access to the requested API endpoint
    # To extract metadata from the current route
    endpoint = request.scope.get("endpoint")
    metadata = getattr(endpoint, "custom_data", {})
    if metadata:
        module = metadata.get("module")
        if module:
            if module not in allowed_modules_and_permissions:
                raise BadRequest(detail="Permission denied")
            if not allowed_modules_and_permissions[module]["module_status"]:
                raise BadRequest(detail="Permission denied")
        permission = metadata.get("permission")
        if permission:
            if not allowed_modules_and_permissions[module]["permissions"].get(
                permission
            ):
                raise BadRequest(detail="Permission denied")

    # Attach User And Tenant In Dependency Return Data
    user_details["user"] = user
    user_details["tenant"] = tenant

    return user_details


async def get_user_details_from_request(
    request: Request, return_error: bool = True
) -> dict:
    """
    Retrieves user details from the request by decoding the access_token.
    Args:
        request: The request object containing cookies.

    Returns:
        dict: A dictionary containing 'user_id' and 'tenant_id'.

    Raises:
        AuthorizationError: If the token is invalid or the user is not authenticated.
    """
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise AuthorizationError(detail="Not authenticated")

    try:
        payload = jwt.decode(
            access_token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        user_id = payload.get("id")
        tenant_id = payload.get("tenant_id")

        if not user_id or not tenant_id:
            raise AuthorizationError(detail="Invalid token")
    except JWTError:
        raise AuthorizationError(detail="Invalid token")

    return {
        "user_id": user_id,
        "tenant_id": tenant_id,
    }