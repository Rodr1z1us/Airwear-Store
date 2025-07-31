from bson import ObjectId
from app.base_datos import BaseDatos

class Prenda:
    def __init__(self, nombre, marca_id, precio):
        self.nombre = nombre
        self.marca_id = marca_id
        self.precio = precio
        self._id = None

    def a_dict(self):
        resultado = {
            'nombre': self.nombre,
            'marca_id': ObjectId(self.marca_id) if self.marca_id else None,
            'precio': self.precio
        }
        if self._id:
            resultado['_id'] = str(self._id)
        return resultado

    @classmethod
    def desde_dict(cls, datos):
        prenda = cls(datos['nombre'], str(datos['marca_id']), datos['precio'])
        if '_id' in datos:
            prenda._id = str(datos['_id'])
        return prenda

    @classmethod
    def obtener_todos(cls):
        coleccion = BaseDatos.obtener_coleccion('prendas')
        prendas = [cls.desde_dict(prenda).a_dict() for prenda in coleccion.find()]
        return prendas

    @classmethod
    def obtener(cls, id):
        try:
            object_id = ObjectId(id)
        except:
            return -1, None  # Invalid ID
        
        coleccion = BaseDatos.obtener_coleccion('prendas')
        prenda = coleccion.find_one({'_id': object_id})
        if not prenda:
            return 0, None  # Not found
        return 1, cls.desde_dict(prenda).a_dict()

    @classmethod
    def crear(cls, nombre, marca_id, precio):
        if not nombre or not marca_id or not precio:
            return -1, None  # Missing required fields
        try:
            object_marca_id = ObjectId(marca_id)
        except:
            return -2, None  # Invalid marca_id
        
        # Check if marca exists
        if not BaseDatos.obtener_coleccion('marcas').find_one({'_id': object_marca_id}):
            return -3, None  # Marca not found
        
        prenda = cls(nombre, marca_id, precio)
        coleccion = BaseDatos.obtener_coleccion('prendas')
        resultado = coleccion.insert_one(prenda.a_dict())
        prenda._id = str(resultado.inserted_id)
        return 1, prenda.a_dict()

    @classmethod
    def actualizar(cls, id, nombre, marca_id, precio):
        try:
            object_id = ObjectId(id)
        except:
            return -1, None  # Invalid ID
        
        if not nombre or not marca_id or not precio:
            return -2, None  # Missing required fields
        try:
            object_marca_id = ObjectId(marca_id)
        except:
            return -3, None  # Invalid marca_id
        
        # Check if marca exists
        if not BaseDatos.obtener_coleccion('marcas').find_one({'_id': object_marca_id}):
            return -4, None  # Marca not found
        
        coleccion = BaseDatos.obtener_coleccion('prendas')
        resultado = coleccion.update_one(
            {'_id': object_id},
            {'$set': {
                'nombre': nombre,
                'marca_id': object_marca_id,
                'precio': precio
            }}
        )
        if resultado.matched_count == 0:
            return 0, None  # Not found
        
        prenda = coleccion.find_one({'_id': object_id})
        return 1, cls.desde_dict(prenda).a_dict()

    @classmethod
    def eliminar(cls, id):
        try:
            object_id = ObjectId(id)
        except:
            return -1  # Invalid ID
        
        coleccion = BaseDatos.obtener_coleccion('prendas')
        if BaseDatos.obtener_coleccion('ventas').find_one({'prenda_id': object_id}):
            return -2  # Associated with ventas
        
        resultado = coleccion.delete_one({'_id': object_id})
        return resultado.deleted_count