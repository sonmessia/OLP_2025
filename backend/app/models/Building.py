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


class CategoryEnum(Enum):
    apartments = "apartments"
    bakehouse = "bakehouse"
    barn = "barn"
    bridge = "bridge"
    bungalow = "bungalow"
    bunker = "bunker"
    cathedral = "cathedral"
    cabin = "cabin"
    carport = "carport"
    cemetery = "cemetery"
    chapel = "chapel"
    church = "church"
    civic = "civic"
    commercial = "commercial"
    conservatory = "conservatory"
    construction = "construction"
    cowshed = "cowshed"
    detached = "detached"
    digester = "digester"
    dormitory = "dormitory"
    farm = "farm"
    farm_auxiliary = "farm_auxiliary"
    garage = "garage"
    garages = "garages"
    garbage_shed = "garbage_shed"
    grandstand = "grandstand"
    greenhouse = "greenhouse"
    hangar = "hangar"
    hospital = "hospital"
    hotel = "hotel"
    house = "house"
    houseboat = "houseboat"
    hut = "hut"
    industrial = "industrial"
    kindergarten = "kindergarten"
    kiosk = "kiosk"
    mosque = "mosque"
    office = "office"
    parking = "parking"
    pavilion = "pavilion"
    public = "public"
    residential = "residential"
    retail = "retail"
    riding_hall = "riding_hall"
    roof = "roof"
    ruins = "ruins"
    school = "school"
    service = "service"
    shed = "shed"
    shrine = "shrine"
    stable = "stable"
    stadium = "stadium"
    static_caravan = "static_caravan"
    sty = "sty"
    synagogue = "synagogue"
    temple = "temple"
    terrace = "terrace"
    train_station = "train_station"
    transformer_tower = "transformer_tower"
    transportation = "transportation"
    university = "university"
    warehouse = "warehouse"
    water_tower = "water_tower"


class Type(Enum):
    Point = "Point"


class ContainedInPlace(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[float] = Field(..., min_length=2)
    type: Type


class Coordinate(RootModel[List[float]]):
    root: List[float]


class Type1(Enum):
    LineString = "LineString"


class ContainedInPlace1(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[Coordinate] = Field(..., min_length=2)
    type: Type1


class Type2(Enum):
    Polygon = "Polygon"


class ContainedInPlace2(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[Coordinate]]
    type: Type2


class Type3(Enum):
    MultiPoint = "MultiPoint"


class ContainedInPlace3(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[float]]
    type: Type3


class Type4(Enum):
    MultiLineString = "MultiLineString"


class ContainedInPlace4(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[Coordinate]]
    type: Type4


class Type5(Enum):
    MultiPolygon = "MultiPolygon"


class ContainedInPlace5(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[List[Coordinate]]]
    type: Type5


class Type6(Enum):
    Point = "Point"


class Location(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[float] = Field(..., min_length=2)
    type: Type6


class Type7(Enum):
    LineString = "LineString"


class Location1(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[Coordinate] = Field(..., min_length=2)
    type: Type7


class Type8(Enum):
    Polygon = "Polygon"


class Location2(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[Coordinate]]
    type: Type8


class Type9(Enum):
    MultiPoint = "MultiPoint"


class Location3(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[float]]
    type: Type9


class Type10(Enum):
    MultiLineString = "MultiLineString"


class Location4(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[Coordinate]]
    type: Type10


class Type11(Enum):
    MultiPolygon = "MultiPolygon"


class Location5(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[List[Coordinate]]]
    type: Type11


class Type12(Enum):
    Building = "Building"


class Building(BaseModel):
    address: Optional[Address] = Field(None, description="The mailing address")
    alternateName: Optional[str] = Field(
        None, description="An alternative name for this item"
    )
    areaServed: Optional[str] = Field(
        None,
        description="The geographic area where a service or offered item is provided",
    )
    category: Optional[List[CategoryEnum]] = Field(
        None,
        description="Category of the building. Enum:'apartments, bakehouse, barn, bridge, bungalow, bunker, cathedral, cabin, carport, chapel, church, civic, commercial, conservatory, construction, cowshed, detached, digester, dormitory, farm, farm_auxiliary, garage, garages, garbage_shed, grandstand, greenhouse, hangar, hospital, hotel, house, houseboat, hut, industrial, kindergarten, kiosk, mosque, office, parking, pavilion, public, residential, retail, riding_hall, roof, ruins, school, service, shed, shrine, stable, stadium, static_caravan, sty, synagogue, temple, terrace, train_station, transformer_tower, transportation, university, warehouse, water_tower'",
    )
    collapseRisk: Optional[float] = Field(
        None,
        description="Probability of total collapse of the building",
        ge=0.0,
        le=1.0,
    )
    containedInPlace: Optional[
        Union[
            ContainedInPlace,
            ContainedInPlace1,
            ContainedInPlace2,
            ContainedInPlace3,
            ContainedInPlace4,
            ContainedInPlace5,
        ]
    ] = Field(
        None,
        description="Geojson reference to the item. It can be Point, LineString, Polygon, MultiPoint, MultiLineString or MultiPolygon",
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
    description: Optional[str] = Field(None, description="A description of this item")
    floorsAboveGround: Optional[float] = Field(
        None, description="Floors above the ground level"
    )
    floorsBelowGround: Optional[float] = Field(
        None, description="Floors below the ground level"
    )
    id: Optional[
        Union[
            str,
            AnyUrl,
        ]
    ] = Field(
        None,
        description="Unique identifier of the entity",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
        min_length=1,
        max_length=256,
    )
    location: Optional[
        Union[Location, Location1, Location2, Location3, Location4, Location5]
    ] = Field(
        None,
        description="Geojson reference to the item. It can be Point, LineString, Polygon, MultiPoint, MultiLineString or MultiPolygon",
    )
    mapUrl: Optional[
        Union[
            str,
            AnyUrl,
        ]
    ] = Field(
        None,
        description="Reference to the map containing the building",
    )
    name: Optional[str] = Field(
        None,
        description="The name of this item",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
        min_length=1,
        max_length=256,
    )
    occupier: Optional[
        List[
            Union[
                str,
                AnyUrl,
            ]
        ]
    ] = Field(
        None,
        description="Person or entity using the building",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!,:\\\\]+$",
        min_length=1,
        max_length=256,
    )
    openingHours: Optional[List[str]] = Field(
        None, description="Opening hours of this building"
    )
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
    peopleCapacity: Optional[float] = Field(
        None, description="Allowed people present at the building", ge=0.0
    )
    peopleOccupancy: Optional[float] = Field(
        None, description="People present at the building", ge=0.0
    )
    seeAlso: Optional[Union[List[AnyUrl], AnyUrl]] = Field(
        None, description="list of uri pointing to additional resources about the item"
    )
    source: Optional[str] = Field(
        None,
        description="A sequence of characters giving the original source of the entity data as a URL. Recommended to be the fully qualified domain name of the source provider, or the URL to the source object",
    )
    type: Optional[Type12] = Field(None, description="NGSI Entity type")
