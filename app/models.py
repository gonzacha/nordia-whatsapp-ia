from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DB_PATH

Base = declarative_base()

class Comercio(Base):
    __tablename__ = "comercios"

    id = Column(Integer, primary_key=True)
    telefono_dueno = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    horarios = Column(Text)
    servicios = Column(Text)

class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True)
    comercio_id = Column(Integer, ForeignKey("comercios.id"))
    cliente_nombre = Column(String)
    cliente_telefono = Column(String)
    fecha = Column(String)
    hora = Column(String)
    servicio = Column(String)

class Conversacion(Base):
    __tablename__ = "conversaciones"

    id = Column(Integer, primary_key=True)
    telefono_cliente = Column(String)
    comercio_id = Column(Integer, ForeignKey("comercios.id"))
    estado = Column(String)

engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
