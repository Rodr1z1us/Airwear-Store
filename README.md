
# AirWear API

1. **Endpoints por Modelo/Tabla**:
   - Se implementaron operaciones CRUD completas (Crear, Leer, Actualizar, Eliminar) para cada modelo:
     - **Marcas**: Crear, listar, obtener por ID, actualizar y eliminar marcas.
     - **Prendas**: Crear, listar, obtener por ID, actualizar y eliminar prendas, con manejo de inventario.
     - **Ventas**: Crear, listar, obtener por ID, actualizar y eliminar ventas, con gestión automática de inventario (resta al crear/actualizar, suma al eliminar).
   - Cada controlador está separado por modelo y utiliza el modelo correspondiente para interactuar con la base de datos.

2. **Demostración con Postman**:
   - El archivo `leeme.md` incluye instrucciones detalladas para probar cada endpoint utilizando Postman. Se proporcionan ejemplos de cuerpos JSON para las solicitudes POST y PUT, y se especifican las URLs para cada operación.

3. **Reportes**:
   - Se implementaron los tres reportes solicitados en un controlador dedicado (`controlador_reportes.py`):
     - **Marcas con al menos una venta**: `GET /api/v1/reportes/marcas-con-ventas`
     - **Prendas vendidas con inventario restante**: `GET /api/v1/reportes/prendas-vendidas-con-inventario`
     - **Cinco marcas más vendidas**: `GET /api/v1/reportes/cinco-marcas-mas-vendidas`
   - Cada reporte utiliza consultas SQLAlchemy optimizadas para obtener los datos requeridos.

4. **Arquitectura de la API**:
   - La API sigue una arquitectura en capas con:
     - **Modelos**: Clases que representan las tablas de la base de datos (Marca, Prenda, Venta) con relaciones definidas.
     - **Controladores**: Módulos que manejan la lógica de negocio y las rutas de la API.
     - **Base de Datos**: Un módulo (`base_datos.py`) para manejar operaciones de guardado y reversión.
   - Se utiliza programación orientada a objetos, con un modelo y controlador por tabla.
   - La API no incluye interfaz gráfica, cumpliendo con el requisito de ser una API pura (no MVC).
   - La estructura de carpetas es clara y organizada, siguiendo el modelo visto en clase.

5. **Base de Datos**:
   - Se utiliza SQLite con SQLAlchemy como ORM.
   - Las relaciones entre tablas (Marca-Prenda, Marca-Venta, Prenda-Venta) están correctamente definidas.
   - Se maneja el inventario de prendas automáticamente en las operaciones de venta (crear/actualizar resta del inventario, eliminar suma al inventario).

6. **Uso**:
   - Descomprimir el proyecto.
   - Seguir las instrucciones de configuración en `leeme.md` (crear entorno virtual, instalar dependencias, ejecutar la aplicación).
   - Probar los endpoints con Postman según las instrucciones proporcionadas.

---

# Notas Adicionales
- Los nombres de archivos, funciones y comentarios están completamente en español.
- Los endpoints utilizan nombres en español (`/marcas`, `/prendas`, `/ventas`, `/reportes`).
- La documentación (`leeme.md`) está en español y detalla cómo probar cada endpoint.
- Si necesitas que se genere un archivo ZIP con esta versión traducida o alguna modificación adicional (como agregar más comentarios en español), por favor indícalos.

¿Hay algo más específico que quieras que traduzca o ajuste en el proyecto?
