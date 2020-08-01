===========
RemoteAuth
===========

Este proyecto busca crear los elementos compartidos entre todos los microservicios de
inmobilio.co.

Cuenta con los siguientes elementos:

* Modelo base para los objetos de usuario creados localmente en cada microservicio de django
* Serviciops para las tareas de autenticacion y almacenamiento de datos de los usuarios remotos.


Quick start
-----------

1. Instalar usando pipenv y llamando el paquete directo desde el repositorio:
    https://gitlab.com/inmobilio/backend/dependencies/dbtraits/-/archive/master/dbtraits-master.tar.gz

2. Aniadir la application a las INSTALLED_APPS de django de la siguiente manera:
    'remoteauth'

3. Añadir la siguiente configuracion:

INMOBILIO_AUTHENTICATION_SERVICE = {
'JWT_VALIDATION_URL': 'http://localhost:9000/auth/user'
}

4. Modificar el user model asi:

AUTH_USER_MODEL = 'remoteauth.authutils.models.User'
