from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import (
    AnyUrl,
    AwareDatetime,
    BaseModel,
    Field,
    RootModel,
)


class Address(BaseModel):
    addressCountry: Optional[str] = Field(
        None, description="The country. For example, Spain"
    )
    addressLocality: Optional[str] = Field(
        None,
        description="The locality in which the street address is, and which is in the region",
    )
    addressRegion: Optional[str] = Field(
        None,
        description="The region in which the locality is, and which is in the country",
    )
    district: Optional[str] = Field(
        None,
        description="A district is a type of administrative division that, in some countries, is managed by the local government",
    )
    postOfficeBoxNumber: Optional[str] = Field(
        None,
        description="The post office box number for PO box addresses. For example, 03578",
    )
    postalCode: Optional[str] = Field(
        None, description="The postal code. For example, 24004"
    )
    streetAddress: Optional[str] = Field(None, description="The street address")
    streetNr: Optional[str] = Field(
        None, description="Number identifying a specific property on a public street"
    )


class Type(Enum):
    Point = "Point"


class Location(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[float] = Field(..., min_length=2)
    type: Type


class Coordinate(RootModel[List[float]]):
    root: List[float]


class Type1(Enum):
    LineString = "LineString"


class Location1(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[Coordinate] = Field(..., min_length=2)
    type: Type1


class Type2(Enum):
    Polygon = "Polygon"


class Location2(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[Coordinate]]
    type: Type2


class Type3(Enum):
    MultiPoint = "MultiPoint"


class Location3(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[float]]
    type: Type3


class Type4(Enum):
    MultiLineString = "MultiLineString"


class Location4(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[Coordinate]]
    type: Type4


class Type5(Enum):
    MultiPolygon = "MultiPolygon"


class Location5(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[List[Coordinate]]]
    type: Type5


class Type6(Enum):
    AirQualityObserved = "AirQualityObserved"


class TypeofLocation(Enum):
    indoor = "indoor"
    outdoor = "outdoor"


class AirQualityObserved(BaseModel):
    address: Optional[Address] = Field(None, description="The mailing address")
    airQualityIndex: Optional[float] = Field(
        None,
        description="Air quality index is a number used to report the quality of the air on any given day",
        ge=0.0,
    )
    airQualityLevel: Optional[str] = Field(
        None,
        description="Overall qualitative level of health concern corresponding to the air quality observed",
        min_length=2,
    )
    alternateName: Optional[str] = Field(
        None, description="An alternative name for this item"
    )
    areaServed: Optional[str] = Field(
        None,
        description="Higher level area to which this air quality measurement belongs to",
    )
    as_: Optional[float] = Field(
        None, alias="as", description="Arsenic detected", ge=0.0
    )
    c6h6: Optional[float] = Field(None, description="Benzene detected", ge=0.0)
    cd: Optional[float] = Field(None, description="Cadmium detected", ge=0.0)
    co: Optional[float] = Field(None, description="Carbon Monoxide detected", ge=0.0)
    co2: Optional[float] = Field(None, description="Carbon Dioxide detected", ge=0.0)
    coLevel: Optional[str] = Field(
        None, description="Qualitative Carbon Monoxide presence"
    )
    dataProvider: Optional[str] = Field(
        None,
        description="A sequence of characters identifying the provider of the harmonised data entity",
    )
    dateCreated: Optional[AwareDatetime] = Field(
        None,
        description="Entity creation timestamp. This will usually be allocated by the storage platform",
    )
    dateModified: Optional[AwareDatetime] = Field(
        None,
        description="Timestamp of the last modification of the entity. This will usually be allocated by the storage platform",
    )
    dateObserved: Optional[AwareDatetime] = Field(
        None, description="The date and time of this observation in ISO8601 UTCformat"
    )
    description: Optional[str] = Field(None, description="A description of this item")
    id: Optional[
        Union[
            str,
            AnyUrl,
        ]
    ] = Field(None, description="Unique identifier of the entity")
    location: Optional[
        Union[Location, Location1, Location2, Location3, Location4, Location5]
    ] = Field(
        None,
        description="Geojson reference to the item. It can be Point, LineString, Polygon, MultiPoint, MultiLineString or MultiPolygon",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
        min_length=1,
        max_length=256,
    )
    name: Optional[str] = Field(None, description="The name of this item")
    ni: Optional[float] = Field(None, description="Nickel detected", ge=0.0)
    no: Optional[float] = Field(None, description="Nitrogen monoxide detected", ge=0.0)
    no2: Optional[float] = Field(None, description="Nitrogen dioxide detected", ge=0.0)
    nox: Optional[float] = Field(None, description="Other Nitrogen oxides detected")
    o3: Optional[float] = Field(None, description="Ozone detected ")
    owner: Optional[
        List[
            Union[
                str,
                AnyUrl,
            ]
        ]
    ] = Field(
        None,
        description="A List containing a JSON encoded sequence of characters referencing the unique Ids of the owner(s)",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!,:\\\\]+$",
        min_length=1,
        max_length=256,
    )
    pb: Optional[float] = Field(None, description="Lead detected   ")
    pm1: Optional[float] = Field(
        None, description="Particulate matter 1 micrometers or less in diameter", ge=0.0
    )
    pm10: Optional[float] = Field(
        None,
        description="Particulate matter 10 micrometers or less in diameter",
        ge=0.0,
    )
    pm25: Optional[float] = Field(
        None,
        description="Particulate matter 2.5 micrometers or less in diameter",
        ge=0.0,
    )
    precipitation: Optional[float] = Field(
        None, description="Amount of water rain", ge=0.0
    )
    refDevice: Optional[
        Union[
            str,
            AnyUrl,
        ]
    ] = Field(
        None,
        description="A reference to the device(s) which captured this observation",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
        min_length=1,
        max_length=256,
    )
    refPointOfInterest: Optional[
        Union[
            str,
            AnyUrl,
        ]
    ] = Field(
        None,
        description="A reference to a point of interest (usually an air quality station) associated to this observation",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
        min_length=1,
        max_length=256,
    )
    refWeatherObserved: Optional[
        Union[
            str,
            AnyUrl,
        ]
    ] = Field(
        None,
        description="Weather observed associated to the air quality conditions described by this entity",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
        min_length=1,
        max_length=256,
    )
    relativeHumidity: Optional[float] = Field(
        None,
        description="Relative Humidity of the air (a number between 0 and 1 representing the range of 0% to 100%)",
        ge=0.0,
        le=1.0,
    )
    reliability: Optional[float] = Field(
        None,
        description="Reliability (percentage, expressed in parts per one) corresponding to the air quality observed",
        ge=0.0,
        le=1.0,
    )
    seeAlso: Optional[Union[List[AnyUrl], AnyUrl]] = Field(
        None, description="list of uri pointing to additional resources about the item"
    )
    sh2: Optional[float] = Field(None, description="Hydrogen sulfide detected", ge=0.0)
    so2: Optional[float] = Field(None, description="Sulfur dioxide detected", ge=0.0)
    source: Optional[str] = Field(
        None,
        description="A sequence of characters giving the original source of the entity data as a URL. Recommended to be the fully qualified domain name of the source provider, or the URL to the source object",
    )
    temperature: Optional[float] = Field(None, description="Temperature of the item")
    type: Optional[Type6] = Field(
        None, description="NGSI Entity type. It has to be AirQualityObserved"
    )
    typeofLocation: Optional[TypeofLocation] = Field(
        None, description="Type of location of the sampled item"
    )
    volatileOrganicCompoundsTotal: Optional[float] = Field(
        None,
        description="Alkanes <C10, ketones <C6, aldehydes <C10, carboxylic acids <C5, aspirits<C7, Alkenes <C8, Aromatics",
    )
    windDirection: Optional[float] = Field(
        None, description="Direction of the weather vane", ge=-180.0, le=180.0
    )
    windSpeed: Optional[float] = Field(
        None, description="Intensity of the wind", ge=0.0
    )
