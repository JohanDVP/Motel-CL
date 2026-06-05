Proyecto: Motelandro

Sistema de gestión integral para el motel Motelandro, diseñado para optimizar el control de habitaciones, el registro de clientes y la administración de reservas en tiempo real.

Que hace el proyecto?

El proyecto cuenta con 3 funcionalidades especificas para 3 operaciones principales, las cuales son mirar, agregar y eliminar, estas 3 funcionalidades estan implementadas para el registro de usuarios, la creacion de habitaciones y la reserva de estas mismas.

Estructura del Proyecto:

project/
├── src/
│   ├── api/          # Endpoints y routers de FastAPI
│   ├── app/          # Frontend con Streamlit
│   ├── core/         # Configuración y excepciones de dominio
│   ├── schemas/      # Modelos Pydantic
│   ├── services/     # Lógica de negocio
│   └── storage/      # Repositorios (Acceso a datos)
├── tests/            # Pruebas unitarias e integración
└── docs/             # Documentación técnica generada

Instalación y Ejecución:

1) Necesitas por obligación tener uv instalado, dirigete al siguiente link y sigue los pasos de instalacion que se te muestra en la pagina dependiendo de tu sistema operativo:

https://docs.astral.sh/uv/getting-started/installation/

Luego de esto, clona el repositorio e instala todas las dependencias, ejecutando los siguientes comandos en la terminal:

git clone (aqui va el link del repositorio)
cd motelandro
uv sync (Esto lee el archivo donde estan listadas todas las dependencias y las instala automaticamente como typer, pytest, etc)

2) Ejecutar Backend (FastAPI):

uv run uvicorn src.api.main:app --reload

3) Ejecutar Frontend (Streamlit):

uv run streamlit run src/app/main.py

Calidad y Automatización:

1) Pruebas: (Para ejecutar las pruebas y verificar la cobertura)

uv run pytest --cov=src

2) Linting y Calidad: (Para verificar el estilo de código con Ruff y la complejidad con Radon)

uv run ruff check src/
uv run radon cc src/ -a -s

Documentación:

La documentación tecnica completa se encuentra disponible corriendo:

uv run --active mkdocs serve 



Stack tecnologico Utilizado:

1. Backend (API y Lógica)
    
    FastAPI: Framework moderno de alto rendimiento para construir APIs REST.

    Pydantic: Utilizado para la validación de datos y la creación de esquemas (contratos de datos).

    Python 3.12: Lenguaje base del proyecto.

2. Base de Datos y Persistencia

    Supabase: Plataforma Backend-as-a-Service basada en PostgreSQL, utilizada para almacenar y gestionar los datos del sistema.

    Supabase-py: Librería cliente para la integración directa con Python.

3. Frontend (Interfaz de Usuario)

    Streamlit: Framework para crear aplicaciones web orientadas a datos de forma rápida, conectando el frontend directamente con la API mediante peticiones requests.

4. Calidad, Automatización y DevOps

    uv: Gestor de paquetes ultrarrápido y gestor de entornos virtuales.

    Pytest: Framework para pruebas unitarias e integración.

    Ruff: Linter y formateador de código extremadamente rápido para garantizar el cumplimiento de estándares.

    Radon: Herramienta para medir la complejidad ciclomática del código (garantizando mantenibilidad "Grado A").

    MkDocs (con Material theme): Generador de documentación técnica estática.

    GitHub Actions: Automatización de workflows para CI/CD (integración y despliegue continuo).



