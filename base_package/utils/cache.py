import json
import uuid

from base_package.services.cache import Cache
from base_package.schemas.user_schema import UserSchema, TenantSchema
from base_package.schemas.tenant_subscription_history import (
    TenantSubscriptionHistorySchema,
)

cache = Cache()


async def get_or_set_user_cached_data(cache_key: str):
    """
    Get User Cache From Memory Database, If Not Exist Set User Cache In Memory Database
    """
    cached_user_data = await cache.get(cache_key)

    if not cached_user_data:
        _id = cache_key.split(":")[1]
        cached_user_data = await set_user_cached_data(_id)

    user_dict = json.loads(cached_user_data)
    return UserSchema(**user_dict)


async def set_user_cached_data(user_id: str):
    """
    Set User Cache In Memory Database
    """
    user = ""
    print(user.__dict__)
    user_schema = UserSchema.model_validate(
        user, from_attributes=True
    )  # returns User Schema Instance
    json_user = user_schema.model_dump_json()  # Converts instance to json

    await cache.set(f"user:{str(user.id)}", json_user)
    return json_user


async def get_or_set_tenant_cached_data(cache_key: str):
    """
    Get Tenant Cache From Memory Database, If Not Exist Set Tenant Cache In Memory Database
    """
    cached_tenant_data = await cache.get(cache_key)

    if not cached_tenant_data:
        _id = cache_key.split(":")[1]
        cached_tenant_data = await set_tenant_cached_data( _id)

    tenant_dict = json.loads(cached_tenant_data)
    return TenantSchema(**tenant_dict)


async def set_tenant_cached_data(tenant_id: str):
    """
    Set Tenant Cache In Memory Database
    """
    tenant = ""
    tenant_schema = TenantSchema.model_validate(tenant)  # returns User Schema Instance
    tenant_json = tenant_schema.model_dump_json()  # Converts instance to json

    await cache.set(f"tenant:{tenant.id}", tenant_json)

    return tenant_json


async def get_or_set_tenant_subscription_history_cached_data(cache_key: str):
    """
    Get Tenant Subscription History Cache From Memory Database, If Not Exist Set Tenant Subscription History Cache In Memory Database
    """
    cached_tenant_subscription_data = await cache.get(cache_key)

    if not cached_tenant_subscription_data:
        _id = cache_key.split(":")[1]
        cached_tenant_subscription_data = (
            await set_tenant_subscription_history_cached_data(_id)
        )

    tenant_subscription_dict = json.loads(cached_tenant_subscription_data)
    return TenantSubscriptionHistorySchema(**tenant_subscription_dict)


async def set_tenant_subscription_history_cached_data(tenant_id: uuid.UUID):
    """
    Set Tenant Subscription History Cache In Memory Database
    #"""
    tenant_subscription_history = ""
    tenant_subscription_history_schema = TenantSubscriptionHistorySchema.model_validate(
        tenant_subscription_history
    )
    json_tenant_subscription = tenant_subscription_history_schema.model_dump_json()
    await cache.set(f"tenant_subscription:{str(tenant_id)}", json_tenant_subscription)
    return json_tenant_subscription


async def get_or_set_account_type_cached_data(user: UserSchema):
    """
    Get User Account Type Cache From Memory Database, If Not Exist Set User Account Type Cache In Memory Database
    """
    if user.account_type_id:
        cached_account_type_modules_and_permissions = await cache.get(
            str(user.account_type_id)
        )
    else:
        cached_account_type_modules_and_permissions = await cache.get(
            f"tenant_account_permissions:{str(user.tenant_id)}"
        )
    if not cached_account_type_modules_and_permissions:
        cached_account_type_modules_and_permissions = (
            await set_account_type_cached_data(user)
        )
    account_type_modules_and_permissions_dict = json.loads(
        cached_account_type_modules_and_permissions
    )
    return account_type_modules_and_permissions_dict


async def set_account_type_cached_data(user: UserSchema):
    """
    Set User Account Type Cache In Memory Database
    """
    account_type_modules_and_permissions = ""
    modules_and_permissions = {}
    for module in account_type_modules_and_permissions:

        permissions_allowed = {}
        for permission in module["permissions"]:
            # For Allowed Module Permission
            if module["is_checked"]:
                permissions_allowed[permission["name"]] = permission["is_checked"]
            else:
                permissions_allowed[permission["name"]] = False

        # Add Allowed Permissmodulesions Lables To Allowed Modules
        modules_and_permissions[module["slug"]] = {
            "module_status": module["is_checked"],
            "permissions": permissions_allowed,
        }
    json_account_type_modules_and_permissions = json.dumps(modules_and_permissions)
    if user.account_type_id:
        await cache.set(
            str(user.account_type_id), json_account_type_modules_and_permissions
        )
    else:
        await cache.set(
            f"tenant_account_permissions:{str(user.tenant_id)}",
            json_account_type_modules_and_permissions,
        )
    return json_account_type_modules_and_permissions
