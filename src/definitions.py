from io import StringIO
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Optional, Union, Generic, TypeVar, Dict, Iterable
from datetime import date
from enum import StrEnum

T = TypeVar("T")


def _snake_to_camel_case(string: str) -> str:
    strio = StringIO()
    components = string.split("_")
    for idx, component in enumerate(components):
        if idx == 0:
            # since the conversion is to camel case, we do not capitalize the first component
            strio.write(component)
            continue
        strio.write(component.capitalize())

    return strio.getvalue()


class ProviderType(StrEnum):
    EXPRESS = "express"
    PARCEL = "parcel"


class LocationType(StrEnum):
    SERVICE_POINT = "servicepoint"
    LOCKER = "locker"
    POST_OFFICE = "postoffice"
    POSTBANK = "postbank"
    POBOX = "pobox"
    POSTBOX = "postbox"


class ServiceType(StrEnum):
    PARCEL_PICK_UP_ALL = "parcel:pick-up-all"
    PARCEL_DROP_OFF_ALL = "parcel:drop-off-all"
    AGE_VERIFICATION = "age-verification"
    CASH_ON_DELIVERY = "cash-on-delivery"
    CASH_SERVICE = "cash-service"
    EXPRESS_DROP_OFF = "express:drop-off"
    EXPRESS_DROP_OFF_ACCOUNT = "express:drop-off-account"
    EXPRESS_DROP_OFF_EASY = "express:drop-off-easy"
    EXPRESS_DROP_OFF_PRELABELED = "express:drop-off-prelabeled"
    EXPRESS_DROP_OFF_UNLABELED = "express:drop-off-unlabeled"
    EXPRESS_PICK_UP = "express:pick-up"
    FRANKING = "franking"
    HANDICAPPED_ACCESS = "handicapped-access"
    LETTER_SERVICE = "letter-service"
    PACKAGING_MATERIAL = "packaging-material"
    PARCEL_DROP_OFF = "parcel:drop-off"
    PARCEL_DROP_OFF_FIRSTMILE = "parcel:drop-off-firstmile"
    PARCEL_DROP_OFF_FIRSTMILE_UNLABELED = "parcel:drop-off-firstmile-unlabeled"
    PARCEL_DROP_OFF_RETURN = "parcel:drop-off-return"
    PARCEL_DROP_OFF_RETURN_UNLABELED = "parcel:drop-off-return-unlabeled"
    PARCEL_DROP_OFF_UNLABELED = "parcel:drop-off-unlabeled"
    PARCEL_DROP_OFF_UNREGISTERED = "parcel:drop-off-unregistered"
    PARCEL_PICK_UP = "parcel:pick-up"
    PARCEL_PICK_UP_REGISTERED = "parcel:pick-up-registered"
    PARCEL_PICK_UP_UNREGISTERED = "parcel:pick-up-unregistered"
    PARKING = "parking"
    POSTBANK = "postbank"
    POSTIDENT = "postident"


class QueryParam(ABC):

    @abstractmethod
    def to_request_format(self) -> Dict[str, str]:
        pass


@dataclass
class FindByKeywordIdQueryParams(QueryParam):
    keyword_id: str
    country_code: str
    postal_code: str

    def to_request_format(self) -> Dict[str, str]:
        return {
            _snake_to_camel_case(field.name): self.__getattribute__(field.name) for field in fields(self)
        }


@dataclass
class FindByAddressQueryParams(QueryParam):
    country_code: str
    address_locality: Optional[str] = None
    postal_code: Optional[str] = None
    street_address: Optional[str] = None
    provider_type: Optional[Iterable[ProviderType]] = None
    location_type: Optional[Iterable[LocationType]] = None
    service_type: Optional[Iterable[ServiceType]] = None
    radius: float = 5000
    limit: int = 15
    hide_closed_locations: bool = False
    current_date: Optional[date] = None

    def to_request_format(self) -> Dict[str, str]:
        api_format = dict()
        for field in fields(self):
            if self.__getattribute__(field.name) is None:
                api_format[_snake_to_camel_case(field.name)] = None
            elif field.name in ["provider_type", "location_type", "service_type"]:
                api_format[_snake_to_camel_case(field.name)] = [str(f.value) for f in self.__getattribute__(field.name)]
            elif field.name in ["current_date"]:
                api_format[_snake_to_camel_case(field.name)] = str(self.__getattribute__(field.name))
            else:
                api_format[_snake_to_camel_case(field.name)] = self.__getattribute__(field.name)

        return api_format


@dataclass
class FindByGeoQueryParams(QueryParam):
    latitude: float
    longitude: float
    provider_type: Optional[Iterable[ProviderType]] = None
    location_type: Optional[Iterable[LocationType]] = None
    service_type: Optional[Iterable[ServiceType]] = None
    radius: float = 5000
    limit: int = 15
    country_code: Optional[str] = None
    hide_closed_locations: bool = False
    current_date: Optional[date] = None

    def to_request_format(self) -> Dict[str, str]:
        api_format = dict()
        for field in fields(self):
            if self.__getattribute__(field.name) is None:
                api_format[_snake_to_camel_case(field.name)] = None
            elif field.name in ["provider_type", "location_type", "service_type"]:
                api_format[_snake_to_camel_case(field.name)] = [str(f.value) for f in self.__getattribute__(field.name)]
            elif field.name in ["current_date"]:
                api_format[_snake_to_camel_case(field.name)] = str(self.__getattribute__(field.name))
            else:
                api_format[_snake_to_camel_case(field.name)] = self.__getattribute__(field.name)

        return api_format


@dataclass
class FailureResponse:
    status: str
    title: Optional[str] = None
    detail: Optional[str] = None


@dataclass
class DhlResponse(Generic[T]):
    response: Union[T, FailureResponse]
    failed: bool
