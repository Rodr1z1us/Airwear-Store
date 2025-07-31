from app import mongo

class BaseDatos:
    @staticmethod
    def obtener_coleccion(nombre):
        return mongo[nombre]