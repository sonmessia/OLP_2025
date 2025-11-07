from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import (
    AnyUrl,
    AwareDatetime,
    BaseModel,
    Field,
    RootModel,
    confloat,
    constr,
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
    CarbonFootPrint = "CarbonFootPrint"


class CarbonFootPrint(BaseModel):
    Al: Optional[confloat(ge=0.0)] = Field(
        None, description="Aluminium. Concentration of aluminium"
    )
    As: Optional[confloat(ge=0.0)] = Field(
        None, description="Arsenic. Concentration of arsenic"
    )
    B: Optional[confloat(ge=0.0)] = Field(
        None, description="Boron. Concentration of boron"
    )
    Ba: Optional[confloat(ge=0.0)] = Field(
        None, description="Barium. Concentration of barium"
    )
    Cd: Optional[confloat(ge=0.0)] = Field(
        None, description="Cadmium. Concentration of cadmium"
    )
    Chla: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of chlorophyll A"
    )
    Cl_: Optional[confloat(ge=0.0)] = Field(
        None, alias="Cl-", description="Concentration of chlorides"
    )
    Cr: Optional[confloat(ge=0.0)] = Field(
        None, description="Chromium. Concentration of chromium"
    )
    Cr_III: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="Cr-III",
        description="Chromium III. Concentration of chromium at the oxidation state +3",
    )
    Cr_VI: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="Cr-VI",
        description="Chromium VI. Concentration of chromium at the oxidation state +6",
    )
    Cu: Optional[confloat(ge=0.0)] = Field(
        None, description="Copper. Concentration of copper"
    )
    Fe: Optional[confloat(ge=0.0)] = Field(
        None, description="Iron. Concentration of iron"
    )
    Hg: Optional[confloat(ge=0.0)] = Field(
        None, description="Mercury. Concentration of mercury"
    )
    N_TOT: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="N-TOT",
        description="Total Nitrogen. Total Nitrogen (TN) is the sum of nitrate-nitrogen (NO3-N), nitrite-nitrogen (NO2-N), ammonia-nitrogen (NH3-N) and organically bonded nitrogen",
    )
    NH3: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of ammonia"
    )
    NH4: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of ammonium"
    )
    NO2: Optional[confloat(ge=0.0)] = Field(
        None,
        description="Nitrite nitrogen. Concentration of a sample in nitrite nitrogen",
    )
    NO3: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of nitrates"
    )
    Ni: Optional[confloat(ge=0.0)] = Field(
        None, description="Nickel. Concentration of Nickel"
    )
    O2: Optional[confloat(ge=0.0)] = Field(
        None, description="Level of free, non-compound oxygen present"
    )
    P_PO4: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="P-PO4",
        description="Phosphate-phosphorus. Concentration of phosphorus as phosphate",
    )
    P_TOT: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="P-TOT",
        description="Total Phosphorus. Total phosphorus is a measure of all forms of\\xa0phosphorus\\xa0in the water, including dissolved and particulate, organic and inorganic",
    )
    PC: Optional[confloat(ge=0.0)] = Field(
        None,
        description="Concentration of pigment phycocyanin which can be measured to estimate cyanobacteria concentrations specifically",
    )
    PE: Optional[confloat(ge=0.0)] = Field(
        None,
        description="Concentration of pigment phycoerythrin which can be measured to estimate cyanobacteria concentrations specifically",
    )
    PO4: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of phosphates"
    )
    Pb: Optional[confloat(ge=0.0)] = Field(
        None, description="Lead. Concentration of lead"
    )
    Se: Optional[confloat(ge=0.0)] = Field(
        None, description="Selenium. Concentration of selenium"
    )
    Sn: Optional[confloat(ge=0.0)] = Field(
        None, description="Tin. Concentration of tin"
    )
    THC: Optional[confloat(ge=0.0)] = Field(
        None, description="Total hydrocarbon. Concentration of total hydrocarbon"
    )
    TKN: Optional[confloat(ge=0.0)] = Field(
        None,
        description="Total Kjeldahl Nitrogen. A measure that determines both the organic and the inorganic forms of nitrogen",
    )
    TO: Optional[confloat(ge=0.0)] = Field(
        None, description="Total oil content. Concentration of oil"
    )
    Zn: Optional[confloat(ge=0.0)] = Field(
        None, description="Zinc. Concentration of zinc"
    )
    address: Optional[Address] = Field(None, description="The mailing address")
    alkalinity: Optional[confloat(ge=0.0)] = Field(
        None,
        description="The alkalinity of water is its acid-neutralizing capacity comprised of the total of all titratable bases",
    )
    alternateName: Optional[str] = Field(
        None, description="An alternative name for this item"
    )
    anionic_surfactants: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="anionic-surfactants",
        description="Concentration of anionic surfactants",
    )
    areaServed: Optional[str] = Field(
        None,
        description="The geographic area where a service or offered item is provided",
    )
    bod: Optional[confloat(ge=0.0)] = Field(
        None,
        description="Biochemical oxygen demand (BOD) is the amount of dissolved oxygen (DO) needed (i.e. demanded) by aerobic biological organisms to break down organic material present in a given water sample at certain temperature over a specific time period",
    )
    cationic_surfactants: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="cationic-surfactants",
        description="Concentrtation of cationic surfactants",
    )
    cod: Optional[confloat(ge=0.0)] = Field(
        None,
        description="Chemical oxygen demand (COD) is an indicative measure of the amount of oxygen that can be consumed by reactions in a measured solution",
    )
    conductance: Optional[confloat(ge=0.0)] = Field(
        None, description="Specific Conductance"
    )
    conductivity: Optional[confloat(ge=0.0)] = Field(
        None, description="Electrical Conductivity"
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
    enterococci: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of Enterococci"
    )
    escherichiaColi: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of Escherichia coli"
    )
    flow: Optional[float] = Field(None, description="Water Flow observed.")
    fluoride: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of fluoride"
    )
    id: Optional[
        Union[
            constr(
                pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
                min_length=1,
                max_length=256,
            ),
            AnyUrl,
        ]
    ] = Field(None, description="Unique identifier of the entity")
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
    non_ionic_surfactants: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="non-ionic-surfactants",
        description="Concentration of non-ionic surfactants",
    )
    orp: Optional[confloat(ge=0.0)] = Field(
        None, description="Oxidation-Reduction potential"
    )
    owner: Optional[
        List[
            Union[
                constr(
                    pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!,:\\\\]+$",
                    min_length=1,
                    max_length=256,
                ),
                AnyUrl,
            ]
        ]
    ] = Field(
        None,
        description="A List containing a JSON encoded sequence of characters referencing the unique Ids of the owner(s)",
    )
    pH: Optional[confloat(ge=0.0, le=14.0)] = Field(
        None, description="Acidity or basicity of an aqueous solution"
    )
    refPointOfInterest: Optional[
        Union[
            constr(
                pattern=r"^[\\w\\-\\.\\{\\}\\$\\+\\*\\[\\]`|~^@!, :\\\\]+$",
                min_length=1,
                max_length=256,
            ),
            AnyUrl,
        ]
    ] = Field(
        None,
        description="A reference to a point of interest associated to this observation",
    )
    salinity: Optional[confloat(ge=0.0)] = Field(
        None, description="Amount of salts dissolved in water"
    )
    seeAlso: Optional[Union[List[AnyUrl], AnyUrl]] = Field(
        None, description="list of uri pointing to additional resources about the item"
    )
    source: Optional[str] = Field(
        None,
        description="A sequence of characters giving the original source of the entity data as a URL. Recommended to be the fully qualified domain name of the source provider, or the URL to the source object",
    )
    sulphate: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of sulfate"
    )
    sulphite: Optional[confloat(ge=0.0)] = Field(
        None, description="Concentration of sulfite"
    )
    tds: Optional[confloat(ge=0.0)] = Field(
        None, description="Total dissolved solids. "
    )
    temperature: Optional[float] = Field(None, description="Temperature")
    total_surfactants: Optional[confloat(ge=0.0)] = Field(
        None,
        alias="total-surfactants",
        description="Concentration of total surfactants",
    )
    tss: Optional[confloat(ge=0.0)] = Field(None, description="Total suspended solids")
    turbidity: Optional[confloat(ge=0.0)] = Field(
        None, description="Amount of light scattered by particles in the water column"
    )
    type: Optional[Type6] = Field(
        None, description="NGSI Entity type. It has to be CarbonFootPrint"
    )
