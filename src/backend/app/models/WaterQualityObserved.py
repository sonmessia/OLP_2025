# Copyright (c) 2025 Green Wave Team
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

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
    WaterQualityObserved = "WaterQualityObserved"


class WaterQualityObserved(BaseModel):
    Al: Optional[float] = Field(
        None, description="Aluminium. Concentration of aluminium", ge=0.0
    )
    As: Optional[float] = Field(
        None, description="Arsenic. Concentration of arsenic", ge=0.0
    )
    B: Optional[float] = Field(
        None, description="Boron. Concentration of boron", ge=0.0
    )
    Ba: Optional[float] = Field(
        None, description="Barium. Concentration of barium", ge=0.0
    )
    Cd: Optional[float] = Field(
        None, description="Cadmium. Concentration of cadmium", ge=0.0
    )
    Chla: Optional[float] = Field(
        None, description="Concentration of chlorophyll A", ge=0.0
    )
    Cl_: Optional[float] = Field(
        None, alias="Cl-", description="Concentration of chlorides", ge=0.0
    )
    Cr: Optional[float] = Field(
        None, description="Chromium. Concentration of chromium", ge=0.0
    )
    Cr_III: Optional[float] = Field(
        None,
        alias="Cr-III",
        description="Chromium III. Concentration of chromium at the oxidation state +3",
        ge=0.0,
    )
    Cr_VI: Optional[float] = Field(
        None,
        alias="Cr-VI",
        description="Chromium VI. Concentration of chromium at the oxidation state +6",
        ge=0.0,
    )
    Cu: Optional[float] = Field(
        None, description="Copper. Concentration of copper", ge=0.0
    )
    Fe: Optional[float] = Field(None, description="Iron. Concentration of iron", ge=0.0)
    Hg: Optional[float] = Field(
        None, description="Mercury. Concentration of mercury", ge=0.0
    )
    N_TOT: Optional[float] = Field(
        None,
        alias="N-TOT",
        description="Total Nitrogen. Total Nitrogen (TN) is the sum of nitrate-nitrogen (NO3-N), nitrite-nitrogen (NO2-N), ammonia-nitrogen (NH3-N) and organically bonded nitrogen",
        ge=0.0,
    )
    NH3: Optional[float] = Field(None, description="Concentration of ammonia", ge=0.0)
    NH4: Optional[float] = Field(None, description="Concentration of ammonium", ge=0.0)
    NO2: Optional[float] = Field(
        None,
        description="Nitrite nitrogen. Concentration of a sample in nitrite nitrogen",
        ge=0.0,
    )
    NO3: Optional[float] = Field(None, description="Concentration of nitrates", ge=0.0)
    Ni: Optional[float] = Field(
        None, description="Nickel. Concentration of Nickel", ge=0.0
    )
    O2: Optional[float] = Field(
        None, description="Level of free, non-compound oxygen present", ge=0.0
    )
    P_PO4: Optional[float] = Field(
        None,
        alias="P-PO4",
        description="Phosphate-phosphorus. Concentration of phosphorus as phosphate",
        ge=0.0,
    )
    P_TOT: Optional[float] = Field(
        None,
        alias="P-TOT",
        description="Total Phosphorus. Total phosphorus is a measure of all forms of\\xa0phosphorus\\xa0in the water, including dissolved and particulate, organic and inorganic",
        ge=0.0,
    )
    PC: Optional[float] = Field(
        None,
        description="Concentration of pigment phycocyanin which can be measured to estimate cyanobacteria concentrations specifically",
        ge=0.0,
    )
    PE: Optional[float] = Field(
        None,
        description="Concentration of pigment phycoerythrin which can be measured to estimate cyanobacteria concentrations specifically",
        ge=0.0,
    )
    PO4: Optional[float] = Field(
        None, description="Concentration of phosphates", ge=0.0
    )
    Pb: Optional[float] = Field(None, description="Lead. Concentration of lead", ge=0.0)
    Se: Optional[float] = Field(
        None, description="Selenium. Concentration of selenium", ge=0.0
    )
    Sn: Optional[float] = Field(None, description="Tin. Concentration of tin", ge=0.0)
    THC: Optional[float] = Field(
        None,
        description="Total hydrocarbon. Concentration of total hydrocarbon",
        ge=0.0,
    )
    TKN: Optional[float] = Field(
        None,
        description="Total Kjeldahl Nitrogen. A measure that determines both the organic and the inorganic forms of nitrogen",
        ge=0.0,
    )
    TO: Optional[float] = Field(
        None, description="Total oil content. Concentration of oil", ge=0.0
    )
    Zn: Optional[float] = Field(None, description="Zinc. Concentration of zinc", ge=0.0)
    address: Optional[Address] = Field(None, description="The mailing address")
    alkalinity: Optional[float] = Field(
        None,
        description="The alkalinity of water is its acid-neutralizing capacity comprised of the total of all titratable bases",
        ge=0.0,
    )
    alternateName: Optional[str] = Field(
        None, description="An alternative name for this item"
    )
    anionic_surfactants: Optional[float] = Field(
        None,
        alias="anionic-surfactants",
        description="Concentration of anionic surfactants",
        ge=0.0,
    )
    areaServed: Optional[str] = Field(
        None,
        description="The geographic area where a service or offered item is provided",
    )
    bod: Optional[float] = Field(
        None,
        description="Biochemical oxygen demand (BOD) is the amount of dissolved oxygen (DO) needed (i.e. demanded) by aerobic biological organisms to break down organic material present in a given water sample at certain temperature over a specific time period",
        ge=0.0,
    )
    cationic_surfactants: Optional[float] = Field(
        None,
        alias="cationic-surfactants",
        description="Concentration of cationic surfactants",
        ge=0.0,
    )
    cod: Optional[float] = Field(
        None,
        description="Chemical oxygen demand (COD) is an indicative measure of the amount of oxygen that can be consumed by reactions in a measured solution",
        ge=0.0,
    )
    conductance: Optional[float] = Field(
        None, description="Specific Conductance", ge=0.0
    )
    conductivity: Optional[float] = Field(
        None, description="Electrical Conductivity", ge=0.0
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
    dateObserved: Optional[str] = Field(
        None,
        description="The date and time of this observation in ISO8601 UTCformat. It can be represented by an specific time instant or by an ISO8601 interval",
    )
    description: Optional[str] = Field(None, description="A description of this item")
    enterococci: Optional[float] = Field(
        None, description="Concentration of Enterococci", ge=0.0
    )
    escherichiaColi: Optional[float] = Field(
        None, description="Concentration of Escherichia coli", ge=0.0
    )
    flow: Optional[float] = Field(None, description="Water Flow observed. ")
    fluoride: Optional[float] = Field(
        None, description="Concentration of fluoride", ge=0.0
    )
    id: Optional[Union[str, AnyUrl]] = Field(
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
    measurand: Optional[List[str]] = Field(
        None,
        description="An array of strings containing details (see format below) about extra measurands provided by this observation",
        min_length=1,
    )
    name: Optional[str] = Field(None, description="The name of this item")
    non_ionic_surfactants: Optional[float] = Field(
        None,
        alias="non-ionic-surfactants",
        description="Concentration of non-ionic surfactants",
        ge=0.0,
    )
    orp: Optional[float] = Field(
        None, description="Oxidation-Reduction potential", ge=0.0
    )
    owner: Optional[List[Union[str, AnyUrl]]] = Field(
        None,
        description="A List containing a JSON encoded sequence of characters referencing the unique Ids of the owner(s)",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!,:\\\\]+$",
        min_length=1,
        max_length=256,
    )
    pH: Optional[float] = Field(
        None, description="Acidity or basicity of an aqueous solution", ge=0.0, le=14.0
    )
    refPointOfInterest: Optional[Union[str, AnyUrl]] = Field(
        None,
        description="A reference to a point of interest associated to this observation",
        pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
        min_length=1,
        max_length=256,
    )
    salinity: Optional[float] = Field(
        None, description="Amount of salts dissolved in water", ge=0.0
    )
    seeAlso: Optional[Union[List[AnyUrl], AnyUrl]] = Field(
        None, description="list of uri pointing to additional resources about the item"
    )
    source: Optional[str] = Field(
        None,
        description="A sequence of characters giving the original source of the entity data as a URL. Recommended to be the fully qualified domain name of the source provider, or the URL to the source object",
    )
    sulphate: Optional[float] = Field(
        None, description="Concentration of sulfate", ge=0.0
    )
    sulphite: Optional[float] = Field(
        None, description="Concentration of sulfite", ge=0.0
    )
    tds: Optional[float] = Field(None, description="Total dissolved solids. ", ge=0.0)
    temperature: Optional[float] = Field(None, description="Temperature")
    total_surfactants: Optional[float] = Field(
        None,
        alias="total-surfactants",
        description="Concentration of total surfactants",
        ge=0.0,
    )
    tss: Optional[float] = Field(None, description="Total suspended solids", ge=0.0)
    turbidity: Optional[float] = Field(
        None,
        description="Amount of light scattered by particles in the water column",
        ge=0.0,
    )
    type: Optional[Type6] = Field(
        None, description="NGSI Entity type. It has to be WaterQualityObserved"
    )
