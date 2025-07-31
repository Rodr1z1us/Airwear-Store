from flask import Blueprint, request, jsonify
from app.modelos.venta import Venta
from datetime import datetime

bp_ventas = Blueprint('ventas', __name__)

@bp_ventas.route('/', methods=['GET'])
def obtener_ventas():
    ventas = Venta.obtener_todos()
    return jsonify(ventas), 200

@bp_ventas.route('/<string:id>', methods=['GET'])
def obtener_venta(id):
    resultado, venta = Venta.obtener(id)
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == 0:
        return jsonify({"error": "Venta no encontrada"}), 404
    
    return jsonify(venta), 200

@bp_ventas.route('/', methods=['POST'])
def crear_venta():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400
    
    resultado, venta = Venta.crear(
        datos.get('prenda_id'),
        datos.get('marca_id'),
        datos.get('fecha', datetime.now().isoformat())
    )
    if resultado == -1:
        return jsonify({"error": "Prenda_id, marca_id y fecha son requeridos"}), 400
    if resultado == -2:
        return jsonify({"error": "ID de prenda o marca inválido"}), 400
    if resultado == -3:
        return jsonify({"error": "Prenda no encontrada"}), 404
    if resultado == -4:
        return jsonify({"error": "Marca no encontrada"}), 404
    
    return jsonify(venta), 201

@bp_ventas.route('/<string:id>', methods=['PUT'])
def actualizar_venta(id):
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400
    
    resultado, venta = Venta.actualizar(
        id,
        datos.get('prenda_id'),
        datos.get('marca_id'),
        datos.get('fecha', datetime.now().isoformat())
    )
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == -2:
        return jsonify({"error": "Prenda_id, marca_id y fecha son requeridos"}), 400
    if resultado == -3:
        return jsonify({"error": "ID de prenda o marca inválido"}), 400
    if resultado == -4:
        return jsonify({"error": "Prenda no encontrada"}), 404
    if resultado == -5:
        return jsonify({"error": "Marca no encontrada"}), 404
    if resultado == 0:
        return jsonify({"error": "Venta no encontrada"}), 404
    
    return jsonify(venta), 200

@bp_ventas.route('/<string:id>', methods=['DELETE'])
def eliminar_venta(id):
    resultado = Venta.eliminar(id)
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == 0:
        return jsonify({"error": "Venta no encontrada"}), 404
    
    return jsonify({"mensaje": "Venta eliminada"}), 200