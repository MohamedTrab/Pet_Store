# Proyecto Pet Store

## Descripción General
El proyecto **Pet Store** es una aplicación web desarrollada com. Esta aplicación simula la gestión de una tienda de mascotas, incluyendo funcionalidades clave como autenticación de usuarios, manejo de inventarios, procesamiento de pedidos y mucho más. El sistema está diseñado con una arquitectura por capas y sigue principios modernos de desarrollo, incluyendo el uso de contenedores y despliegues en Kubernetes.

## Tecnologías Utilizadas
- **Backend**: Python (Flask).
- **Base de Datos**: PostgreSQL.
- **Contenedores**: Docker y Docker Compose.
- **Orquestación**: Kubernetes.
- **Documentación API**: Swagger (Flasgger).
- **Mensajería**: RabbitMQ.

## Estructura del Proyecto

```
pet_store/
├── app/                  # Código principal de la aplicación
├── migrations/           # Archivos de migración de la base de datos
├── Dockerfile            # Configuración para construir la imagen Docker
├── docker-compose.yml    # Configuración de servicios para Docker Compose
├── k8s/                  # Archivos de configuración de Kubernetes
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Este archivo
└── .venv/                # Entorno virtual (opcional para ejecución local)
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.9+
- Docker y Docker Compose
- Kubernetes CLI (kubectl) y minikube (opcional para local)

### Configuración Local
1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd pet_store
   ```

2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   Crear un archivo `.env` con las variables necesarias, por ejemplo:
   ```env
   DATABASE_URL=postgresql://usuario:password@localhost/pet_store
   SECRET_KEY=tu_clave_secreta
   ```

4. Aplicar migraciones:
   ```bash
   flask db upgrade
   ```

5. Ejecutar la aplicación:
   ```bash
   flask run
   ```

La aplicación estará disponible en `http://127.0.0.1:5000`.

### Uso con Docker
1. Construir y ejecutar los contenedores:
   ```bash
   docker-compose up --build
   ```

2. Acceder a la aplicación en `http://localhost:5000`.

### Despliegue en Kubernetes
1. Aplicar configuraciones de Kubernetes:
   ```bash
   kubectl apply -f k8s/
   ```

2. Verificar que los pods estén corriendo:
   ```bash
   kubectl get pods
   ```

3. Acceder a la aplicación (detalles dependen de la configuración de `k8s/service.yaml`).

## Funcionalidades

### Principales
- **Autenticación y Autorización**: Basada en JWT.
- **Gestión de Productos**: Crear, leer, actualizar y eliminar productos.
- **Carrito de Compras**: Agregar y quitar productos.
- **Procesamiento de Pedidos**: Conexión con pasarelas de pago simuladas.
- **Reseñas de Productos**: Los usuarios pueden dejar y visualizar reseñas de los productos.

### Extensiones
- **Monitoreo y Alertas**: Integración con herramientas como Prometheus y Grafana para supervisar el rendimiento.
- **Caché**: Uso de Redis para mejorar la velocidad de acceso a los datos frecuentemente solicitados.
- **Mensajería**: Uso de RabbitMQ para la comunicación entre servicios.

### Flujos de Comunicación
1. **Autenticación del Usuario (1:1)**:
   - El cliente inicia sesión y recibe un token de autenticación.
     ```
     Cliente ->> Usuarios: POST /api/users/login
     Usuarios -->> Cliente: Token de autenticación
     ```

2. **Búsqueda de Producto (1:N)**:
   - El usuario busca "collar para perro".
   - El servicio de Búsqueda consulta a Productos y Categorías para obtener resultados relevantes.
     ```
     Cliente ->> Búsqueda: GET /api/search?q=collar para perro
     Búsqueda ->> Productos: Consulta productos
     Búsqueda ->> Categorías: Consulta categorías
     Búsqueda -->> Cliente: Resultados de búsqueda
     ```

3. **Detalles del Producto (1:1)**:
   - El usuario selecciona un producto específico.
   - El servicio de Productos obtiene los detalles y un resumen de las reseñas.
     ```
     Cliente ->> Productos: GET /api/products/12345
     Productos ->> Reseñas: Obtiene resumen de reseñas
     Productos -->> Cliente: Detalles del producto
     ```

4. **Añadir al Carrito (1:1)**:
   - El usuario añade el producto al carrito.
   - El servicio de Carrito verifica la disponibilidad con el servicio de Productos.
     ```
     Cliente ->> Carrito: POST /api/cart/items
     Carrito ->> Productos: Verifica disponibilidad
     Carrito -->> Cliente: Confirmación de añadido al carrito
     ```

5. **Realizar Pedido (1:N)**:
   - El usuario realiza un pedido.
   - El servicio de Pedidos verifica la dirección con Usuarios, obtiene los ítems del Carrito y actualiza el inventario en Productos.
     ```
     Cliente ->> Pedidos: POST /api/orders
     Pedidos ->> Usuarios: Verifica dirección
     Pedidos ->> Carrito: Obtiene ítems del carrito
     Pedidos ->> Productos: Actualiza inventario
     Pedidos -->> Cliente: Confirmación de pedido
     ```

## Pruebas
1. Configurar un entorno de pruebas con datos de ejemplo.
2. Utilizar herramientas como Postman o cURL para probar los endpoints.
3. Verificar que los flujos de trabajo funcionen correctamente:
   - Registro e inicio de sesión.
   - Gestión de productos.
   - Añadir y consultar el carrito.
   - Procesamiento de pedidos.

## Contribuciones
Para contribuir:
1. Realizar un fork del repositorio.
2. Crear una rama para la nueva funcionalidad o corrección:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Enviar un pull request detallado.

## Licencia
Este proyecto está bajo la licencia MIT. Para más información, consulta el archivo `LICENSE`.

