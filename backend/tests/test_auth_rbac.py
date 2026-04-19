import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from backend.constants import DATABASE_URL
from backend.database.models import UserRole
from backend.services.auth import AuthService


AUTH_BASE = "/api/v1/auth"


def _unique_email(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}@example.com"


def _upsert_user(email: str, password: str, role: UserRole, is_active: bool = True) -> None:
    sync_database_url = DATABASE_URL.replace("+asyncpg", "")
    hashed_password = AuthService.get_password_hash(password)

    engine = create_engine(sync_database_url, pool_pre_ping=True)
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO "user" (uuid, email, hashed_password, is_active, role, created_at, updated_at)
                VALUES (:uuid, :email, :hashed_password, :is_active, :role, NOW(), NOW())
                ON CONFLICT (email)
                DO UPDATE SET
                    hashed_password = EXCLUDED.hashed_password,
                    is_active = EXCLUDED.is_active,
                    role = EXCLUDED.role,
                    updated_at = NOW()
                """
            ),
            {
                "uuid": str(uuid.uuid4()),
                "email": email,
                "hashed_password": hashed_password,
                "is_active": is_active,
                "role": role.value,
            },
        )


def test_register_login_refresh_and_me_success(client: TestClient) -> None:
    email = _unique_email("customer")
    password = "DeliverU123"

    register_response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "email": email,
            "password": password,
            "password_confirm": password,
        },
    )
    assert register_response.status_code == 201
    assert register_response.json()["role"] == "customer"

    login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert tokens["access_token"]
    assert tokens["refresh_token"]

    me_response = client.get(
        f"{AUTH_BASE}/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == email
    assert me_response.json()["role"] == "customer"

    refresh_response = client.post(
        f"{AUTH_BASE}/refresh-token",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )
    assert refresh_response.status_code == 200
    assert refresh_response.json()["access_token"]


def test_auth_failure_and_inactive_user_blocked(client: TestClient) -> None:
    email = _unique_email("inactive")
    password = "DeliverU123"

    register_response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "email": email,
            "password": password,
            "password_confirm": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    deactivate_response = client.post(
        f"{AUTH_BASE}/deactivate",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert deactivate_response.status_code == 200

    wrong_password_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": "WrongPass123",
        },
    )
    assert wrong_password_response.status_code == 401

    inactive_login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert inactive_login_response.status_code == 401
    assert inactive_login_response.json()["detail"] == "User account is inactive"


def test_logout_invalidates_access_and_refresh_tokens(client: TestClient) -> None:
    email = _unique_email("logout")
    password = "DeliverU123"

    register_response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "email": email,
            "password": password,
            "password_confirm": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200
    tokens = login_response.json()

    logout_response = client.post(
        f"{AUTH_BASE}/logout",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert logout_response.status_code == 200

    me_after_logout_response = client.get(
        f"{AUTH_BASE}/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me_after_logout_response.status_code == 401

    refresh_after_logout_response = client.post(
        f"{AUTH_BASE}/refresh-token",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )
    assert refresh_after_logout_response.status_code == 401


def test_change_password_and_deactivate_flow(client: TestClient) -> None:
    email = _unique_email("change-pass")
    old_password = "DeliverU123"
    new_password = "DeliverU124"

    register_response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "email": email,
            "password": old_password,
            "password_confirm": old_password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": old_password,
        },
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    wrong_current_response = client.post(
        f"{AUTH_BASE}/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "current_password": "InvalidCurrent123",
            "new_password": new_password,
            "new_password_confirm": new_password,
        },
    )
    assert wrong_current_response.status_code == 401

    change_response = client.post(
        f"{AUTH_BASE}/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "current_password": old_password,
            "new_password": new_password,
            "new_password_confirm": new_password,
        },
    )
    assert change_response.status_code == 200

    old_login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": old_password,
        },
    )
    assert old_login_response.status_code == 401

    new_login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": new_password,
        },
    )
    assert new_login_response.status_code == 200
    new_access_token = new_login_response.json()["access_token"]

    deactivate_response = client.post(
        f"{AUTH_BASE}/deactivate",
        headers={"Authorization": f"Bearer {new_access_token}"},
    )
    assert deactivate_response.status_code == 200

    inactive_login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": email,
            "password": new_password,
        },
    )
    assert inactive_login_response.status_code == 401
    assert inactive_login_response.json()["detail"] == "User account is inactive"


def test_admin_user_creation_permission_boundaries(client: TestClient) -> None:
    admin_email = _unique_email("admin")
    admin_password = "DeliverU123"
    _upsert_user(email=admin_email, password=admin_password, role=UserRole.ADMIN, is_active=True)

    customer_email = _unique_email("rbac-customer")
    customer_password = "DeliverU123"
    register_response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "email": customer_email,
            "password": customer_password,
            "password_confirm": customer_password,
        },
    )
    assert register_response.status_code == 201

    customer_login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": customer_email,
            "password": customer_password,
        },
    )
    assert customer_login_response.status_code == 200
    customer_access_token = customer_login_response.json()["access_token"]

    customer_forbidden_response = client.post(
        f"{AUTH_BASE}/admin/users",
        headers={"Authorization": f"Bearer {customer_access_token}"},
        json={
            "email": _unique_email("should-fail"),
            "password": "DeliverU123",
            "role": "driver",
        },
    )
    assert customer_forbidden_response.status_code == 403

    admin_login_response = client.post(
        f"{AUTH_BASE}/login",
        json={
            "email": admin_email,
            "password": admin_password,
        },
    )
    assert admin_login_response.status_code == 200
    admin_access_token = admin_login_response.json()["access_token"]

    create_driver_response = client.post(
        f"{AUTH_BASE}/admin/users",
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json={
            "email": _unique_email("driver"),
            "password": "DeliverU123",
            "role": "driver",
        },
    )
    assert create_driver_response.status_code == 201
    assert create_driver_response.json()["role"] == "driver"

    create_customer_response = client.post(
        f"{AUTH_BASE}/admin/users",
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json={
            "email": _unique_email("customer-should-fail"),
            "password": "DeliverU123",
            "role": "customer",
        },
    )
    assert create_customer_response.status_code == 400
