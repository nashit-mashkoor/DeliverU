from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import JSON, Column, Numeric, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    DRIVER = "driver"


class OrderStatus(str, Enum):
    DRAFT = "draft"
    PLACED = "placed"
    LOCKED = "locked"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ComplaintStatus(str, Enum):
    OPEN = "open"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class LedgerEntryType(str, Enum):
    PAYABLE = "payable"
    RECEIVABLE = "receivable"
    ADJUSTMENT = "adjustment"


class User(SQLModel, table=True):
    """User table for authentication"""

    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    role: UserRole = Field(
        default=UserRole.CUSTOMER,
        sa_column=Column(String(20), nullable=False, server_default=UserRole.CUSTOMER.value),
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    items: List["Item"] = Relationship(back_populates="user")
    customer_profile: Optional["CustomerProfile"] = Relationship(back_populates="user")
    driver_profile: Optional["DriverProfile"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="customer")
    complaints: List["Complaint"] = Relationship(back_populates="customer")
    recurring_templates: List["RecurringOrderTemplate"] = Relationship(back_populates="customer")


class Region(SQLModel, table=True):
    """Service region represented by a bounding box."""

    __tablename__ = "region"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    name: str = Field(nullable=False, unique=True, index=True)
    min_latitude: float = Field(nullable=False)
    max_latitude: float = Field(nullable=False)
    min_longitude: float = Field(nullable=False)
    max_longitude: float = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    customer_profiles: List["CustomerProfile"] = Relationship(back_populates="region")
    slots: List["DeliverySlot"] = Relationship(back_populates="region")
    grocery_items: List["GroceryItem"] = Relationship(back_populates="region")
    restaurants: List["Restaurant"] = Relationship(back_populates="region")
    orders: List["Order"] = Relationship(back_populates="region")
    complaints: List["Complaint"] = Relationship(back_populates="region")
    recurring_templates: List["RecurringOrderTemplate"] = Relationship(back_populates="region")
    driver_assignments: List["RegionDriverAssignment"] = Relationship(back_populates="region")


class CustomerProfile(SQLModel, table=True):
    """Extended customer profile and serviceability details."""

    __tablename__ = "customer_profile"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    user_id: int = Field(foreign_key="user.id", nullable=False, unique=True, index=True)
    region_id: Optional[int] = Field(default=None, foreign_key="region.id", index=True)
    full_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None, index=True)
    address_text: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    profile_image_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    user: User = Relationship(back_populates="customer_profile")
    region: Optional[Region] = Relationship(back_populates="customer_profiles")


class DriverProfile(SQLModel, table=True):
    """Extended driver profile details."""

    __tablename__ = "driver_profile"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    user_id: int = Field(foreign_key="user.id", nullable=False, unique=True, index=True)
    full_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None, index=True)
    license_number: Optional[str] = Field(default=None, index=True)
    national_id_number: Optional[str] = Field(default=None, index=True)
    bike_details: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    user: User = Relationship(back_populates="driver_profile")
    region_assignments: List["RegionDriverAssignment"] = Relationship(back_populates="driver_profile")
    assigned_orders: List["Order"] = Relationship(back_populates="driver_profile")
    complaints: List["Complaint"] = Relationship(back_populates="driver_profile")
    ledger_entries: List["DriverLedgerEntry"] = Relationship(back_populates="driver_profile")
    proof_uploads: List["ProofAttachment"] = Relationship(back_populates="uploaded_by_driver")


