#!/bin/bash

## This script will read the JSON file, connect to ratecard database, remove existing table, create fields, and update the field with 
## JSON data.

myfile="/tmp/RateCardSmall.json"
export PGPASSWORD=dbadmin

psql -h localhost -U dbadmin -d ratecarddb <<EOF
DROP TABLE AzureRateCardTable;
CREATE TABLE AzureRateCardTable (id SERIAL PRIMARY KEY, region VARCHAR(20) NOT NULL, ratecard JSON NOT NULL);
\\set var \`cat $myfile\`
\\set
INSERT INTO AzureRateCardTable (region, ratecard) VALUES ('AzureRegionUK', :'var');

EOF

