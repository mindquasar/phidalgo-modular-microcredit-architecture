# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a PostgreSQL: reemplaza USER, PASSWORD, HOST, PORT y DBNAME con los valores reales
DATABASE_URL = "postgresql://postgres:lvame8d@localhost:5432/microcredit"

# Crea el motor de SQLAlchemy, que maneja la conexión con la base de datos
engine = create_engine(DATABASE_URL)

# Crea una clase base a partir de la cual se definirán los modelos de la base de datos
Base = declarative_base()

# Crea una fábrica de sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función auxiliar para obtener una sesión de base de datos en cada solicitud
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
