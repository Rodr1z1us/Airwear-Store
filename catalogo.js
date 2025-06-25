// 📚 CRUD para Tienda de Ropa usando MongoDB

// ---------------------------------------------
// a. Creación de la base de datos
// ---------------------------------------------
use tiendaRopaDB;

// ---------------------------------------------
// Colección: usuarios
// ---------------------------------------------

// Insertar un usuario
db.usuarios.insertOne({
  username: "maria_garcia",
  email: "maria@example.com",
  password: "claveSegura456",
  rol: "cliente",
  fecha_registro: new Date("2025-01-15")
});

// Insertar varios usuarios
db.usuarios.insertMany([
  {
    username: "juan_perez",
    email: "juan@example.com",
    password: "juanito123",
    rol: "cliente",
    fecha_registro: new Date("2025-02-20")
  },
  {
    username: "admin_ropa",
    email: "admin@tiendaropa.com",
    password: "adminSecure2025",
    rol: "admin",
    fecha_registro: new Date("2025-01-10")
  }
]);

// Actualizar usuario
db.usuarios.updateOne(
  { username: "maria_garcia" },
  { $set: { email: "maria.nuevo@example.com" } }
);

// Eliminar usuario
db.usuarios.deleteOne({ username: "juan_perez" });

// ---------------------------------------------
// Colección: prendas
// ---------------------------------------------

// Insertar una prenda
db.prendas.insertOne({
  nombre: "Camiseta básica",
  marca: "Zara",
  categoria: "Camisetas",
  precio: 19.99,
  tallas_disponibles: ["S", "M", "L"],
  colores: ["blanco", "negro"],
  stock: 50
});

// Insertar varias prendas
db.prendas.insertMany([
  {
    nombre: "Jeans slim fit",
    marca: "Levi's",
    categoria: "Pantalones",
    precio: 59.99,
    tallas_disponibles: ["28", "30", "32", "34"],
    colores: ["azul", "negro"],
    stock: 30
  },
  {
    nombre: "Chaqueta de cuero",
    marca: "Guess",
    categoria: "Abrigos",
    precio: 129.99,
    tallas_disponibles: ["S", "M", "L"],
    colores: ["negro", "marrón"],
    stock: 15
  },
  {
    nombre: "Vestido floral",
    marca: "Mango",
    categoria: "Vestidos",
    precio: 39.99,
    tallas_disponibles: ["XS", "S", "M"],
    colores: ["rojo", "azul"],
    stock: 25
  }
]);

// Actualizar precio de una prenda
db.prendas.updateOne(
  { nombre: "Camiseta básica" },
  { $set: { precio: 22.99 } }
);

// Eliminar una prenda
db.prendas.deleteOne({ nombre: "Vestido floral" });

// ---------------------------------------------
// Colección: ventas
// ---------------------------------------------

// Insertar una venta
db.ventas.insertOne({
  prenda: { 
    nombre: "Jeans slim fit",
    marca: "Levi's"
  },
  fecha_venta: new Date("2025-05-10"),
  cantidad: 1,
  total: 59.99,
  usuario: { username: "maria_garcia" }
});

// Insertar varias ventas
db.ventas.insertMany([
  {
    prenda: { 
      nombre: "Camiseta básica",
      marca: "Zara"
    },
    fecha_venta: new Date("2025-05-10"),
    cantidad: 2,
    total: 45.98,
    usuario: { username: "maria_garcia" }
  },
  {
    prenda: { 
      nombre: "Chaqueta de cuero",
      marca: "Guess"
    },
    fecha_venta: new Date("2025-05-11"),
    cantidad: 1,
    total: 129.99,
    usuario: { username: "admin_ropa" }
  },
  {
    prenda: { 
      nombre: "Jeans slim fit",
      marca: "Levi's"
    },
    fecha_venta: new Date("2025-05-12"),
    cantidad: 3,
    total: 179.97,
    usuario: { username: "maria_garcia" }
  },
  {
    prenda: { 
      nombre: "Camiseta básica",
      marca: "Zara"
    },
    fecha_venta: new Date("2025-05-12"),
    cantidad: 1,
    total: 22.99,
    usuario: { username: "admin_ropa" }
  }
]);

// Actualizar total de una venta
db.ventas.updateOne(
  { "prenda.nombre": "Camiseta básica", cantidad: 2 },
  { $set: { total: 39.98 } }
);

// Eliminar una venta
db.ventas.deleteOne({ "prenda.nombre": "Chaqueta de cuero" });

// ---------------------------------------------
// c. Consultas
// ---------------------------------------------

// i. Obtener la cantidad vendida de prendas por fecha y filtrarla con una fecha específica
// Esta consulta agrupa las ventas por fecha y suma la cantidad de prendas vendidas para una fecha específica
db.ventas.aggregate([
  {
    $match: {
      fecha_venta: {
        $eq: new Date("2025-05-10") // Fecha específica a filtrar
      }
    }
  },
  {
    $group: {
      _id: "$fecha_venta",
      total_prendas_vendidas: { $sum: "$cantidad" }
    }
  }
]);

// ii. Obtener la lista de todas las marcas que tienen al menos una venta
// Esta consulta obtiene las marcas únicas que aparecen en las ventas
db.ventas.aggregate([
  {
    $group: {
      _id: "$prenda.marca"
    }
  }
]);

// iii. Obtener prendas vendidas y su cantidad restante en stock
// Esta consulta relaciona las ventas con las prendas para mostrar cuántas unidades se han vendido y cuántas quedan en stock
db.ventas.aggregate([
  {
    $lookup: {
      from: "prendas",
      localField: "prenda.nombre",
      foreignField: "nombre",
      as: "info_prenda"
    }
  },
  { $unwind: "$info_prenda" },
  {
    $group: {
      _id: "$prenda.nombre",
      marca: { $first: "$prenda.marca" },
      total_vendido: { $sum: "$cantidad" },
      stock_actual: { $first: "$info_prenda.stock" }
    }
  },
  {
    $project: {
      _id: 0,
      prenda: "$_id",
      marca: 1,
      unidades_vendidas: "$total_vendido",
      stock_restante: "$stock_actual"
    }
  }
]);

// iv. Obtener listado de las 5 marcas más vendidas y su cantidad de ventas
// Esta consulta agrupa las ventas por marca, suma la cantidad vendida y las ordena de mayor a menor, limitando a 5 resultados
db.ventas.aggregate([
  {
    $group: {
      _id: "$prenda.marca",
      total_vendido: { $sum: "$cantidad" }
    }
  },
  {
    $sort: { total_vendido: -1 }
  },
  {
    $limit: 5
  },
  {
    $project: {
      _id: 0,
      marca: "$_id",
      cantidad_vendida: "$total_vendido"
    }
  }
]);