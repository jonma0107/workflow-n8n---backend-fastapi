from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Libro

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Biblioteca",
    description="API para gestionar libros desde N8N",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas Pydantic
class LibroCreate(BaseModel):
    titulo: str
    autor: str
    isbn: Optional[str] = None
    editorial: Optional[str] = None
    año_publicacion: Optional[int] = None
    genero: Optional[str] = None
    descripcion: Optional[str] = None

class LibroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    isbn: Optional[str]
    editorial: Optional[str]
    año_publicacion: Optional[int]
    genero: Optional[str]
    descripcion: Optional[str]

    class Config:
        from_attributes = True

# Rutas
@app.get("/")
def read_root():
    return {
        "message": "API Biblioteca - N8N Integration",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/libros", response_model=LibroResponse)
def crear_o_actualizar_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo libro o actualizar si ya existe (UPSERT)
    
    Si el ISBN existe: actualiza el libro existente
    Si el ISBN no existe o está vacío: crea uno nuevo
    
    Esto permite ejecutar el workflow múltiples veces sin errores.
    """
    try:
        existing_libro = None
        
        # Verificar si ya existe un libro con el mismo ISBN (si se proporciona)
        if libro.isbn and libro.isbn.strip():  # Solo si ISBN no está vacío
            try:
                existing_libro = db.query(Libro).filter(Libro.isbn == libro.isbn).first()
            except Exception as e:
                # Si falla la consulta, intentar reconectar
                db.rollback()
                db.close()
                existing_libro = db.query(Libro).filter(Libro.isbn == libro.isbn).first()
        
        if existing_libro:
            # ACTUALIZAR libro existente
            for key, value in libro.dict(exclude_unset=True).items():
                setattr(existing_libro, key, value)
            
            db.commit()
            db.refresh(existing_libro)
            
            return existing_libro
        else:
            # CREAR nuevo libro
            db_libro = Libro(**libro.dict())
            db.add(db_libro)
            db.commit()
            db.refresh(db_libro)
            
            return db_libro
            
    except Exception as e:
        db.rollback()
        # Mensaje de error más amigable
        error_msg = str(e)
        if "SSL" in error_msg or "connection" in error_msg.lower():
            raise HTTPException(
                status_code=503, 
                detail="Error de conexión con la base de datos. Por favor, intenta nuevamente."
            )
        raise HTTPException(status_code=500, detail=f"Error al procesar el libro: {error_msg}")

@app.post("/api/libros/strict", response_model=LibroResponse, status_code=201)
def crear_libro_strict(libro: LibroCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo libro (modo strict - falla si ya existe)
    
    Este endpoint rechaza ISBN duplicados.
    Úsalo cuando quieras asegurar que no hay duplicados.
    """
    try:
        # Verificar si ya existe un libro con el mismo ISBN
        if libro.isbn and libro.isbn.strip():
            existing_libro = db.query(Libro).filter(Libro.isbn == libro.isbn).first()
            if existing_libro:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Ya existe un libro con el ISBN: {libro.isbn}"
                )
        
        # Crear el nuevo libro
        db_libro = Libro(**libro.dict())
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
        
        return db_libro
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el libro: {str(e)}")

@app.get("/api/libros", response_model=List[LibroResponse])
def listar_libros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener todos los libros
    """
    libros = db.query(Libro).offset(skip).limit(limit).all()
    return libros

@app.get("/api/libros/{libro_id}", response_model=LibroResponse)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    """
    Obtener un libro por ID
    """
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.delete("/api/libros/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un libro por ID
    """
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    db.delete(libro)
    db.commit()
    return {"message": f"Libro '{libro.titulo}' eliminado correctamente"}

@app.put("/api/libros/{libro_id}", response_model=LibroResponse)
def actualizar_libro(libro_id: int, libro: LibroCreate, db: Session = Depends(get_db)):
    """
    Actualizar un libro existente
    """
    db_libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if db_libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    for key, value in libro.dict(exclude_unset=True).items():
        setattr(db_libro, key, value)
    
    db.commit()
    db.refresh(db_libro)
    return db_libro

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

