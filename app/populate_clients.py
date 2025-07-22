# populate_clients.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from database import Base, engine, SessionLocal
from faker import Faker
import random
import sys

# ------------------------
# Modelo de la tabla 'clients'
# ------------------------
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String(8), unique=True, index=True, nullable=False)  # DNI con 8 dígitos
    name = Column(String, nullable=False)  # Nombre completo

# ------------------------
# Inicializa Faker con localización en español
# ------------------------
faker = Faker("es_ES")

# ------------------------
# Generador de DNIs únicos con formato 0XXXXXXX
# ------------------------
def generate_dni():
    return "0" + "".join([str(random.randint(0, 9)) for _ in range(7)])

# ------------------------
# Función para poblar la tabla con datos sintéticos
# ------------------------
def populate_clients(n=1000):
    try:
        # Intenta abrir una sesión con la base de datos
        db = SessionLocal()
    except OperationalError as e:
        print("❌ Error al conectar con la base de datos:", e)
        sys.exit(1)

    try:
        # Crea la tabla 'clients' si no existe
        Base.metadata.create_all(bind=engine)

        existing_dnis = set()
        for _ in range(n):
            dni = generate_dni()

            # Asegura que el DNI sea único dentro del batch
            while dni in existing_dnis:
                dni = generate_dni()
            existing_dnis.add(dni)

            # Genera un nombre completo en español
            name = f"{faker.first_name()} {faker.last_name()}"

            # Crea una instancia del modelo
            client = Client(dni=dni, name=name)

            # Agrega a la sesión
            db.add(client)

        # Confirma la transacción
        db.commit()
        print(f"✅ Insertados {n} clientes correctamente.")
    
    except SQLAlchemyError as e:
        # En caso de error, deshace la transacción
        db.rollback()
        print("❌ Error al insertar registros:", e)
    
    finally:
        # Siempre cierra la sesión
        db.close()

# ------------------------
# Punto de entrada del script
# ------------------------
if __name__ == "__main__":
    populate_clients()