class DeliverySlot(SQLModel, table=True):
    """Recurring daily delivery slot template per region."""

    __tablename__ = "delivery_slot"
    __table_args__ = (
        UniqueConstraint("region_id", "start_time", "end_time", name="uq_slot_region_time_window"),
    )

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    region_id: int = Field(foreign_key="region.id", nullable=False, index=True)
    slot_name: Optional[str] = Field(default=None)
    start_time: time = Field(nullable=False)
    end_time: time = Field(nullable=False)
    capacity: int = Field(default=20, ge=1)
    order_cutoff_minutes: int = Field(default=30, ge=0)
    edit_cancel_lock_minutes: int = Field(default=30, ge=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    region: Region = Relationship(back_populates="slots")
    orders: List["Order"] = Relationship(back_populates="slot")
    recurring_templates: List["RecurringOrderTemplate"] = Relationship(back_populates="slot")


class RegionDriverAssignment(SQLModel, table=True):
    """Many-to-many region/driver assignment table."""

    __tablename__ = "region_driver_assignment"
    __table_args__ = (
        UniqueConstraint("region_id", "driver_profile_id", name="uq_region_driver_assignment"),
    )

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    region_id: int = Field(foreign_key="region.id", nullable=False, index=True)
    driver_profile_id: int = Field(foreign_key="driver_profile.id", nullable=False, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    region: Region = Relationship(back_populates="driver_assignments")
    driver_profile: DriverProfile = Relationship(back_populates="region_assignments")


class GroceryItem(SQLModel, table=True):
    """Region-specific grocery catalog item."""

    __tablename__ = "grocery_item"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    region_id: int = Field(foreign_key="region.id", nullable=False, index=True)
    name: str = Field(nullable=False, index=True)
    description: Optional[str] = Field(default=None)
    estimated_price: Optional[float] = Field(default=None, sa_column=Column(Numeric(10, 2), nullable=True))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    region: Region = Relationship(back_populates="grocery_items")
    order_items: List["OrderItem"] = Relationship(back_populates="grocery_item")


class Restaurant(SQLModel, table=True):
    """Region-specific restaurant information for MVP free-text ordering."""

    __tablename__ = "restaurant"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    region_id: int = Field(foreign_key="region.id", nullable=False, index=True)
    name: str = Field(nullable=False, index=True)
    phone_number: Optional[str] = Field(default=None)
    address_text: Optional[str] = Field(default=None)
    opening_time: Optional[time] = Field(default=None)
    closing_time: Optional[time] = Field(default=None)
    menu_image_url: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    region: Region = Relationship(back_populates="restaurants")
    orders: List["Order"] = Relationship(back_populates="restaurant")
    recurring_templates: List["RecurringOrderTemplate"] = Relationship(back_populates="restaurant")


class Order(SQLModel, table=True):
    """Customer order for a selected region slot."""

    __tablename__ = "order"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    customer_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    region_id: int = Field(foreign_key="region.id", nullable=False, index=True)
    slot_id: int = Field(foreign_key="delivery_slot.id", nullable=False, index=True)
    driver_profile_id: Optional[int] = Field(default=None, foreign_key="driver_profile.id", index=True)
    restaurant_id: Optional[int] = Field(default=None, foreign_key="restaurant.id", index=True)
    status: OrderStatus = Field(
        default=OrderStatus.DRAFT,
        sa_column=Column(String(20), nullable=False, server_default=OrderStatus.DRAFT.value),
    )
    is_recurring: bool = Field(default=False)
    restaurant_order_notes: Optional[str] = Field(default=None)
    additional_notes: Optional[str] = Field(default=None)
    locked_at: Optional[datetime] = Field(default=None)
    placed_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    customer: User = Relationship(back_populates="orders")
    region: Region = Relationship(back_populates="orders")
    slot: DeliverySlot = Relationship(back_populates="orders")
    driver_profile: Optional[DriverProfile] = Relationship(back_populates="assigned_orders")
    restaurant: Optional[Restaurant] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    complaints: List["Complaint"] = Relationship(back_populates="order")
    proof_attachments: List["ProofAttachment"] = Relationship(back_populates="order")
    ledger_entries: List["DriverLedgerEntry"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    """Individual grocery item line within an order."""

    __tablename__ = "order_item"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    order_id: int = Field(foreign_key="order.id", nullable=False, index=True)
    grocery_item_id: Optional[int] = Field(default=None, foreign_key="grocery_item.id", index=True)
    item_name_snapshot: Optional[str] = Field(default=None)
    quantity: int = Field(default=1, ge=1)
    estimated_unit_price: Optional[float] = Field(default=None, sa_column=Column(Numeric(10, 2), nullable=True))
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    order: Order = Relationship(back_populates="items")
    grocery_item: Optional[GroceryItem] = Relationship(back_populates="order_items")


class Complaint(SQLModel, table=True):
    """Customer complaints linked to orders and operations context."""

    __tablename__ = "complaint"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    customer_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id", index=True)
    driver_profile_id: Optional[int] = Field(default=None, foreign_key="driver_profile.id", index=True)
    region_id: Optional[int] = Field(default=None, foreign_key="region.id", index=True)
    description: str = Field(nullable=False)
    status: ComplaintStatus = Field(
        default=ComplaintStatus.OPEN,
        sa_column=Column(String(20), nullable=False, server_default=ComplaintStatus.OPEN.value),
    )
    resolution_notes: Optional[str] = Field(default=None)
    resolved_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    customer: User = Relationship(back_populates="complaints")
    order: Optional[Order] = Relationship(back_populates="complaints")
    driver_profile: Optional[DriverProfile] = Relationship(back_populates="complaints")
    region: Optional[Region] = Relationship(back_populates="complaints")


class DriverLedgerEntry(SQLModel, table=True):
    """Unified driver ledger for payable, receivable, and adjustments."""

    __tablename__ = "driver_ledger_entry"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    driver_profile_id: int = Field(foreign_key="driver_profile.id", nullable=False, index=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id", index=True)
    entry_type: LedgerEntryType = Field(
        default=LedgerEntryType.PAYABLE,
        sa_column=Column(String(20), nullable=False, server_default=LedgerEntryType.PAYABLE.value),
    )
    amount: float = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    description: Optional[str] = Field(default=None)
    entry_date: date = Field(default_factory=date.today)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    driver_profile: DriverProfile = Relationship(back_populates="ledger_entries")
    order: Optional[Order] = Relationship(back_populates="ledger_entries")


class ProofAttachment(SQLModel, table=True):
    """File metadata for delivery proof uploads."""

    __tablename__ = "proof_attachment"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    order_id: int = Field(foreign_key="order.id", nullable=False, index=True)
    uploaded_by_driver_profile_id: int = Field(foreign_key="driver_profile.id", nullable=False, index=True)
    object_key: str = Field(nullable=False, unique=True)
    original_filename: str = Field(nullable=False)
    content_type: Optional[str] = Field(default=None)
    size_bytes: int = Field(nullable=False, ge=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    order: Order = Relationship(back_populates="proof_attachments")
    uploaded_by_driver: DriverProfile = Relationship(back_populates="proof_uploads")


class RecurringOrderTemplate(SQLModel, table=True):
    """Recurring order definition for daily generation jobs."""

    __tablename__ = "recurring_order_template"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    customer_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    region_id: int = Field(foreign_key="region.id", nullable=False, index=True)
    slot_id: int = Field(foreign_key="delivery_slot.id", nullable=False, index=True)
    restaurant_id: Optional[int] = Field(default=None, foreign_key="restaurant.id", index=True)
    is_active: bool = Field(default=True)
    includes_restaurant: bool = Field(default=False)
    grocery_payload: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))
    restaurant_order_notes: Optional[str] = Field(default=None)
    additional_notes: Optional[str] = Field(default=None)
    start_date: date = Field(default_factory=date.today)
    end_date: Optional[date] = Field(default=None)
    last_generated_for_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    customer: User = Relationship(back_populates="recurring_templates")
    region: Region = Relationship(back_populates="recurring_templates")
    slot: DeliverySlot = Relationship(back_populates="recurring_templates")
    restaurant: Optional[Restaurant] = Relationship(back_populates="recurring_templates")


class Item(SQLModel, table=True):
    """Legacy sample item table retained during early migration"""

    __tablename__ = "item"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    name: str = Field(nullable=False, index=True)
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationships
    user: Optional["User"] = Relationship(back_populates="items")
