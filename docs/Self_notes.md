```
docker run -e ACCEPT_EULA=Y -e 'MSSQL_SA_PASSWORD=FdeEnterprisePass123!' -p 1433:1433 --name legacy-mssql -d mcr.microsoft.com/mssql/server:2022-latest
```

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
