--------------------------------------------------------------
-- ĐẢM BẢO TẤT CẢ ENUM ĐƯỢC TẠO TRƯỚC KHI SỬ DỤNG
--------------------------------------------------------------

-- ENUMs cho Device
CREATE TYPE direction_type AS ENUM ('Inlet', 'Outlet', 'Entry', 'Exit');
CREATE TYPE device_type AS ENUM ('Device');

-- ENUMs cho AirQualityObserved
CREATE TYPE airqualityobserved_type AS ENUM ('AirQualityObserved');
CREATE TYPE typeoflocation_type AS ENUM ('indoor', 'outdoor');

-- ENUMs cho WaterQualityObserved
CREATE TYPE waterqualityobserved_type AS ENUM ('WaterQualityObserved');


--------------------------------------------------------------
-- BẢNG 1: CarbonFootprint
--------------------------------------------------------------
CREATE TABLE CarbonFootprint (
    id TEXT PRIMARY KEY,
    CO2eq NUMERIC,
    address JSON,
    alternateName TEXT,
    areaServed TEXT,
    dataProvider TEXT,
    dateCreated TIMESTAMP,
    dateModified TIMESTAMP,
    description TEXT,
    emissionDate TIMESTAMP,
    emissionSource TEXT,
    location JSON,
    name TEXT,
    owner JSON,
    relatedSource TEXT,
    seeAlso JSON,
    source TEXT,
    tags JSON,
    type TEXT
);

-- Add indexes to improve query performance on CarbonFootprint
CREATE INDEX idx_carbonfootprint_emission_date ON CarbonFootprint(emissionDate);
CREATE INDEX idx_carbonfootprint_date_created ON CarbonFootprint(dateCreated);
CREATE INDEX idx_carbonfootprint_related_source ON CarbonFootprint(relatedSource);
--------------------------------------------------------------
-- BẢNG 2: AirQualityObserved
--------------------------------------------------------------
CREATE TABLE AirQualityObserved (
    id TEXT PRIMARY KEY,
    address JSON,
    airQualityIndex NUMERIC,
    airQualityLevel TEXT,
    alternateName TEXT,
    areaServed TEXT,
    "as" NUMERIC,
    c6h6 NUMERIC,
    cd NUMERIC,
    charge NUMERIC,
    co NUMERIC,
    co2 NUMERIC,
    coLevel TEXT,
    dataProvider TEXT,
    dateCreated TIMESTAMP,
    dateModified TIMESTAMP,
    dateObserved TIMESTAMP,
    description TEXT,
    location JSON,
    name TEXT,
    ni NUMERIC,
    no NUMERIC,
    no2 NUMERIC,
    nox NUMERIC,
    o3 NUMERIC,
    owner JSON,
    pb NUMERIC,
    pm1 NUMERIC,
    pm10 NUMERIC,
    pm25 NUMERIC,
    pm4 NUMERIC,
    precipitation NUMERIC,
    pressure NUMERIC,
    relativeHumidity NUMERIC,
    reliability NUMERIC,
    seeAlso JSON,
    sh2 NUMERIC,
    so2 NUMERIC,
    source TEXT,
    temperature NUMERIC,
    tpc NUMERIC,
    tsp NUMERIC,
    type airqualityobserved_type,
    typeofLocation typeoflocation_type,
    volatileOrganicCompoundsTotal NUMERIC,
    windDirection NUMERIC,
    windSpeed NUMERIC
);


--------------------------------------------------------------
-- BẢNG 3: WaterQualityObserved
--------------------------------------------------------------
CREATE TABLE WaterQualityObserved (
    id TEXT PRIMARY KEY,
    "Al" NUMERIC, "As" NUMERIC, "B" NUMERIC, "Ba" NUMERIC, "Cd" NUMERIC,
    "Chla" NUMERIC, "Cl_" NUMERIC, "Cr" NUMERIC, "Cr_III" NUMERIC, "Cr_VI" NUMERIC,
    "Cu" NUMERIC, "Fe" NUMERIC, "Hg" NUMERIC, "N_TOT" NUMERIC, "NH3" NUMERIC,
    "NH4" NUMERIC, "NO2" NUMERIC, "NO3" NUMERIC, "Ni" NUMERIC, "O2" NUMERIC,
    "P_PO4" NUMERIC, "P_TOT" NUMERIC, "PC" NUMERIC, "PE" NUMERIC, "PO4" NUMERIC,
    "Pb" NUMERIC, "Se" NUMERIC, "Sn" NUMERIC, "THC" NUMERIC, "TKN" NUMERIC,
    "TO" NUMERIC, "Zn" NUMERIC,

    address JSON,
    alkalinity NUMERIC,
    alternateName TEXT,
    "anionic_surfactants" NUMERIC,
    areaServed TEXT,
    bod NUMERIC,
    "cationic_surfactants" NUMERIC,
    cod NUMERIC,
    componentAnalyzed TEXT,
    componentName TEXT,
    concentration NUMERIC,
    conductance NUMERIC,
    conductivity NUMERIC,
    dataProvider TEXT,
    dateCreated TIMESTAMP,
    dateModified TIMESTAMP,
    dateObserved TIMESTAMP,
    description TEXT,
    enterococci NUMERIC,
    escherichiaColi NUMERIC,
    flow NUMERIC,
    fluoride NUMERIC,
    location JSON,
    measurand JSON,
    name TEXT,
    "non_ionic_surfactants" NUMERIC,
    orp NUMERIC,
    owner JSON,
    "pH" NUMERIC,
    salinity NUMERIC,
    seeAlso JSON,
    source TEXT,
    sulphate NUMERIC,
    sulphite NUMERIC,
    tds NUMERIC,
    temperature NUMERIC,
    "total_surfactants" NUMERIC,
    tss NUMERIC,
    turbidity NUMERIC,
    type waterqualityobserved_type
);


--------------------------------------------------------------
-- BẢNG 4: Device
--------------------------------------------------------------
CREATE TABLE Device (
    id TEXT PRIMARY KEY,
    address JSON,
    alternateName TEXT,
    areaServed TEXT,
    batteryLevel JSON,
    category JSON,
    configuration JSON,
    controlledAsset JSON,
    controlledProperty JSON,
    dataProvider TEXT,
    dateCreated TIMESTAMP,
    dateFirstUsed TIMESTAMP,
    dateInstalled TIMESTAMP,
    dateLastCalibration TIMESTAMP,
    dateLastValueReported TIMESTAMP,
    dateManufactured TIMESTAMP,
    dateModified TIMESTAMP,
    dateObserved TIMESTAMP,
    depth NUMERIC,
    description TEXT,
    deviceCategory JSON,
    deviceState TEXT,
    direction direction_type,
    distance NUMERIC,
    dstAware BOOLEAN,
    firmwareVersion TEXT,
    hardwareVersion TEXT,
    ipAddress JSON,
    location JSON,
    macAddress TEXT,
    mcc TEXT,
    mnc TEXT,
    name TEXT,
    osVersion TEXT,
    owner JSON,
    provider TEXT,
    relativePosition TEXT,
    rssi NUMERIC,
    seeAlso JSON,
    serialNumber TEXT,
    softwareVersion TEXT,
    source TEXT,
    supportedProtocol JSON,
    type device_type,
    value TEXT
);

