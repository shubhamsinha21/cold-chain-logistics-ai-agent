# Ingesting data

- Download the dataset from 'data\source\data.txt'
- Create an EC2 instance > docker container > mcr.microsoft.com/mssql/server:2022-latest
- Spin up the Legacy SQL Server


```
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=FdeEnterprisePass123!" -p 1433:1433 --name legacy-mssql -d mcr.microsoft.com/mssql/server:2022-latest
```

# or multi-line with volume inside EC2
```
docker run -v mssql_data:/var/opt/mssql \
-e "ACCEPT_EULA=Y" \
-e "MSSQL_SA_PASSWORD=FdeEnterprisePass123!" \
-p 1433:1433 \
--name legacy-mssql \
-d mcr.microsoft.com/mssql/server:2022-latest
```

- After this, we will install the requirements.
```
python -m pip install -r requirements.txt
```

- python scripts/ingest_legacy_data.py

- connecting to the data

We need to query the database

Azure studio - https://github.com/microsoft/azuredatastudio

https://learn.microsoft.com/en-us/previous-versions/azure-data-studio/download-azure-data-studio?tabs=win-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall

- It is recommended to use Vs Code "MSSQL" extension by microsoft.

The recommendation is to use VS code extension : "SQL Server (mssql)" by microsoft

Click on icon that looks like server or refrigarator, not the one with cylinder
Add connection
Fill the below :

```
Profile Name: legacy-mssql
Server name*: localhost
Port: 1433
Trust server certificate: 🟩 Check this box / turn it ON (Crucial for Docker)
Authentication type*: SQL Login
User name*: sa
Password*: FdeEnterprisePass123!
Save Password: 🟩 Check this box
Database name: Type master (or leave it on "Select a database")
Encrypt: ⚠️ Change this from Mandatory to Optional (or False)
```
***
In order to run a sequel query here, create a new temp file in the memory.

CTRL+N
Plain text -> SQL
Command to test -> 
```
SELECT COUNT(*) AS total_rows FROM dbo.TBL_SC_FLEET_HIST_RAW;
```

# instruction for Ec2 instance > datbase

- Instance type : c7i-flex.large
- storage : 30 gb
- mac os
- Security group > attach the security while creating ec2 instance
- Launch instance
- SSH using .pem file from your system
- install the docker

```
docker run -v mssql_data:/var/opt/mssql \
  -e "ACCEPT_EULA=Y" \
  -e "MSSQL_SA_PASSWORD=FdeEnterprisePass123!" \
  -p 1433:1433 \
  --name legacy-mssql \
  -d mcr.microsoft.com/mssql/server:2022-latest
```