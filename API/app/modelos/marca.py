from bson import ObjectId
from app.base_datos import BaseDatos

class Marca:
    def __init__(self, nombre):
        self.nombre = nombre
        self._id = None

    def a_dict(self):
        resultado = {'nombre': self.nombre}
        if self._id:
            resultado['_id'] = str(self._id)
        return resultado

    @classmethod
    def desde_dict(cls, datos):
        marca = cls(datos['nombre'])
        if '_id' in datos:
            marca._id = str(datos['_id'])
        return marca

    @classmethod
    def obtener_todos(cls):
        coleccion = BaseDatos.obtener_coleccion('marcas')
        marcas = [cls.desde_dict(marca).a_dict() for marca in coleccion.find()]
        return marcas

    @classmethod
    def obtener(cls, id):
        try:
            object_id = ObjectId(id)
        except:
            return -1, None  # Invalid ID
        
        coleccion = BaseDatos.obtener_coleccion('marcas')
        marca = coleccion.find_one({'_id': object_id})
        if not marca:
            return 0, None  # Not found
        return 1, cls.desde_dict(marca).a_dict()

    @classmethod
    def crear(cls, nombre):
        if not nombre:
            return -1, None  # Missing nombre
        
        marca = cls(nombre)
        coleccion = BaseDatos.obtener_coleccion('marcas')
        resultado = coleccion.insert_one(marca.a_dict())
        marca._id = str(resultado.inserted_id)
        return 1, marca.a_dict()

    @classmethod
    def actualizar(cls, id, nombre):
        try:
            object_id = ObjectId(id)
        except:
            return -1, None  # Invalid ID
        
        if not nombre:
            return -2, None  # Missing nombre
        
        coleccion = BaseDatos.obtener_coleccion('marcas')
        resultado = coleccion.update_one(
            {'_id': object_id},
            {'$set': {'nombre': nombre}}
        )
        if resultado.matched_count == 0:
            return 0, None  # Not found
        
        marca = coleccion.find_one({'_id': object_id})
        return 1, cls.desde_dict(marca).a_dict()

    @classmethod
    def eliminar(cls, id):
        try:
            object_id = ObjectId(id)
        except:
            return -1  # Invalid ID
        
        coleccion = BaseDatos.obtener_coleccion('marcas')
        if (BaseDatos.obtener_coleccion('prendas').find_one({'marca_id': object_id}) or
            BaseDatos.obtener_coleccion('ventas').find_one({'marca_id': object_id})):
            return -2  # Associated with prendas or ventas
        
        resultado = coleccion.delete_one({'_id': object_id})
        return resultado.deleted_count