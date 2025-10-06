from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    autor = Column(String(255), nullable=False)
    isbn = Column(String(50), unique=True, nullable=True)
    editorial = Column(String(255), nullable=True)
    año_publicacion = Column(Integer, nullable=True)
    genero = Column(String(100), nullable=True)
    descripcion = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Libro(titulo='{self.titulo}', autor='{self.autor}')>"

