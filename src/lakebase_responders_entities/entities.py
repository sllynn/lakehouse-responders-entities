import uuid

from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel, LargeBinary, Column


class VehicleType(str, Enum):
    car = "Auto"
    van = "Lieferwagen"


class ServiceType(str, Enum):
    fire = "Feuerwehr"
    police = "Polizei"
    medical = "Rettungsdienst"


class Vehicle(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    service_type: ServiceType
    vehicle_type: VehicleType
    registration: str = Field(max_length=10)
    capacity: int = Field(ge=1)
    lon: float = Field(ge=-180, le=180)
    lat: float = Field(ge=-90, le=90)


class UrgencyLevel(str, Enum):
    low = "Niedrig"
    medium = "Mittel"
    high = "Hoch"


class Emergency(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    service_type: ServiceType
    transcript: str = Field(max_length=1000)
    address: str = Field(max_length=1000)
    urgency: UrgencyLevel
    lon: float = Field(ge=-180, le=180)
    lat: float = Field(ge=-90, le=90)
    reported: datetime = Field(default_factory=datetime.utcnow)


class Plan(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    vehicle_id: uuid.UUID = Field(foreign_key="vehicle.id")
    plan_index: int = Field(ge=0)
    emergency_id: uuid.UUID = Field(foreign_key="emergency.id")
    route: bytes = Field(sa_column=Column(LargeBinary))
    eta: datetime = Field()
