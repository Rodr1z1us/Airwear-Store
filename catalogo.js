
use tiendaRopaDB;


// USUARIOS--------------------------------------------------------------------------------------------------------------------


// Insertar 
db.usuarios.insertOne({
    username: "admin_ropa",
    email: "admin@airwear.com",
    password: "12345",
    rol: "admin",
    fecha_registro: new Date("2025-01-10")
  });

// Insertar varios
db.usuarios.insertMany([
  {
    username: "omar_birra",
    email: "juan@msn.com",
    password: "juanito123",
    rol: "cliente",
    fecha_registro: new Date("2025-02-20")
  },
  {
  username: "maria_garcia",
  email: "maria@msn.com",
  password: "claveSegura456",
  rol: "cliente",
  fecha_registro: new Date("2025-01-15")
}
]);


// Actualizar 
db.usuarios.updateOne(
  { username: "maria_garcia" },
  { $set: { email: "maria.nuevo@gmail.com" } }
);

// Eliminar 
db.usuarios.deleteOne({ username: "omar_birra" });


//PRENDAS--------------------------------------------------------------------------------------------------------------------


// Insertar 
db.prendas.insertOne({
  nombre: "Camiseta básica",
  marca: "AirWear",
  categoria: "Camisetas",
  precio: 19.99,
  tallas_disponibles: ["S", "M", "L"],
  colores: ["blanco", "negro"],
  stock: 50
});


// Insertar varias
db.prendas.insertMany([
  {
    nombre: "Jeans slim fit",
    marca: "AirWear",
    categoria: "Pantalones",
    precio: 59.99,
    tallas_disponibles: ["28", "30", "32", "34"],
    colores: ["azul", "negro"],
    stock: 30
  },
  {
    nombre: "Chaqueta de cuero",
    marca: "AirWear",
    categoria: "Abrigos",
    precio: 129.99,
    tallas_disponibles: ["S", "M", "L"],
    colores: ["negro", "marrón"],
    stock: 15
  },
  {
    nombre: "Vestido floral",
    marca: "AirWear",
    categoria: "Vestidos",
    precio: 39.99,
    tallas_disponibles: ["XS", "S", "M"],
    colores: ["rojo", "azul"],
    stock: 25
  }
]);

// Actualizar 
db.prendas.updateOne(
  { nombre: "Camiseta básica" },
  { $set: { precio: 22.99 } }
);

// Eliminar
db.prendas.deleteOne({ nombre: "Vestido floral" });


// VENTAS--------------------------------------------------------------------------------------------------------------------

// Insertar 
db.ventas.insertOne({
  prenda: { 
    nombre: "Jeans slim fit",
    marca: "AirWear"
  },
  fecha_venta: new Date("2025-05-10"),
  cantidad: 1,
  total: 59.99,
  usuario: { username: "maria_garcia" }
});

// Insertar varias
db.ventas.insertMany([
  {
    prenda: { 
      nombre: "Camiseta básica",
      marca: "AirWear"
    },
    fecha_venta: new Date("2025-05-10"),
    cantidad: 2,
    total: 45.98,
    usuario: { username: "maria_garcia" }
  },
  {
    prenda: { 
      nombre: "Chaqueta de cuero",
      marca: "AirWear"
    },
    fecha_venta: new Date("2025-05-11"),
    cantidad: 1,
    total: 129.99,
    usuario: { username: "admin_ropa" }
  },
  {
    prenda: { 
      nombre: "Jeans slim fit",
      marca: "AirWear"
    },
    fecha_venta: new Date("2025-05-12"),
    cantidad: 3,
    total: 179.97,
    usuario: { username: "maria_garcia" }
  },
  {
    prenda: { 
      nombre: "Camiseta básica",
      marca: "AirWear"
    },
    fecha_venta: new Date("2025-05-12"),
    cantidad: 1,
    total: 22.99,
    usuario: { username: "admin_ropa" }
  }
]);

// Actualizar 
db.ventas.updateOne(
  { "prenda.nombre": "Camiseta básica", cantidad: 2 },
  { $set: { total: 39.98 } }
);

// Eliminar
db.ventas.deleteOne({ "prenda.nombre": "Chaqueta de cuero" });
  

//-----------------------------------------------------------------------------------------------------------------------


//  Obtener la cantidad vendida de prendas por fecha 


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

//  marcas que tienen al menos una venta

db.ventas.aggregate([
  {
    $group: {
      _id: "$prenda.marca"
    }
  }
]);

//  prendas vendidas y su cantidad restante en stock

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

//  5 marcas más vendidas y su cantidad 

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