# Integración Visual Studio Code + GitHub + Azure

![vscode+github+azure](https://github.com/user-attachments/assets/34b66048-c1c2-494c-82a6-b4616f2ee17b)

---

# Índice

1. [**Integración Visual Studio Code + GitHub + Azure**](#integración-visual-studio-code--github--azure)
2. [**🔑 Iniciar sesión en Azure CLI**](#-iniciar-sesión-en-azure-cli)
   1. [**🪟 Windows**](#-windows)
   2. [**🍎 macOS**](#-macos)
   3. [**👨‍💻 Linux (WSL - Ubuntu)**](#-linux-wsl---ubuntu)
      - [**⚡ Opción 1: Instalar con comandos**](#-opción-1-instalar-con-comandos)
      - [**🗒️ Opción 2: Instalar paso a paso**](#-opción-2-instalar-paso-a-paso)
   4. [**✅ Verificar la instalación**](#-verificar-la-instalación)
   5. [**🔄 Actualizar el Azure CLI**](#-actualizar-el-azure-cli)
      - [**🪟 Linux (WSL - Ubuntu)**](#-linux-wsl---ubuntu-1)
      - [**🌐 Windows, macOS y Linux**](#-windows-macos-y-linux)
3. [**🔐 Iniciar sesión en Azure CLI**](#-iniciar-sesión-en-azure-cli-1)
4. [**Cerrar sesión en Azure CLI**](#cerrar-sesión-en-azure-cli)
5. [**🔑 Acceso a Azure Container Registry**](#-acceso-a-azure-container-registry)
   - [**📦 Iniciar sesión en el registro de contenedores de Azure**](#-iniciar-sesión-en-el-registro-de-contenedores-de-azure)
6. [**⚡ Desplegar aplicación de React + Vite en App Service**](#-desplegar-aplicación-de-react--vite-en-app-service)
   1. [**🧪 App Service - Ambiente de pruebas**](#-app-service---ambiente-de-pruebas)
   2. [**⚡ Modificar configuraciones en `vite.config.js`**](#-modificar-configuraciones-en-viteconfigjs)
   3. [**💻 Crear un Dockerfile**](#-crear-un-dockerfile)
   4. [**📦 Compilar la imagen de Docker**](#-compilar-la-imagen-de-docker)
   5. [**Envío de la imagen al registro de contenedores**](#envío-de-la-imagen-al-registro-de-contenedores)
7. [**🔎 Monitorear el registro de Logs de App Service**](#-monitorear-el-registro-de-logs-de-app-service)
8. [**🏭 App Service - Ambiente de producción**](#-app-service---ambiente-de-producción)
9. [**⚡ Modificar configuraciones en `vite.config.js`**](#-modificar-configuraciones-en-viteconfigjs-1)
10. [**💻 Crear un Dockerfile**](#-crear-un-dockerfile-1)
11. [**📦 Compilar la imagen de Docker**](#-compilar-la-imagen-de-docker-1)
12. [**🔎 Monitorear el registro de Logs de App Service**](#-monitorear-el-registro-de-logs-de-app-service-1)

---

# 🔑 Iniciar sesión en Azure CLI

> [!IMPORTANT]
> Para instalar e iniciar sesión con Azure CLI, sigue los siguientes pasos dependiendo del sistema operativo en el que desees instalarlo.

## 🪟 Windows

Ve al siguiente enlace de [instalación de Azure CLI](https://learn.microsoft.com/es-es/cli/azure/install-azure-cli-windows?tabs=azure-cli). Selecciona el instalador a descargar de acuerdo con la arquitectura de tu computadora, si es de **32 bits** o **64 bits**.

![Captura de pantalla 2024-10-21 172759](https://github.com/user-attachments/assets/7eb9a5e3-1b9b-4086-86f7-73eb25ecc621)

Ejecuta el instalador como administrador y sigue las instrucciones en pantalla.

## 🍎 macOS

Ve al siguiente enlace de [instalacion de Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-macos) para MacOs para más información.

Abre la termina, copia, pega y ejecuta el siguiente comando de instalación.

```shell
# Instalar el Azure CLI desde el administrador de paquetes de macOS
brew update && brew install azure-cli
```

## 👨‍💻 Linux (WSL - Ubuntu)

### ⚡Opción 1: Instalar con comandos

Abre la termina y ejecuta los siguientes comandos de instalación

```shell
# Descargar el archivo de instalación y ejecutarlo.
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Una buena práctica es siempre leer el contenido de los archivos de instalación que vas a ejecutar en tu máquina local. La tubería en `| sudo bash` se encarga de ejecutar las instrucciones del archivo de instalación automáticamente.

### 🗒️Opción 2: Instalar paso a paso

Obtener los paquetes necesarios para el proceso

```shell
# Actualizar el repositorio de software local
sudo apt-get update
# Instalar paquetes necesarios
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
```

Descargar e instalar la llave de acceso de Microsoft

```shell
sudo mkdir -p /etc/apt/keyrings
curl -sLS https://packages.microsoft.com/keys/microsoft.asc |
  gpg --dearmor | sudo tee /etc/apt/keyrings/microsoft.gpg > /dev/null
sudo chmod go+r /etc/apt/keyrings/microsoft.gpg
```

Añadir Azure CLI al repositorio de software local

```shell
AZ_DIST=$(lsb_release -cs)
echo "Types: deb
URIs: https://packages.microsoft.com/repos/azure-cli/
Suites: ${AZ_DIST}
Components: main
Architectures: $(dpkg --print-architecture)
Signed-by: /etc/apt/keyrings/microsoft.gpg" | sudo tee /etc/apt/sources.list.d/azure-cli.sources
```

Actualizar el repositorio de referencias local e instalar el paquete

```shell
# Actualizar la lista de paquetes recientemennte añadida
sudo apt-get update
# Instalar Azure CLI de la lista de paquetes
sudo apt-get install azure-cli
```

## ✅ Verificar la instalación

Abre una terminal (o símbolo del sistema en Windows) y ejecuta el siguiente comando:

```shell
# Mostrar la versión de Azure CLI
az --version
```

Deberías ver información sobre la versión instalada de Azure CLI como esta.

![Captura de pantalla 2024-10-24 141035](https://github.com/user-attachments/assets/8f3d1295-d1d2-4c52-aaa9-bdb41db5b17e)

## 🔄 Actualizar el Azure CLI

En caso de que la CLI no esté actualizada o quieras verificar que existe una nueva versión e instalarla, puedes ejecutar los siguientes snippets:

### 🪟 Linux (WSL - Ubuntu)

A grandes rasgos, el script actualiza las referencias de paquetes del entorno local y actualiza las referencias a nuevas versiones, entonces, el administrador de paquetes de Linux puede descargar, instalar y actualizar estos.

```shell
# Actualizar la lista de versiones de paquetes
sudo apt-get update

# Actualizar Azure CLI únicamente
sudo apt-get install --only-upgrade -y azure-cli
```

### 🌐 Windows, macOS y Linux

Tambien puedes usar el comando integrado de Azure CLI para actualizar la herramienta únicamente en otros sistemas operativos, además de Linux.

```shell
# Actualizar Azure CLI con el comando integrado
az upgrade
```

## 🔐 Iniciar sesión en Azure CLI

Abre una terminal y ejecuta el siguiente comando:

```shell
# Iniciar sesión en Azure con el navegador
az login
```

Esto abrirá una nueva ventana del navegador donde deberás ingresar tus credenciales de Azure.
Si estás usando una cuenta de Azure con acceso a múltiples suscripciones, puedes listar las suscripciones autenticadas y establecer la suscripción por defecto con:

```shell
# Listar las cuentas de Azure autenticadas
az account list
```

Esto mostrará una salida similar a esta:

```raw
[
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "********-****-****-****-************",
    "id": "********-****-****-****-************",
    "isDefault": true,
    "managedByTenants": [],
    "name": "Microsoft Azure DevOps",
    "state": "Enabled",
    "tenantDefaultDomain": "********.mx",
    "tenantDisplayName": "******** S.A. DE C.V.",
    "tenantId": "********-****-****-****-************",
    "user": {
      "name": "********@********.mx",
      "type": "user"
    }
  },
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "********-****-****-****-************",
    "id": "********-****-****-****-************",
    "isDefault": false,
    "managedByTenants": [],
    "name": "Azure for Students",
    "state": "Enabled",
    "tenantId": "********-****-****-****-************",
    "user": {
      "name": "********@********.com",
      "type": "user"
    }
  }
]
```

Ahora copia valor de id de la suscripción deseada y reemplázalo en el siguiente comando para fijarla como la cuenta predeterminada de Azure CLI

```shell
# Seleccionar una suscripción de Azure
az account set --subscription "subscription id o name"
```

Ahora, deberías estar listo para usar Azure CLI con tu cuenta de Azure.

## Cerrar sesión en Azure CLI

Para remover el acceso a una cuenta de Azure, usa el siguiente comando:

```shell
# Cerrar sesión en Azure CLI
az logout
```

Adicionalmente, podrías querer quitar del listado de suscripciones y caché la cuenta de Azure de la que acabas de cerrar sesión. Para hacer esto, escribe el siguiente comando:

```shell
# Limpiar la caché de cuentas registradas en Azure CLI
az account clear
```

> [!WARNING]
> Limpiar la caché de la suscripción no es el mismo proceso de cierre de sesión de Azure. Sin embargo, cuando limpias la caché de la suscripción, no podrás ejecutar comandos como `az account set` hasta que vuelvas a iniciar sesión en una cuenta de nuevo.

---

# 🔑 Acceso a Azure Container Registry

![login acr](https://github.com/user-attachments/assets/dbe82a3b-6947-4efc-94fe-f4e54c36c6b0)

Azure Container Registry es un servicio de almacenamiento y administración de imagenes de Docker basado en el estándar OCI (Open Container Initiative), que rige los estándares para aplicaciones basadas en contenedores.

Para poder desplegar las aplicaciones en la nube, el registro de contenedores fungirá como un intermediario entre el entorno de desarrollo y la infraestructura de despliegue en la nube de Azure.

Cada vez que se añada una nueva imagen con la etiqueta latest dentro del registro de contenedores, App Service, el servicio encargado de hospedar las aplicaciones será notificado de que hay una nueva versión de la aplicación disponible y, automáticamente, actualizará la aplicación con esta nueva versión.

La configuración de despliegue automático en App Service con Azure Container Registry será configurada por Ennoven ya que es una característica que no se añade por defecto en la configuración inicial de este servicio.

## 📦 Iniciar sesión en el registro de contenedores de Azure

Para poder usar el servicio necesitarás tener instalado el cliente de Docker y datos adicionales del registro de contenedores privado de Azure.

> [!IMPORTANT]
> Ennoven te proporcionará tanto la **URI del registro de contenedores**, así como el **nombre de usuario** y el **access token** para iniciar sesión en el servicio.

Copia, modifica y pega el siguiente snippet en la terminal y modificar <container-registry-uri> por la URI del recurso. Haz un Enter.

```shell
# Iniciar sesión en Azure Container Registry
docker login <container-registry-uri>
```

El servicio te pedirá el nombre de usuario y un token de acceso. Cópialos y pégalos en la terminal, da Enter y listo. Debería aparecer un mensaje de inicio de sesión como este:

![image](https://github.com/user-attachments/assets/63858409-3ec6-404d-9fc7-fc889cb90af4)

> [!WARNING]
> Este tutorial no incluye instrucciones para instalar Docker, que es necesario para realizar todos estos procesos, pero puedes encontrar una [guía rápida de instalación](https://docs.docker.com/engine/install/) en el siguiente recurso oficial de Docker.

---

# ⚡ Desplegar aplicación de React + Vite en App Service

![fastapi+appservice+container_registry](https://github.com/user-attachments/assets/6a189c45-23a0-43a0-8e31-9d0854a52c01)


## 🧪App Service - Ambiente de pruebas

Para desplegar la aplicación en el ambiente de pruebas, se necesitan algunos conocimientos básicos de Docker, de Git y de la terminal para administrar los recursos de Azure CLI.
Los pasos para seguir se describen a continuación:

## 💻 Crear un Dockerfile

> [!NOTE]
> El Dockerfile es un archivo de texto que contiene todas las instrucciones para construir una imagen de Docker. Es como una receta que le dice a Docker cómo configurar el entorno en el cual correrá tu aplicación. Contiene comandos para instalar dependencias, copiar archivos y definir configuraciones.El siguiente Dockerfile contiene instrucciones para compilar una imagen de Docker para una aplicación de FastAPI.

`./Dockerfile.dev`

```dockerfile
# syntax=docker/dockerfile:1

#############################################
# Etapa 1: Compilar imagen dev-dependencies #
#############################################

# Obtener la imagen de Python
FROM cgr.dev/chainguard/python:latest-dev AS dev
# Crear un directorio de trabajo y establecerlo como el directorio de trabajo actual
WORKDIR /app
# Crear una ambiente virtual para instalar las dependencias
RUN python -m venv venv
# Establecer el ambiente virtual al PATH para ser accesible desde Python
ENV PATH="/app/venv/bin:$PATH"
# Copiar la lista de dependencias al directorio de trabajo
COPY requirements.txt requirements.txt
# Instalar las dependencias
RUN pip install -r requirements.txt
# Eliminar pip para evitar brechas de seguridad
RUN pip uninstall -y pip

# Exponer el puerto 8000 del contenedor
EXPOSE 8000

# Establecer el punto de entrada para ejecutar la aplicación
ENTRYPOINT ["fastapi", "dev", "main.py"]
```

## 📦 Compilar la imagen de Docker

Para construir una imagen de Docker a partir del código fuente, se creará un archivo en Bash para compilar la imagen cada vez que se tenga una nueva versión finalizada del código en el ambiente de desarrollo.

> [!IMPORTANT]
> En la carpeta del proyecto, crea un archivo llamado `build_container_dev.sh`, copia y pega el código que se proporciona abajo, y modifica los siguientes parámetros:
>
> El parámetro `IMAGE_NAME` con un nombre personalizado para tu imagen de Docker.
> El parámetro `ORG` con el namespace de tu registro de contenedores.

> [!NOTE]
> Ennoven les proporcionará el namespace cuando se cree el registro de contenedores de Azure.

`./build_container_dev.sh`

```shell
#!/bin/bash

# Obtener el tag del último commit
echo "🔍 Obteniendo el tag del último commit"
TAG=$(git rev-parse --short HEAD)

### MODIFICAR CON LOS DATOS DE TU PROYECTO #################
IMAGE_NAME=mycontainer # Nombre de la imagen de Docker
ORG=mynamespace      # Namespace del registro de contenedor
###########################################################

# Construir la imagen de Docker
echo "🚀 Construyendo la imagen $IMAGE_NAME:$TAG para desarrollo\n"
if docker build -f Dockerfile.dev -t $IMAGE_NAME:$TAG .; then
    #######################################################
    # Crear etiquetas de la imagen compilada
    #######################################################
          
    # Crear una imagen con el tag del último commit
    echo "🔗 Creando un enlace simbólico a $IMAGE_NAME:$TAG"
    docker tag $IMAGE_NAME:$TAG $ORG/$IMAGE_NAME:$TAG
    # Confirmar que la imagen se ha creado
    echo "✅ La imagen $IMAGE_NAME:$TAG se ha creado correctamente\n"

    # Crear una imagen con el tag latest
    echo "🔗 Creando un enlace simbólico a $IMAGE_NAME:latest"
    docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:latest
    # Confirmar que la imagen se ha creado
    echo "✅ La imagen $IMAGE_NAME:latest se ha creado correctamente\n"

    # Crear una imagen con el tag remoto para el último commit
    echo "🔗 Creando un enlace simbólico a $ORG/$IMAGE_NAME:$TAG"
    docker tag $IMAGE_NAME:$TAG $ORG/$IMAGE_NAME:$TAG
    # Confirmar que la imagen se ha creado
    echo "✅ La imagen $ORG/$IMAGE_NAME:$TAG se ha creado correctamente\n"

    # Crear una imagen con el tag remoto para el tag latest
    echo "🔗 Creando un enlace simbólico a $ORG/$IMAGE_NAME:latest"
    docker tag $IMAGE_NAME:$TAG $ORG/$IMAGE_NAME:latest
    # Confirmar que la imagen se ha creado
    echo "✅ La imagen $ORG/$IMAGE_NAME:latest se ha creado correctamente\n"


    #######################################################
    # Enviar la imagen de Docker al registro de contenedor
    #######################################################
    
    # Enviar la imagen al registro de contenedores de Azure Container Registry
    echo "📤 Enviando la imagen $ORG/$IMAGE_NAME:$TAG al registro de contenedores de Azure Container Registry"
    docker push $ORG/$IMAGE_NAME:$TAG

    # Enviando la imagen con el tag latest
    echo "\n📤 Enviando la imagen $ORG/$IMAGE_NAME:latest al registro de contenedores de Azure Container Registry"
    docker push $ORG/$IMAGE_NAME:latest
else
    # Mostrar un mensaje de error si la imagen no se ha creado
    echo "❌ Ha ocurrido un error al crear la imagen $IMAGE_NAME:$TAG"
    exit 1
```

Para ejecutar el script, abre una termina dentro del mismo directorio donde se encuentra el archivo `build_container_dev.sh` y escribe lo siguiente para ejecutarlo.

```shell
# Ejecutar el script de compilación de imágenes de Docker
sh build_container_dev.sh
```

## 🔎 Monitorear el registro de Logs de App Service

Para iniciar el monitor de App Service, escribe en la terminal el siguiente comando:

> [!IMPORTANT]
> Abre una terminal, copia y pega el snippet abajo de esta instrucción y modifica los siguientes parámetros:
>
> El parámetro `<myapp>` con el nombre de la aplicación en App Service.
> El parámetro `<resource-group-name>` con el nombre del grupo de recursos de la aplicación.

```shell
az webapp log tail --name <myapp> --resource-group <resource-group-name>
```

En la misma terminal deberías poder ver los registros de la salida estándar de tu aplicación similar a los que se muestran a continuación. Estos registros incluyen respuestas peticiones HTTP y prints de textos que hayas colocado en tu código durante el debug.

```raw
2024-09-11T20:26:52  Welcome, you are now connected to log-streaming service.
Starting Log Tail -n 10 of existing logs ----
/appsvctmp/volatile/logs/runtime/container.log
2024-09-11T20:26:48.9033327Z Reproduciendo chunk...
2024-09-11T20:26:48.9033354Z Reproduciendo chunk...
2024-09-11T20:26:48.9033388Z Guardando grabación de audio en el blob storage
2024-09-11T20:26:48.9033419Z Recepción de datos de audio detenida
2024-09-11T20:26:48.9033445Z WebSocket desconectado
2024-09-11T20:26:48.9033472Z Finalizando tareas...
2024-09-11T20:26:48.9033500Z Transcripción detenida
2024-09-11T20:26:48.9033547Z Las tareas han sido finalizadas para el chat id 978359c7-7d12-4df2-a2d0-093c36aa007d
2024-09-11T20:26:48.9033576Z Reconocimiento detenido
2024-09-11T20:26:48.9033606Z INFO:     169.254.130.6:41408 - "GET / HTTP/1.1" 404 Not Found
/appsvctmp/volatile/logs/runtime/container.2.log
2024-09-09T20:45:41.7411610Z Reproduciendo chunk...
2024-09-09T20:45:41.7411636Z Reproduciendo chunk...
2024-09-09T20:45:41.7411662Z Recibiendo audio...
2024-09-09T20:45:41.7411689Z Reproduciendo chunk...
2024-09-09T20:45:41.7411714Z Reproduciendo chunk...
2024-09-09T20:45:41.7411740Z Reproduciendo chunk...
2024-09-09T20:45:41.7411766Z Reproduciendo chunk...
2024-09-09T20:45:41.7411794Z Recibiendo audio...
2024-09-09T20:45:41.7411835Z Reproduciendo chunk...
2024-09-09T20:45:41.7411862Z Reproduciendo chunk...
/appsvctmp/volatile/logs/runtime/container.1.log
2024-09-09T18:17:51.3144779Z 06.17.51.312786
Ending Log Tail of existing logs ---
Starting Live Log Stream ---
2024-09-11T20:27:53  No new trace in the past 1 min(s).
```

## 🏭 App Service - Ambiente de producción

Para desplegar la aplicación en el ambiente de producción, se necesitan algunos conocimientos básicos de Docker, de Git y de la terminal para administrar los recursos de Azure CLI.
Los pasos para seguir se describen a continuación:

## 💻 Crear un Dockerfile

> [!NOTE]
> El Dockerfile es un archivo de texto que contiene todas las instrucciones para construir una imagen de Docker. Es como una receta que le dice a Docker cómo configurar el entorno en el cual correrá tu aplicación. Contiene comandos para instalar dependencias, copiar archivos y definir configuraciones. El siguiente Dockerfile contiene instrucciones para compilar una imagen de Docker para una aplicación de Vite + React.

`./Dockerfile.prod`

```dockerfile
# syntax=docker/dockerfile:1

#############################################
# Etapa 1: Compilar imagen dev-dependencies #
#############################################

# Obtener la imagen de Python
FROM cgr.dev/chainguard/python:latest-dev AS dev
# Crear un directorio de trabajo y establecerlo como el directorio de trabajo actual
WORKDIR /app
# Crear una ambiente virtual para instalar las dependencias
RUN python -m venv venv
# Establecer el ambiente virtual al PATH para ser accesible desde Python
ENV PATH="/app/venv/bin:$PATH"
# Copiar la lista de dependencias al directorio de trabajo
COPY requirements.txt requirements.txt
# Instalar las dependencias
RUN pip install -r requirements.txt
# Eliminar pip para evitar conflictos con CVE
RUN pip uninstall -y pip


#############################################
# Etapa 2: Compilar imagen de producción    #
#############################################
# Obtener la imagen de Python mínima
FROM cgr.dev/chainguard/python:latest AS prod
# Crear un directorio de trabajo y establecerlo como el directorio de trabajo actual
WORKDIR /app
# Copiar el código fuente al directorio de trabajo
COPY . /app/
# Copiar el ambiente virtual de la imagen dev-dependencies
COPY --from=dev /app/venv /app/venv
# Establecer el ambiente virtual al PATH para ser accesible desde Python
ENV PATH="/app/venv/bin:$PATH"

# Exponer el puerto 8000 del contenedor
EXPOSE 8000

# Establecer el punto de entrada para ejecutar la aplicación
ENTRYPOINT ["fastapi", "run", "main.py"]
```

## 📦 Compilar la imagen de Docker

Para construir una imagen de Docker a partir del código fuente, se creará un archivo en Bash para compilar la imagen cada vez que se tenga una nueva versión finalizada del código en el ambiente de producción.

> [!IMPORTANT]
> En la carpeta del proyecto, crea un archivo llamado `build_container_prod.sh`, copia y pega el código que se proporciona abajo, y modifica los siguientes parámetros:
>
> El parámetro `IMAGE_NAME` con un nombre personalizado para tu imagen de Docker.
> El parámetro `ORG` con el namespace de tu registro de contenedores.

> [!NOTE]
> Ennoven les proporcionará el namespace cuando se cree el registro de contenedores de Azure.

`./build_container_prod.sh`

```bash
#!/bin/bash

# Obtener el tag del último commit
echo "🔍 Obteniendo el tag del último commit"
TAG=$(git rev-parse --short HEAD)

### MODIFICAR CON LOS DATOS DE TU PROYECTO #################
IMAGE_NAME=mycontainer # Nombre de la imagen de Docker
ORG=mynamespace      # Namespace del registro de contenedor
###########################################################

# Construir la imagen de Docker
echo "🚀 Construyendo la imagen $IMAGE_NAME:$TAG para producción\n"
if docker build -f Dockerfile.prod -t $IMAGE_NAME:$TAG .; then
    #######################################################
    # Crear etiquetas de la imagen compilada
    #######################################################
          
    # Crear una imagen con el tag del último commit
    echo "🔗 Creando un enlace simbólico a $IMAGE_NAME:$TAG"
    docker tag $IMAGE_NAME:$TAG $ORG/$IMAGE_NAME:$TAG
    # Confirmar que la imagen se ha creado
    echo "✅ La imagen $IMAGE_NAME:$TAG se ha creado correctamente\n"

    # Crear una imagen con el tag latest
    echo "🔗 Creando un enlace simbólico a $IMAGE_NAME:latest"
    docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:latest
    # Confirmar que la imagen se ha creado
    echo "✅ La imagen $IMAGE_NAME:latest se ha creado correctamente\n"

    # Crear una imagen con el tag remoto para el último commit
    echo "🔗 Creando un enlace simbólico a $ORG/$IMAGE_NAME:$TAG"
    docker tag $IMAGE_NAME:$TAG $ORG/$IMAGE_NAME:$TAG
    # Confirmar que la imagen se ha creado
    echo "✅ La imagen $ORG/$IMAGE_NAME:$TAG se ha creado correctamente\n"

    # Crear una imagen con el tag remoto para el tag latest
    echo "🔗 Creando un enlace simbólico a $ORG/$IMAGE_NAME:latest"
    docker tag $IMAGE_NAME:$TAG $ORG/$IMAGE_NAME:latest
    # Confirmar que la imagen se ha creado
    echo "✅ La imagen $ORG/$IMAGE_NAME:latest se ha creado correctamente\n"


    #######################################################
    # Enviar la imagen de Docker al registro de contenedor
    #######################################################
    
    # Enviar la imagen al registro de contenedores de Azure Container Registry
    echo "📤 Enviando la imagen $ORG/$IMAGE_NAME:$TAG al registro de contenedores de Azure Container Registry"
    docker push $ORG/$IMAGE_NAME:$TAG

    # Enviando la imagen con el tag latest
    echo "\n📤 Enviando la imagen $ORG/$IMAGE_NAME:latest al registro de contenedores de Azure Container Registry"
    docker push $ORG/$IMAGE_NAME:latest
else
    # Mostrar un mensaje de error si la imagen no se ha creado
    echo "❌ Ha ocurrido un error al crear la imagen $IMAGE_NAME:$TAG"
    exit 1
```

Para ejecutar el script, abre una termina dentro del mismo directorio donde se encuentra el archivo `build_container_prod.sh` y escribe lo siguiente para ejecutarlo.

```shell
# Ejecutar el script de compilación de imágenes de Docker
sh build_container_prod.sh
```

## 🔎 Monitorear el registro de Logs de App Service

Para iniciar el monitor de App Service, escribe en la terminal el siguiente comando:

> [!IMPORTANT]
> Abre una terminal, copia y pega el snippet abajo de esta instrucción y modifica los siguientes parámetros:
>
> El parámetro `<myapp>` con el nombre de la aplicación en App Service.
> El parámetro `<resource-group-name>` con el nombre del grupo de recursos de la aplicación.

```shell
az webapp log tail --name <myapp> --resource-group <resource-group-name>
```

En la misma terminal deberías poder ver los registros de la salida estándar de tu aplicación similar a los que se muestran a continuación. Estos registros incluyen respuestas peticiones HTTP y prints de textos que hayas colocado en tu código durante el debug.

```raw
2024-09-11T20:26:52  Welcome, you are now connected to log-streaming service.
Starting Log Tail -n 10 of existing logs ----
/appsvctmp/volatile/logs/runtime/container.log
2024-09-11T20:26:48.9033327Z Reproduciendo chunk...
2024-09-11T20:26:48.9033354Z Reproduciendo chunk...
2024-09-11T20:26:48.9033388Z Guardando grabación de audio en el blob storage
2024-09-11T20:26:48.9033419Z Recepción de datos de audio detenida
2024-09-11T20:26:48.9033445Z WebSocket desconectado
2024-09-11T20:26:48.9033472Z Finalizando tareas...
2024-09-11T20:26:48.9033500Z Transcripción detenida
2024-09-11T20:26:48.9033547Z Las tareas han sido finalizadas para el chat id 978359c7-7d12-4df2-a2d0-093c36aa007d
2024-09-11T20:26:48.9033576Z Reconocimiento detenido
2024-09-11T20:26:48.9033606Z INFO:     169.254.130.6:41408 - "GET / HTTP/1.1" 404 Not Found
/appsvctmp/volatile/logs/runtime/container.2.log
2024-09-09T20:45:41.7411610Z Reproduciendo chunk...
2024-09-09T20:45:41.7411636Z Reproduciendo chunk...
2024-09-09T20:45:41.7411662Z Recibiendo audio...
2024-09-09T20:45:41.7411689Z Reproduciendo chunk...
2024-09-09T20:45:41.7411714Z Reproduciendo chunk...
2024-09-09T20:45:41.7411740Z Reproduciendo chunk...
2024-09-09T20:45:41.7411766Z Reproduciendo chunk...
2024-09-09T20:45:41.7411794Z Recibiendo audio...
2024-09-09T20:45:41.7411835Z Reproduciendo chunk...
2024-09-09T20:45:41.7411862Z Reproduciendo chunk...
/appsvctmp/volatile/logs/runtime/container.1.log
2024-09-09T18:17:51.3144779Z 06.17.51.312786
Ending Log Tail of existing logs ---
Starting Live Log Stream ---
2024-09-11T20:27:53  No new trace in the past 1 min(s).
```
