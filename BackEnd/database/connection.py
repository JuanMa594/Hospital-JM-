from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# 1. Prioridad: Cadena de conexión completa (ideal para PostgreSQL en Render o SQL Server en la nube)
database_url = os.getenv("DATABASE_URL")

if database_url:
    # SQLAlchemy requiere que empiece por postgresql:// no postgres://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    connection_string = database_url
# 2. Conexión SQL Server con usuario y contraseña (ej. Azure SQL Database)
elif DB_SERVER and DB_NAME and DB_USER and DB_PASSWORD:
    # Usamos ODBC Driver 18 porque es el que instalamos en el Dockerfile
    odbc_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no"
    connection_string = "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_str)
# 3. Conexión SQL Server local con Windows Authentication (como lo tenías antes)
else:
    odbc_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};Trusted_Connection=yes"
    connection_string = "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_str)

# Configuración de SSL para PostgreSQL (Supabase requiere SSL)
connect_args = {}
if connection_string.startswith("postgresql"):
    connect_args = {"sslmode": "require"}

engine = create_engine(connection_string, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
