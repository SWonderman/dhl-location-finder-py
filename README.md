### Introduction
You are looking at a simple Python wrapper for the [DHL's Location Finder - Unified](https://developer.dhl.com/api-reference/location-finder-unified?language_content_entity=en#reference-docs-section) API (v 1.9.5).

The wrapper uses [Pydantic](https://docs.pydantic.dev/latest/) for schema validation and [requests](https://pypi.org/project/requests/) for communication with DHL endpoints.

### Requirements
* Python 3.11 (because of the usage of StrEnum) or later

### Examples
#### Finding a Service Point by keyword ID
```python
from client import DhlLocationFinderClient
from definitions import DhlResponse, FindByKeywordIdQueryParams
from schemas import DhlLocation

client = DhlLocationFinderClient(
    api_key="<your_key>",
)

result: DhlResponse[DhlLocation] = client.find_by_keyword_id(params=FindByKeywordIdQueryParams(
    keyword_id="134",
    country_code="DE",
    postal_code="12249",
))

```

#### Finding a Service Point by address
```python
from typing import List

from client import DhlLocationFinderClient
from definitions import DhlResponse, FindByAddressQueryParams, ProviderType
from schemas import DhlLocation

client = DhlLocationFinderClient(
    api_key="<your_key>",
)

response: DhlResponse[List[DhlLocation]] = client.find_by_address(params=FindByAddressQueryParams(
    country_code="DE",
    address_locality="Berlin",
    postal_code="12249",
    provider_type=[ProviderType.PARCEL]
))
```

#### Finding a Service Point by geo coordinates
```python
from typing import List

from client import DhlLocationFinderClient
from definitions import DhlResponse, FindByGeoQueryParams
from schemas import DhlLocation

client = DhlLocationFinderClient(
    api_key="<your_key>",
)

response: DhlResponse[List[DhlLocation]] = client.find_by_geo(params=FindByGeoQueryParams(
    latitude=52.421132,
    longitude=13.35927,
))
```

#### Finding a Service Point by location ID
```python
from client import DhlLocationFinderClient
from definitions import DhlResponse
from schemas import DhlLocation

client = DhlLocationFinderClient(
    api_key="<your_key>",
)

response: DhlResponse[DhlLocation] = client.find_by_location_id(location_id="8007-412249134")
```

### How to handle responses
Every call on the `DhlLocationFinderClient` instance will return an instance of `DhlResponse`. In the Golang-like fashion, `DhlResponse` will carry information about the status of the operation, meaning, if the call to the API failed or succeeded, and the associated data. 

The status will dictate what object is returned with the response. If the call to the API was successful, a `DhlLocation` (or a `List[DhlLocation]`) object will be returned. On failure, a `FailureResponse` object will be returned carrying data on what went wrong.

Example:
```python
client = DhlLocationFinderClient(
    api_key="<your_key>",
)

result: DhlResponse[DhlLocation] = client.find_by_location_id(location_id="8007-412249134")

if result.failed:
    # handle error - DhlResponse carries FailureResponse object
    failed_response: FailureResponse = result.response
    logger.error(msg=f"Something went wrong by finding Service Point by location ID. Response status: {failed_response.status}, title: {failed_response.title}, details: {failed_response.detail}")
    return

# success - DhlResponse carries DhlLocation object
return result.response
```