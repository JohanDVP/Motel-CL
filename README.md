Motelandro:

Sistema basico degestion de reservar para un motel, este nos permite, registrar usuarios, ver habitaciones disponibles, hacer reservas y cancelar estas mismas desde la linea de comandos.

Que hace el proyecto?

1) Ver todas las habitaciones del motel(solo tenemos 2, somos un motel pobre)
2) Registrar usuarios nuevos
3) Hacer una reserva, eligiendo habitacion y horas
4) Cancelar una reserva existente
5) Ver todas las reservar registradas hasta el momento.

Instalación

Necesitas por obligación tener uv instalado, dirigete al siguiente link y sigue los pasos de instalacion que se te muestra en la pagina dependiendo de tu sistema operativo:

https://docs.astral.sh/uv/getting-started/installation/

Luego de esto, clona el repositorio e instala todas las dependencias, ejecutando los siguientes comandos en la terminal:

git clone (aqui va el link del repositorio)
cd motelandro
uv sync (Esto lee el archivo donde estan listadas todas las dependencias y las instala automaticamente como typer, pytest, etc)

Como usarlo?

- Para ver la gran basta cantidad de habitaciones del motel (solo 2):

uv run python main.py ver-rooms

- Para Registrar un usuario nuevo:

uv run python main.py registrar-usuarios

- Hacer una reserva de una habitacion:

uv run python main.py reservar

- Cancelar una reserva:

uv run python main.py cancelar-reserva

- Ver todas las reservas:

uv run python main.py listar-reservas

Estructura del proyecto:

motelandro/
├── data/
│   └── datos.json       # Base de datos local
├── src/app/
│   ├── models.py        # Clases de datos
│   ├── storage.py       # Lee y escribe el JSON
│   ├── services.py      # Lógica del negocio
│   └── exceptions.py    # Errores personalizados
├── tests/
│   ├── test_modelos.py
│   └── test_logica.py
├── main.py              # Interfaz de usuario
└── pyproject.toml

Para correr los test:

uv run pytest tests/ -v

Para medir complejidad ciclomatica:

uv run radon cc src -a  

Tecnologias usadas:

- Python 3.12
- uv (Gestion del proyecto)
- Typer (Para comandos en el main.py)
- Rich (Colores)
- Pytest (Para correr los test)
- IA (Herramienta de apoyo)



Docstrings
Excepciones