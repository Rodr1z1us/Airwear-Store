## app/__init__.py
from flask import Flask
from pymongo import MongoClient
from config import Configuracion

mongo = None

def crear_app():
    global mongo
    app = Flask(__name__)
    app.config.from_object(Configuracion)
    
    mongo = MongoClient(app.config['MONGO_URI']).tienda_ropa
    
    from app.controladores.controlador_marcas import bp_marcas
    from app.controladores.controlador_prendas import bp_prendas
    from app.controladores.controlador_ventas import bp_ventas
    from app.controladores.controlador_reportes import bp_reportes
    
    app.register_blueprint(bp_marcas, url_prefix='/api/v1/marcas')
    app.register_blueprint(bp_prendas, url_prefix='/api/v1/prendas')
    app.register_blueprint(bp_ventas, url_prefix='/api/v1/ventas')
    app.register_blueprint(bp_reportes, url_prefix='/api/v1/reportes')
    
    return app