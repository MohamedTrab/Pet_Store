# Proyecto Pet Store

## Descripción General
El proyecto **Pet Store** es una aplicación web diseñada para simular la gestión de una tienda de mascotas. Esta aplicación incluye funcionalidades clave como la autenticación de usuarios, la gestión de inventarios, el procesamiento de pedidos, entre otras. El sistema está diseñado con una arquitectura en capas y sigue principios modernos de desarrollo, incluyendo el uso de contenedores y despliegues en Kubernetes.

## Tecnologías Utilizadas
- **Backend**: Python (Flask).
- **Base de Datos**: PostgreSQL.
- **Mensajería**: RabbitMQ.
- **Contenedores**: Docker y Docker Compose.
- **Orquestación**: Kubernetes.
- **Documentación API**: Swagger (Flasgger).

## Estructura del Proyecto
```
pet_store/
├── app/                  # Código principal de la aplicación
├── migrations/           # Archivos de migración de la base de datos
├── Dockerfile            # Configuración para construir la imagen Docker
├── docker-compose.yml    # Configuración de servicios para Docker Compose
├── k8s/                  # Archivos de configuración Kubernetes
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Este archivo
└── .venv/                # Entorno virtual (opcional para ejecución local)
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.9+
- Docker y Docker Compose
- Kubernetes CLI (kubectl) y Minikube (opcional para pruebas locales)

### Configuración Local

1. **Clonar el repositorio**:
```bash
git clone <url-del-repositorio>
cd pet_store
```

2. **Crear un entorno virtual e instalar dependencias**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Configurar variables de entorno**:  
   Crear un archivo `.env` con las variables necesarias, por ejemplo:
   ```env
   DATABASE_URL=postgresql://usuario:contraseña@localhost/pet_store
   SECRET_KEY=tu_clave_secreta
   ```

4. **Aplicar migraciones**:
```bash
flask db upgrade
```

5. **Iniciar la aplicación**:
```bash
python -m uvicorn app:app --reload
```
La aplicación estará disponible en [http://127.0.0.1:5000](http://127.0.0.1:5000).

## RabbitMQ

RabbitMQ es una solución de mensajería de código abierto que gestiona mensajes asíncronos entre diferentes servicios o componentes de una aplicación. En este proyecto, RabbitMQ se utiliza para publicar y consumir mensajes mediante colas como:
- **user_registration**
- **cart_creation**
- **category_creation**

### Creación Automática de Colas
Las colas necesarias se crean automáticamente al iniciar la aplicación, utilizando el protocolo AMQP (Advanced Message Queuing Protocol). AMQP es un estándar para la comunicación entre productores y consumidores de mensajes, asegurando una gestión fiable de los intercambios.

### Configuración con Docker
Para configurar RabbitMQ con Docker, usa la imagen oficial:
```bash
docker pull rabbitmq:3-management
```
Esta imagen incluye una interfaz de gestión accesible en [http://localhost:15672](http://localhost:15672) con las credenciales predeterminadas:
- **Usuario**: guest
- **Contraseña**: guest

Para publicar y consumir mensajes en RabbitMQ, la aplicación utiliza bibliotecas como `pika` (en Python).

### Comandos de Docker Compose
Con Docker Compose, puedes iniciar RabbitMQ y otros servicios definidos en el archivo `docker-compose.yml`:
```bash
docker-compose up -d
```
Esto inicia todos los contenedores necesarios, incluidas las siguientes bases de datos:
- **users_db**: `postgresql://postgres:postgres@localhost:5432/users_db`
- **products_db**: `postgresql://postgres:postgres@localhost:5432/products_db`
- **orders_db**: `postgresql://postgres:postgres@localhost:5432/orders_db`
- **reviews_db**: `postgresql://postgres:postgres@localhost:5432/reviews_db`
- **pets_db**: `postgresql://postgres:postgres@localhost:5432/pets_db`

Cada base de datos funciona en un contenedor independiente y está conectada a la aplicación mediante variables de entorno.

## Docker
Docker simplifica el despliegue de aplicaciones al contenerizar dependencias y configuraciones necesarias.

### Función de Docker
- **Aislamiento**: Cada servicio (aplicación, bases de datos, RabbitMQ) funciona en un contenedor independiente.
- **Portabilidad**: Los contenedores Docker pueden desplegarse en cualquier entorno compatible con Docker.

### Iniciar la Aplicación con Docker
1. Construir la imagen Docker:
   ```bash
   docker build -t pet_store .
   ```
2. Iniciar la aplicación:
   ```bash
   docker-compose up -d
   ```
   Esto inicia todos los servicios definidos, incluyendo RabbitMQ y las bases de datos.

## Kubernetes

Kubernetes se utiliza para orquestar y gestionar los contenedores, ofreciendo funcionalidades avanzadas como:
- **Escalado Automático**: Ajuste dinámico de pods según la carga.
- **Resiliencia**: Reinicio automático de pods defectuosos.
- **Gestión de Recursos**: Uso eficiente de CPU y memoria.

### Despliegue en Kubernetes
Para desplegar la aplicación y sus servicios (incluyendo RabbitMQ):
1. Aplicar los archivos de configuración de Kubernetes:
   ```bash
   kubectl apply -f k8s/
   ```
2. Verificar los pods en ejecución:
   ```bash
   kubectl get pods
   ```

### Optimización de la Aplicación
- **Horizontal Pod Autoscaler (HPA)**: Configura HPA para ajustar dinámicamente el número de pods según la carga:
  ```yaml
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  metadata:
    name: pet-store-hpa
  spec:
    scaleTargetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: pet-store
    minReplicas: 2
    maxReplicas: 10
    metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 75
  ```
- **Monitorización**: Utiliza herramientas como Prometheus y Grafana para supervisar el rendimiento y la disponibilidad.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

