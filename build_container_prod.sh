#!/bin/bash

# Obtener el tag del último commit
echo "🔍 Obteniendo el tag del último commit"
TAG=$(git rev-parse --short HEAD)

### MODIFICAR CON LOS DATOS DE TU PROYECTO #################
IMAGE_NAME=score-credit-backend-prod # Nombre de la imagen de Docker
ORG=arrendamex.azurecr.io      # Namespace del registro de contenedor
###########################################################

# Construir la imagen de Docker
echo "🚀 Construyendo la imagen $IMAGE_NAME:$TAG para producción\n"
if docker buildx build --platform linux/amd64 -f Dockerfile.prod -t $IMAGE_NAME:$TAG .; then
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

fi