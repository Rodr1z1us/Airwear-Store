from flask import Blueprint, jsonify
from app.base_datos import BaseDatos
from bson.objectid import ObjectId
from app.modelos.marca import Marca
from app.modelos.prenda import Prenda
from app.modelos.venta import Venta

bp_reportes = Blueprint('reportes', __name__)

@bp_reportes.route('/marcas-con-ventas', methods=['GET'])
def marcas_con_ventas():
    coleccion_ventas = BaseDatos.obtener_coleccion('ventas')
    coleccion_marcas = BaseDatos.obtener_coleccion('prendas')
    marcas_ids = coleccion_ventas.distinct('marca')
    marcas = [coleccion_marcas.find_one({'_id': ObjectId(id)}) for id in marcas]
    return jsonify([Marca.desde_dict(marca).a_dict() for marca in marcas if marca])

@bp_reportes.route('/prendas-vendidas-con-inventario', methods=['GET'])
def prendas_vendidas_con_inventario():
    coleccion_ventas = BaseDatos.obtener_coleccion('ventas')
    coleccion_prendas = BaseDatos.obtener_coleccion('prendas')
    
    pipeline = [
        {"$group": {"_id": "$prenda_id", "total_vendido": {"$sum": "$cantidad"}}}
    ]
    ventas_agregadas = coleccion_ventas.aggregate(pipeline)
    
    resultados = []
    for venta in ventas_agregadas:
        prenda = coleccion_prendas.find_one({'_id': ObjectId(venta['_id'])})
        if prenda:
            resultados.append({
                'nombre': prenda['nombre'],
                'inventario': prenda['inventario'],
                'total_vendido': venta['total_vendido']
            })
    
    return jsonify(resultados)

@bp_reportes.route('/cinco-marcas-mas-vendidas', methods=['GET'])
def cinco_marcas_mas_vendidas():
    coleccion_ventas = BaseDatos.obtener_coleccion('ventas')
    coleccion_marcas = BaseDatos.obtener_coleccion('marcas')
    
    pipeline = [
        {"$group": {"_id": "$marca_id", "total_ventas": {"$sum": "$cantidad"}}},
        {"$sort": {"total_ventas": -1}},
        {"$limit": 5}
    ]
    ventas_agregadas = coleccion_ventas.aggregate(pipeline)
    
    resultados = []
    for venta in ventas_agregadas:
        marca = coleccion_marcas.find_one({'_id': ObjectId(venta['_id'])})
        if marca:
            resultados.append({
                'nombre': marca['nombre'],
                'total_ventas': venta['total_ventas']
            })
    
    return jsonify(resultados)