from typing import Dict, Any, Optional, List, Union
from abc import ABC

import requests

from schemas import DhlLocation
from definitions import (
    QueryParam,
    FailureResponse,
    DhlResponse,
    FindByKeywordIdQueryParams,
    FindByGeoQueryParams,
    FindByAddressQueryParams,
)


class _DhlClient(ABC):
    def __init__(self, api_key: str, api_url: str) -> None:
        self._api_key = api_key
        self.api_url = api_url if api_url.endswith("/") else f"{api_url}/"

    def _get_request_headers(self) -> Dict[str, Any]:
        return {
            "DHL-API-Key": self._api_key
        }


class DhlLocationFinderClient(_DhlClient):
    def __init__(self, api_key: str, api_url: str = "https://api.dhl.com/") -> None:
        super().__init__(api_key=api_key, api_url=api_url)

    def _call_endpoint(
        self, endpoint: str, params: Optional[QueryParam], parse_to_iterable: bool = False
    ) -> DhlResponse[Union[DhlLocation, List[DhlLocation]]]:
        response: requests.Response = requests.get(
            url=endpoint,
            headers=self._get_request_headers(),
            params=params.to_request_format() if params else None
        )

        if response.status_code == 200:

            if parse_to_iterable:
                dhl_location_data = [DhlLocation(**data) for data in response.json().get("locations", [])]
            else:
                dhl_location_data = DhlLocation(**response.json())

            return DhlResponse(
                response=dhl_location_data,
                failed=False
            )

        return DhlResponse(
            response=FailureResponse(**response.json()),
            failed=True
        )

    def find_by_address(self, params: FindByAddressQueryParams) -> DhlResponse[List[DhlLocation]]:
        """
        Search for DHL Service Point locations by address.
        """
        endpoint = self.api_url + "location-finder/v1/find-by-address"

        return self._call_endpoint(endpoint=endpoint, params=params, parse_to_iterable=True)

    def find_by_geo(self, params: FindByGeoQueryParams) -> DhlResponse[List[DhlLocation]]:
        """
        Search for DHL Service Point locations by geo coordinates.
        """
        endpoint = self.api_url + "location-finder/v1/find-by-geo"

        return self._call_endpoint(endpoint=endpoint, params=params, parse_to_iterable=True)

    def find_by_keyword_id(self, params: FindByKeywordIdQueryParams) -> DhlResponse[DhlLocation]:
        """
        Search for DHL Service Point locations by keyword ID.
        """
        endpoint = self.api_url + "location-finder/v1/find-by-keyword-id"

        return self._call_endpoint(endpoint=endpoint, params=params)

    def find_by_location_id(self, location_id: str) -> DhlResponse[DhlLocation]:
        """
        Retrieve one DHL Service Point location by its ID.
        """
        endpoint = self.api_url + f"location-finder/v1/locations/{location_id}"

        return self._call_endpoint(endpoint=endpoint, params=None)
