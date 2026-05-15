# Cosmox Blog

Módulo backend para la gestión de blogs de la tienda virtual de videojuegos Cosmox.

## Requisitos

- Python 3.13 o superior
- pip

## Instalación manual

### 1. Clonar repositorio

```bash
git clone https://github.com/DarienVB/Modulo-de-blog-para-Cosmox
cd blog
```

### 2. Crear entorno virtual

```bash
python -m venv env
```

### 3. Activar entorno virtual

Windows:

```bash
env\Scripts\activate
```

Linux:

```bash
source env/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor

```bash
python manage.py runserver
```

### 8. Abrir navegador

```txt
http://127.0.0.1:8000/
```
