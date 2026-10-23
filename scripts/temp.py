
import os
import pyodbc
from dotenv import load_dotenv
from pathlib import Path

# Locate and load the project-root .env file
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / ".env"

print("ENV file exists:", env_path.exists())
print("ENV path:", env_path)

if not env_path.exists():
    raise FileNotFoundError(f".env file not found at: {env_path}")

load_dotenv(env_path, override=True)

# Read database configuration
host = os.getenv("SQL_SERVER_HOST") or "127.0.0.1"
port = os.getenv("SQL_SERVER_PORT") or "1433"
user = os.getenv("SQL_ADMIN_USER")
password = os.getenv("SQL_ADMIN_PASSWORD")

# Print safe diagnostics (never print the password)
print("Host:", repr(host))
print("Port:", repr(port))
print("Username:", repr(user))
print("Password loaded:", bool(password))
print("Available drivers:", pyodbc.drivers())

if not user or not password:
    raise ValueError(
        "Database credentials are missing. "
        "Check SQL_ADMIN_USER and SQL_ADMIN_PASSWORD in .env."
    )

if "ODBC Driver 18 for SQL Server" not in pyodbc.drivers():
    raise RuntimeError("ODBC Driver 18 for SQL Server is not available.")

# Build the connection string
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER=tcp:127.0.0.1,{port};"
    "DATABASE=master;"
    f"UID={user};"
    f"PWD={{{password}}};"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=5;"
)

# Test the connection
try:
    print("Testing SQL Server connection...")

    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION, SYSTEM_USER, DB_NAME()")
        result = cursor.fetchone()

        print("CONNECTION SUCCESSFUL!")
        print("SQL Server version:", result[0])
        print("Login:", result[1])
        print("Database:", result[2])

except pyodbc.Error as e:
    print("CONNECTION FAILED")
    print("Error:", repr(e))
