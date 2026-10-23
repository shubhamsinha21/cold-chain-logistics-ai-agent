```
docker run -e ACCEPT_EULA=Y -e 'MSSQL_SA_PASSWORD=FdeEnterprisePass123!' -p 1433:1433 --name legacy-mssql -d mcr.microsoft.com/mssql/server:2022-latest
```

** Here SA = USERNAME **

- when i used this command i got this:
""
Unable to find image locally: Docker didn’t find the SQL Server image on your computer.

Pulling from mssql/server: Docker is downloading the image from Microsoft’s container registry.

Downloading 269.5MB/502.1MB: The download is in progress.
""

- Why did this happen? 

This is the first time you’re pulling this image, so Docker needs to download it before starting the container.

- After the download, i got this:

```
Status: Downloaded newer image for mcr.microsoft.com/mssql/server:2022-latest
WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested
3474806d2220c6364796fe5143e852a71ddb45056bec76050827ef0cb582c425
```

- What if we have added the .env file into .gitignore
- still it shows in git repo
- we would use this commands:

```
git rm --cached .env    
git add .
git commit ....
```

- Lots of errors while doing ingestion
1. In .env, we had spaces bet "=" and key and values
2. ODBC Driver 18 for SQL server was not installed.

```
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew trust microsoft/mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18
```

- verify

```
odbcinst -q -d
```

3. Then we have the dependency "unixODBC" missing.

```
brew install unixodbc
```

4. unixODBC driver configuration read nahi kar paa raha tha. 

5. msodbcsql18 normal Homebrew formula mein available nahi hai. Microsoft ke official instructions kiye

- Add microsoft's repository

```
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
```

- Trust the repo
```
brew trust microsoft/mssql-release
```

- Install the driver

```
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18
```

6. Finally, SQL_SERVER_HOST ko localhost -> 127.0.0.1 se change kiye

*** 
Final result:

```
python scripts/ingest_legacy_data.py
DB Host: '127.0.0.1'
DB Port: '1433'
DB User: 'sa'
Password loaded: True
Connecting to legacy MSSQL Database...
Ingesting data into TBL_SC_FLEET_HIST_RAW. This may take a minute...
✅ Legacy data ingestion complete!
```