from unittest import TestCase
from datetime import date

from src.definitions import FindByKeywordIdQueryParams, FindByAddressQueryParams, ProviderType, LocationType, FindByGeoQueryParams


class TestDefinitions(TestCase):
    def test_find_by_keyword_id_query_param_to_request_format(self) -> None:
        params = FindByKeywordIdQueryParams(
            keyword_id="153",
            country_code="DE",
            postal_code="112233",
        )

        expected = {
            "keywordId": "153",
            "countryCode": "DE",
            "postalCode": "112233"
        }

        self.assertEqual(params.to_request_format(), expected)

    def test_find_by_address_query_param_to_request_format(self) -> None:
        params = FindByAddressQueryParams(
            country_code="DE",
            address_locality="Berlin",
            postal_code="112233",
            street_address="Frankfurter Landstrasse 107",
            provider_type=[ProviderType.EXPRESS, ProviderType.PARCEL],
            location_type=[LocationType.LOCKER, LocationType.POBOX, LocationType.POST_OFFICE],
            service_type=None,
            current_date=date(2024, 6, 15),
        )

        expected = {
            "countryCode": "DE",
            "addressLocality": "Berlin",
            "postalCode": "112233",
            "streetAddress": "Frankfurter Landstrasse 107",
            "providerType": ["express", "parcel"],
            "locationType": ["locker", "pobox", "postoffice"],
            "serviceType": None,
            "radius": 5000,
            "limit": 15,
            "hideClosedLocations": False,
            "currentDate": "2024-06-15"
        }

        self.assertEqual(params.to_request_format(), expected)

    def test_find_by_geo_query_param_to_request_format(self) -> None:
        params = FindByGeoQueryParams(
            latitude=50.7160027,
            longitude=7.1300817,
            provider_type=[ProviderType.EXPRESS, ProviderType.PARCEL],
            location_type=[LocationType.LOCKER, LocationType.POBOX, LocationType.POST_OFFICE],
            service_type=None,
            current_date=date(2024, 6, 15),
        )

        expected = {
            "latitude": 50.7160027,
            "longitude": 7.1300817,
            "providerType": ["express", "parcel"],
            "locationType": ["locker", "pobox", "postoffice"],
            "serviceType": None,
            "radius": 5000,
            "limit": 15,
            "countryCode": None,
            "hideClosedLocations": False,
            "currentDate": "2024-06-15",
        }

        self.assertEqual(params.to_request_format(), expected)
