.. Administrador de Trabajos de Grado documentation master file, created by
   sphinx-quickstart on Thu Jan  9 17:18:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bienvenido a la documentación del Administrador de Trabajos de Grado!
=====================================================================

Funcionalidades
---------------
Este sistema tiene el proposito de llevar un registro de los trabajos de grado, así como también de sus propuestas y toda la información referente a las mismas. Entre sus funcionalidades se encuentran:

- Inicio de sesión para usuarios administradores gestores.
- Registro de personas involucradas en trabajos de grado, ya sean estudiantes, profesores o externos
- Registro de trabajos de grado con la siguiente información:
   - Titulo del TG
   - NRC
   - Estudiantes que lo realizan y toda su información
   - Tutores (Académico y Empresarial si aplica)
   - Compañia (Si aplica)
   - Fecha de inicio y de propuesta
   - Semestre de entrega
   - Propuesta de TG con toda su información
   - Estado de los TG
- Histórico de todos los TG que se han realizado.
- Estádisticas de los TG que se han realizado por semestre
- Exportación a pdf de la información presente en las distintas tablas

Instalación
-----------

Para instalar el proyecto debe tener instalado lo siguiente:

- Python 3.8
- pip
- virtualenv

Para correr el proyecto:

- Clonar el proyecto del repositorio
- Crear e inicializar el ambiente virtual
- Correr el comando pip install
- Con todas las dependencias instaladas ejecutar el siguiente comando:

   python manage.py runserver

Repositorio
-----------

Codigo Fuente: https://github.com/juan-goncalves/thesis-manager.git

License
-------

El projecto esta licensiado bajo la bsd