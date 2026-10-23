from pathlib import Path
import pandas as pd
import urllib
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

#__file__ is experimented/phase-0/ ingest_legacy_data.py
script_dir = Path(__file__).resolve().parent # points to experiment/phas-0
project_root = script_dir.parents[0] #climbs up 1 levels to project root

load_dotenv(project_root / ".env", override=True) # load the .env file from the project root

data_path = project_root / "data" / "raw" / "dynamic_supply_chain_logistics_dataset.csv"

db_host = os.getenv("SQL_SERVER_HOST", "localhost") 
# if the host is not present we wil look into local host
db_port = os.getenv("SQL_SERVER_PORT", "1433")
db_user = os.getenv("SQL_ADMIN_USER")
db_password = os.getenv("SQL_ADMIN_PASSWORD")

print("DB Host:", repr(db_host))
print("DB Port:", repr(db_port))
print("DB User:", repr(db_user))
print("Password loaded:", bool(db_password))

# 1. load the raw dataset from CSV file
df = pd.read_csv(data_path)

#2. mapping clean columns to a messy 2000s legacy enterprise schema
legacy_mapping = {
    'timestamp': 'TS_UTC',
    'vehicle_gps_latitude': 'V_LAT',
    'vehicle_gps_longitude': 'V_LON',
    'iot_temperature': 'IOT_TEMP_VAL_C',
    'cargo_condition_status': 'CGO_COND_CD',
    'risk_classification': 'RISK_CLS_TXT',
    'delay_probability': 'DELAY_PROB_DEC',
    'port_congestion_level': 'PRT_CNG_LVL',
    'route_risk_level': 'RT_RSK_IDX'
}

# note** we have created weird column names just to show how the legacy system might have designed.
# note** u can find the actual column names in the dataset

#3. Keep only the columns we mapped for this demo and rename them
df_legacy = df[list(legacy_mapping.keys())].rename(columns=legacy_mapping)

#4. Add a fake ingestion flag to make it look like an automated legacy system
df_legacy['SYS_INGEST_FLAG'] = 'Y'
# it tells that these are the columns that have been ingested

#5. Connect to the Docker MSSQL Server
print("Connecting to legacy MSSQL Database...")

# Use the pyodbc driver. (Ensure you have ODBC Driver 17 or 18 for SQL Server installed on your OS)
# Build the connection string using the same settings that worked
# in our direct pyodbc connection test.
conection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={db_host},{db_port};"
    f"DATABASE=master;"
    f"UID={db_user};"
    f"PWD={db_password};"
    f"Encrypt=no;"
    f"TrustServerCertificate=yes;"
    "Connection Timeout=5;"
)

# parsing the connection string
params = urllib.parse.quote_plus(conection_string)

# passing it to the sqlalchemy engine
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

#6. Ingest data into the messy table name
table_name = "TBL_SC_FLEET_HIST_RAW"
print(f"Ingesting data into {table_name}. This may take a minute...")
df_legacy.to_sql(table_name, engine, if_exists='replace', index=False, schema='dbo')

print("✅ Legacy data ingestion complete!")