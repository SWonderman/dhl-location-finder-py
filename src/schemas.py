from typing import Optional, Union, List
from datetime import datetime, date, time

from pydantic import BaseModel, Field


class BusinessUnit(BaseModel):
    id: str = Field(validation_alias="locationId")
    provider: str


class Location(BaseModel):
    ids: List[BusinessUnit]
    keyword: str
    keyword_id: str = Field(validation_alias="keywordId")
    type: str
    is_lean_locker: Optional[bool] = Field(default=None, validation_alias="leanLocker")


class Address(BaseModel):
    country_code: str = Field(min_length=2, max_length=2, validation_alias="countryCode", description="Following ISO 3166-1 alpha-2")
    postal_code: str = Field(validation_alias="postalCode")
    address_locality: str = Field(validation_alias="addressLocality")
    street_address: str = Field(validation_alias="streetAddress")


class Geo(BaseModel):
    latitude: float
    longitude: float


class ContainedInPlace(BaseModel):
    name: str


class Place(BaseModel):
    address: Address
    geo: Geo
    contained_in: Optional[ContainedInPlace] = Field(default=None, validation_alias="containedInPlace")


class OpeningHours(BaseModel):
    opens_at: time = Field(validation_alias="opens")
    closes_at: time = Field(validation_alias="closes")
    day_link: str = Field(validation_alias="dayOfWeek")


class ClosurePeriod(BaseModel):
    type: str
    from_date: Union[datetime, date] = Field(validation_alias="fromDate")
    to_date: Union[datetime, date] = Field(validation_alias="to_date")


class AverageCapacityPerDay(BaseModel):
    day: str = Field(validation_alias="dayOfWeek")
    capacity: str


class DhlLocation(BaseModel):
    url: str
    location: Location
    name: str
    distance: Optional[int] = Field(default=None)
    place: Place
    opening_hours: List[OpeningHours] = Field(default_factory=list, validation_alias="openingHours")
    closure_periods: List[ClosurePeriod] = Field(default_factory=list, validation_alias="closurePeriods")
    service_types: List[str] = Field(default_factory=list, validation_alias="serviceTypes")
    available_capacity: Optional[str] = Field(default=None, validation_alias="availableCapacity")
    average_capacity_per_day: List[AverageCapacityPerDay] = Field(default_factory=list, validation_alias="averageCapacityDayOfWeek")
