from bson import ObjectId
from app.base_datos import BaseDatos
from datetime import datetime

class Venta:
    def __init__(self, prenda_id, marca_id, fecha):
        self.prenda_id = prenda_id
        self.marca_id = marca_id
        self.fecha = fecha
        self._id = None

    def a_dict(self):
        resultado = {
            'prenda_id': ObjectId(self.prenda_id) if self.prenda_id else None,
            'marca_id': ObjectId(self.marca_id) if self.marca_id else None,
            'fecha': self.fecha
        }
        if self._id:
            resultado['_id'] = str(self._id)
        return resultado

    @classmethod
    def desde_dict(cls, datos):
        venta = cls(str(datos['prenda_id']), str(datos['marca_id']), datos['fecha'])
        if '_id' in datos:
            venta._id = str(datos['_id'])
        return venta

    @classmethod
    def obtener_todos(cls):
        coleccion = BaseDatos.obtener_coleccion('ventas')
        ventas = [cls.desde_dict(venta).a_dict() for venta in coleccion.find()]
        return ventas

    @classmethod
    def obtener(cls, id):
        try:
            object_id = ObjectId(id)
        except:
            return -1, None  # Invalid ID
        
        coleccion = BaseDatos.obtener_coleccion('ventas')
        venta = coleccion.find_one({'_id': object_id})
        if not venta:
            return 0, None  # Not found
        return 1, cls.desde_dict(venta).a_dict()

    @classmethod
    def crear(cls, prenda_id, marca_id, fecha):
        if not prenda_id or not marca_id or not fecha:
            return -1, None  # Missing required fields
        try:
            object_prenda_id = ObjectId(prenda_id)
            object_marca_id = ObjectId(marca_id)
        except:
            return -2, None  # Invalid prenda_id or marca_id
        
        # Check if prenda and marca exist
        if not BaseDatos.obtener_coleccion('prendas').find_one({'_id': object_prenda_id}):
            return -3, None  # Prenda not found
        if not BaseDatos.obtener_coleccion('marcas').find_one({'_id': object_marca_id}):
            return -4, None  # Marca not found
        
        venta = cls(prenda_id, marca_id, fecha)
        coleccion = BaseDatos.obtener_coleccion('ventas')
        resultado = coleccion.insert_one(venta.a_dict())
        venta._id = str(resultado.inserted_id)
        return 1, venta.a_dict()

    @classmethod
    def actualizar(cls, id, prenda_id, marca_id, fecha):
        try:
            object_id = ObjectId(id)
        except:
            return -1, None  # Invalid ID
        
        if not prenda_id or not marca_id or not fecha:
            return -2, None  # Missing required fields
        try:
            object_prenda_id = ObjectId(prenda_id)
            object_marca_id = ObjectId(marca_id)
        except:
            return -3, None  # Invalid prenda_id or marca_id
        
        # Check if prenda and marca exist
        if not BaseDatos.obtener_coleccion('prendas').find_one({'_id': object_prenda_id}):
            return -4, None  # Prenda not found
        if not BaseDatos.obtener_coleccion('marcas').find_one({'_id': object_marca_id}):
            return -5, None  # Marca not found
        
        coleccion = BaseDatos.obtener_coleccion('ventas')
        resultado = coleccion.update_one(
            {'_id': object_id},
            {'$set': {
                'prenda_id': object_prenda_id,
                'marca_id': object_marca_id,
                'fecha': fecha
            }}
        )
        if resultado.matched_count == 0:
            return 0, None  # Not found
        
        venta = coleccion.find_one({'_id': object_id})
        return 1, cls.desde_dict(venta).a_dict()

    @classmethod
    def eliminar(cls, id):
        try:
            object_id = ObjectId(id)
        except:
            return -1  # Invalid ID
        
        coleccion = BaseDatos.obtener_coleccion('ventas')
        resultado = coleccion.delete_one({'_id': object_id})
        return resultado.deleted_count