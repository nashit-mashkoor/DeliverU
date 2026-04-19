import asyncio
import os
from dataclasses import dataclass
from datetime import time

from sqlmodel import select

from backend.database.crud import AsyncSessionLocal
from backend.database.models import (
    CustomerProfile,
    DeliverySlot,
    DriverProfile,
    GroceryItem,
    Region,
    RegionDriverAssignment,
    Restaurant,
    User,
    UserRole,
)
from backend.services.auth import AuthService


@dataclass
class SeedResult:
    created: int = 0
    reused: int = 0


def _env(key: str, default: str) -> str:
    value = os.environ.get(key, default).strip()
    return value or default


async def _get_user_by_email(session, email: str):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def _get_region_by_name(session, name: str):
    result = await session.execute(select(Region).where(Region.name == name))
    return result.scalar_one_or_none()


async def _get_slot_by_region_time(session, region_id: int, start_time: time, end_time: time):
    result = await session.execute(
        select(DeliverySlot).where(
            DeliverySlot.region_id == region_id,
            DeliverySlot.start_time == start_time,
            DeliverySlot.end_time == end_time,
        )
    )
    return result.scalar_one_or_none()


async def _get_restaurant_by_name(session, region_id: int, name: str):
    result = await session.execute(
        select(Restaurant).where(Restaurant.region_id == region_id, Restaurant.name == name)
    )
    return result.scalar_one_or_none()


async def _get_grocery_by_name(session, region_id: int, name: str):
    result = await session.execute(
        select(GroceryItem).where(GroceryItem.region_id == region_id, GroceryItem.name == name)
    )
    return result.scalar_one_or_none()


async def seed() -> None:
    result = SeedResult()

    admin_email = _env("SEED_ADMIN_EMAIL", "admin@example.com")
    customer_email = _env("SEED_CUSTOMER_EMAIL", "customer@example.com")
    driver_email = _env("SEED_DRIVER_EMAIL", "driver@example.com")
    default_password = _env("SEED_DEFAULT_PASSWORD", "DeliverU123")

    region_name = _env("SEED_REGION_NAME", "Downtown")
    restaurant_name = _env("SEED_RESTAURANT_NAME", "City Bites")
    grocery_name = _env("SEED_GROCERY_NAME", "Milk 1L")

    async with AsyncSessionLocal() as session:
        admin = await _get_user_by_email(session, admin_email)
        if admin is None:
            admin = User(
                email=admin_email,
                hashed_password=AuthService.get_password_hash(default_password),
                role=UserRole.ADMIN,
                is_active=True,
            )
            session.add(admin)
            result.created += 1
        else:
            admin.role = UserRole.ADMIN
            admin.is_active = True
            result.reused += 1

        customer = await _get_user_by_email(session, customer_email)
        if customer is None:
            customer = User(
                email=customer_email,
                hashed_password=AuthService.get_password_hash(default_password),
                role=UserRole.CUSTOMER,
                is_active=True,
            )
            session.add(customer)
            result.created += 1
        else:
            customer.role = UserRole.CUSTOMER
            customer.is_active = True
            result.reused += 1

        driver = await _get_user_by_email(session, driver_email)
        if driver is None:
            driver = User(
                email=driver_email,
                hashed_password=AuthService.get_password_hash(default_password),
                role=UserRole.DRIVER,
                is_active=True,
            )
            session.add(driver)
            result.created += 1
        else:
            driver.role = UserRole.DRIVER
            driver.is_active = True
            result.reused += 1

        await session.flush()

        region = await _get_region_by_name(session, region_name)
        if region is None:
            region = Region(
                name=region_name,
                min_latitude=24.840,
                max_latitude=24.920,
                min_longitude=67.020,
                max_longitude=67.120,
                is_active=True,
            )
            session.add(region)
            await session.flush()
            result.created += 1
        else:
            region.is_active = True
            result.reused += 1

        customer_profile_result = await session.execute(
            select(CustomerProfile).where(CustomerProfile.user_id == customer.id)
        )
        customer_profile = customer_profile_result.scalar_one_or_none()
        if customer_profile is None:
            customer_profile = CustomerProfile(
                user_id=customer.id,
                region_id=region.id,
                full_name="Slice Zero Customer",
                phone_number="03000000001",
                address_text="Block A, Downtown",
                latitude=24.880,
                longitude=67.070,
            )
            session.add(customer_profile)
            result.created += 1
        else:
            customer_profile.region_id = region.id
            result.reused += 1

        driver_profile_result = await session.execute(
            select(DriverProfile).where(DriverProfile.user_id == driver.id)
        )
        driver_profile = driver_profile_result.scalar_one_or_none()
        if driver_profile is None:
            driver_profile = DriverProfile(
                user_id=driver.id,
                full_name="Slice Zero Driver",
                phone_number="03000000002",
                license_number="DRV-001",
                national_id_number="42101-0000000-1",
                bike_details="125cc",
                is_active=True,
            )
            session.add(driver_profile)
            await session.flush()
            result.created += 1
        else:
            driver_profile.is_active = True
            result.reused += 1

        slot = await _get_slot_by_region_time(session, region.id, time(hour=18, minute=0), time(hour=20, minute=0))
        if slot is None:
            slot = DeliverySlot(
                region_id=region.id,
                slot_name="Evening Peak",
                start_time=time(hour=18, minute=0),
                end_time=time(hour=20, minute=0),
                capacity=20,
                order_cutoff_minutes=30,
                edit_cancel_lock_minutes=30,
                is_active=True,
            )
            session.add(slot)
            result.created += 1
        else:
            slot.is_active = True
            result.reused += 1

        assignment_result = await session.execute(
            select(RegionDriverAssignment).where(
                RegionDriverAssignment.region_id == region.id,
                RegionDriverAssignment.driver_profile_id == driver_profile.id,
            )
        )
        assignment = assignment_result.scalar_one_or_none()
        if assignment is None:
            session.add(RegionDriverAssignment(region_id=region.id, driver_profile_id=driver_profile.id, is_active=True))
            result.created += 1
        else:
            assignment.is_active = True
            result.reused += 1

        restaurant = await _get_restaurant_by_name(session, region.id, restaurant_name)
        if restaurant is None:
            session.add(
                Restaurant(
                    region_id=region.id,
                    name=restaurant_name,
                    phone_number="03110000000",
                    address_text="Main Market, Downtown",
                    opening_time=time(hour=10, minute=0),
                    closing_time=time(hour=23, minute=0),
                    is_active=True,
                )
            )
            result.created += 1
        else:
            restaurant.is_active = True
            result.reused += 1

        grocery = await _get_grocery_by_name(session, region.id, grocery_name)
        if grocery is None:
            session.add(
                GroceryItem(
                    region_id=region.id,
                    name=grocery_name,
                    description="Seed grocery item",
                    estimated_price=320.00,
                    is_active=True,
                )
            )
            result.created += 1
        else:
            grocery.is_active = True
            result.reused += 1

        await session.commit()

    print("Seed completed")
    print(f"created={result.created} reused={result.reused}")
    print(f"admin={admin_email}")
    print(f"customer={customer_email}")
    print(f"driver={driver_email}")
    print(f"password={default_password}")


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()
