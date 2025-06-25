# Airwear-Store

Este proyecto consiste en la creación de una API con MongoDB para una tienda de ropa, junto con un frontend que permite la gestión de usuarios, prendas y ventas. El sistema completo ofrece operaciones básicas como inserción, actualización, eliminación y consultas avanzadas a través de una interfaz web.

**Usuarios**

{
  username: "ligia_bravo",
  email: "libra@msn.com",
  password: "clave123",
  rol: "cliente",
  fecha_registro: new Date("2025-01-15")
}

**Prendas**

{
  nombre: "Camiseta básica",
  marca: "AirWear",
  categoria: "Camisetas",
  precio: 19.99,
  tallas_disponibles: ["S", "M", "L"],
  colores: ["blanco", "negro"],
  stock: 50
}

**Ventas**

{
  prenda: { 
    nombre: "camiseta basica",
    marca: "AirWear"
  },
  fecha_venta: new Date("2025-05-10"),
  cantidad: 1,
  total: 59.99,
  usuario: { username: "maria_garcia" }
}
