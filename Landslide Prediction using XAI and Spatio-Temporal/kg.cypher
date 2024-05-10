CREATE CONSTRAINT `Landslide_landslide_uniq` IF NOT EXISTS
FOR (n: `landslide`)
REQUIRE (n.`Landslide`) IS UNIQUE;
UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Landslide` IN $idsToSkip 
MERGE (n: `landslide` { `Landslide`: toLower(trim(nodeRecord.`Landslide`)) IN ['1','true','yes'] });




CREATE CONSTRAINT `Slope_slope_uniq` IF NOT EXISTS
FOR (n: `slope`)
REQUIRE (n.`Slope`) IS UNIQUE;



UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Slope` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Slope`)) IS NULL
MERGE (n: `slope` { `Slope`: toInteger(trim(nodeRecord.`Slope`)) });




CREATE CONSTRAINT `Aspect_aspect_uniq` IF NOT EXISTS
FOR (n: `aspect`)
REQUIRE (n.`Aspect`) IS UNIQUE;




UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Aspect` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Aspect`)) IS NULL
MERGE (n: `aspect` { `Aspect`: toInteger(trim(nodeRecord.`Aspect`)) });




CREATE CONSTRAINT `Curvature_curvature_uniq` IF NOT EXISTS
FOR (n: `curvature`)
REQUIRE (n.`Curvature`) IS UNIQUE;





UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Curvature` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Curvature`)) IS NULL
MERGE (n: `curvature` { `Curvature`: toInteger(trim(nodeRecord.`Curvature`)) });




CREATE CONSTRAINT `Earthquake_earthquake_uniq` IF NOT EXISTS
FOR (n: `earthquake`)
REQUIRE (n.`Earthquake`) IS UNIQUE;




UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Earthquake` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Earthquake`)) IS NULL
MERGE (n: `earthquake` { `Earthquake`: toInteger(trim(nodeRecord.`Earthquake`)) });




CREATE CONSTRAINT `Elevation_elevation_uniq` IF NOT EXISTS
FOR (n: `elevation`)
REQUIRE (n.`Elevation`) IS UNIQUE;




UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Elevation` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Elevation`)) IS NULL
MERGE (n: `elevation` { `Elevation`: toInteger(trim(nodeRecord.`Elevation`)) });




CREATE CONSTRAINT `Plan_plan_uniq` IF NOT EXISTS
FOR (n: `plan`)
REQUIRE (n.`Plan`) IS UNIQUE;




UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Plan` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Plan`)) IS NULL
MERGE (n: `plan` { `Plan`: toInteger(trim(nodeRecord.`Plan`)) });




CREATE CONSTRAINT `Profile_profile_uniq` IF NOT EXISTS
FOR (n: `profile`)
REQUIRE (n.`Profile`) IS UNIQUE;


CREATE CONSTRAINT `Landslide_landslide_uniq` IF NOT EXISTS
FOR (n: `landslide`)
REQUIRE (n.`Landslide`) IS UNIQUE;
UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Landslide` IN $idsToSkip 
MERGE (n: `landslide` { `Landslide`: toLower(trim(nodeRecord.`Landslide`)) IN ['1','true','yes'] });

CREATE CONSTRAINT `Slope_slope_uniq` IF NOT EXISTS
FOR (n: `slope`)
REQUIRE (n.`Slope`) IS UNIQUE;

UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Slope` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Slope`)) IS NULL
MERGE (n: `slope` { `Slope`: toInteger(trim(nodeRecord.`Slope`)) });

CREATE CONSTRAINT `Aspect_aspect_uniq` IF NOT EXISTS
FOR (n: `aspect`)
REQUIRE (n.`Aspect`) IS UNIQUE;

UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Aspect` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Aspect`)) IS NULL
MERGE (n: `aspect` { `Aspect`: toInteger(trim(nodeRecord.`Aspect`)) });




CREATE CONSTRAINT `Curvature_curvature_uniq` IF NOT EXISTS
FOR (n: `curvature`)
REQUIRE (n.`Curvature`) IS UNIQUE;

UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Curvature` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Curvature`)) IS NULL
MERGE (n: `curvature` { `Curvature`: toInteger(trim(nodeRecord.`Curvature`)) });




CREATE CONSTRAINT `Earthquake_earthquake_uniq` IF NOT EXISTS
FOR (n: `earthquake`)
REQUIRE (n.`Earthquake`) IS UNIQUE;




UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Earthquake` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Earthquake`)) IS NULL
MERGE (n: `earthquake` { `Earthquake`: toInteger(trim(nodeRecord.`Earthquake`)) });

CREATE CONSTRAINT `Elevation_elevation_uniq` IF NOT EXISTS
FOR (n: `elevation`)
REQUIRE (n.`Elevation`) IS UNIQUE;




UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Elevation` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Elevation`)) IS NULL
MERGE (n: `elevation` { `Elevation`: toInteger(trim(nodeRecord.`Elevation`)) });




CREATE CONSTRAINT `Plan_plan_uniq` IF NOT EXISTS
FOR (n: `plan`)
REQUIRE (n.`Plan`) IS UNIQUE;




UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Plan` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Plan`)) IS NULL
MERGE (n: `plan` { `Plan`: toInteger(trim(nodeRecord.`Plan`)) });




CREATE CONSTRAINT `Profile_profile_uniq` IF NOT EXISTS
FOR (n: `profile`)
REQUIRE (n.`Profile`) IS UNIQUE;




UNWIND $nodeRecords AS nodeRecord
WITH *
WHERE NOT nodeRecord.`Profile` IN $idsToSkip AND NOT toInteger(trim(nodeRecord.`Profile`)) 