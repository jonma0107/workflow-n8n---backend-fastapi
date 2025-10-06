# API Biblioteca - Backend FastAPI

Backend para gestionar una biblioteca de libros usando FastAPI y PostgreSQL (Neon.tech).

## 🚀 Características

- API RESTful completa para gestión de libros
- Integración con PostgreSQL en Neon.tech
- Dockerizado para fácil despliegue
- Compatible con N8N para automatizaciones
- Validación de datos con Pydantic

## 📋 Requisitos

- Docker y Docker Compose
- Cuenta en Neon.tech con base de datos creada
- Python 3.11+ (para desarrollo local)

## 🛠️ Instalación

### Usando Docker (Recomendado)

1. Crear el archivo `.env` en la carpeta `backend/`.

2. Desde el directorio raíz del proyecto, ejecutar:
```bash
docker-compose up -d
```

3. La API estará disponible en: `http://localhost:8000`

### Desarrollo Local

1. Crear entorno virtual:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Crear archivo `.env` con las credenciales de la base de datos

4. Ejecutar la aplicación:
```bash
uvicorn main:app --reload
```

## 📚 Endpoints

### Health Check
- `GET /` - Información general de la API
- `GET /health` - Estado de salud de la API

### Libros
- `POST /api/libros` - Crear un nuevo libro
- `GET /api/libros` - Listar todos los libros
- `GET /api/libros/{id}` - Obtener un libro específico
- `PUT /api/libros/{id}` - Actualizar un libro
- `DELETE /api/libros/{id}` - Eliminar un libro

## 📝 Ejemplo de uso

### Crear un libro (POST)
```bash
curl -X POST "http://localhost:8000/api/libros" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Cien años de soledad",
    "autor": "Gabriel García Márquez",
    "isbn": "978-0307474728",
    "editorial": "Editorial Sudamericana",
    "año_publicacion": 1967,
    "genero": "Realismo mágico",
    "descripcion": "Una obra maestra de la literatura latinoamericana"
  }'
```

### Listar libros (GET)
```bash
curl "http://localhost:8000/api/libros"
```

## 🔧 Modelo de Datos

```python
{
    "id": int,              # Generado automáticamente
    "titulo": str,          # Requerido
    "autor": str,           # Requerido
    "isbn": str,            # Opcional, debe ser único
    "editorial": str,       # Opcional
    "año_publicacion": int, # Opcional
    "genero": str,          # Opcional
    "descripcion": str,     # Opcional
    "created_at": datetime, # Generado automáticamente
    "updated_at": datetime  # Actualizado automáticamente
}
```

## 🐳 Docker

El contenedor incluye:
- Python 3.11 slim
- FastAPI + Uvicorn
- SQLAlchemy
- Psycopg2
- Recarga automática en desarrollo

## 🔗 Integración con N8N

La API está diseñada para trabajar con N8N. Cuando ambos servicios están en la misma red Docker, usar:
- URL interna: `http://backend:8000/api/libros`
- URL externa: `http://localhost:8000/api/libros`

## 📄 Documentación API

Una vez ejecutada la API, acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🗃️ Base de Datos

La aplicación crea automáticamente las tablas necesarias al iniciar. La base de datos está alojada en Neon.tech con las siguientes características:
- PostgreSQL compatible
- SSL requerido
- Connection pooling habilitado

## 🚨 Notas Importantes

1. **Seguridad**: En producción, no expongas las credenciales en el docker-compose.yml. Usa Docker secrets o variables de entorno seguras.

2. **CORS**: La API tiene CORS habilitado para permitir todas las orígenes. En producción, restringe esto.

3. **ISBN Único**: Si proporcionas un ISBN, debe ser único. La API rechazará libros con ISBN duplicados.

## 📦 Estructura del Proyecto

```
backend/
├── main.py           # Aplicación principal y endpoints
├── models.py         # Modelos SQLAlchemy
├── database.py       # Configuración de base de datos
├── requirements.txt  # Dependencias Python
├── Dockerfile        # Configuración Docker
└── README.md         # Este archivo
```

## 🤝 Contribuir

Este es un proyecto educativo. Siéntete libre de mejorarlo y adaptarlo a tus necesidades.

## 📧 Soporte

Para problemas o preguntas, revisa:
1. Los logs del contenedor: `docker logs biblioteca-api`
2. La documentación de FastAPI: https://fastapi.tiangolo.com/
3. La documentación de Neon: https://neon.tech/docs/

