from flask import Blueprint, request, jsonify
from app.modelos.prenda import Prenda

bp_prendas = Blueprint('prendas', __name__)

@bp_prendas.route('/', methods=['GET'])
def obtener_prendas():
    prendas = Prenda.obtener_todos()
    return jsonify(prendas), 200

@bp_prendas.route('/<string:id>', methods=['GET'])
def obtener_prenda(id):
    resultado, prenda = Prenda.obtener(id)
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == 0:
        return jsonify({"error": "Prenda no encontrada"}), 404
    
    return jsonify(prenda), 200

@bp_prendas.route('/', methods=['POST'])
def crear_prenda():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400
    
    resultado, prenda = Prenda.crear(
        datos.get('nombre'),
        datos.get('marca_id'),
        datos.get('precio')
    )
    if resultado == -1:
        return jsonify({"error": "Nombre, marca_id y precio son requeridos"}), 400
    if resultado == -2:
        return jsonify({"error": "ID de marca inválido"}), 400
    if resultado == -3:
        return jsonify({"error": "Marca no encontrada"}), 404
    
    return jsonify(prenda), 201

@bp_prendas.route('/<string:id>', methods=['PUT'])
def actualizar_prenda(id):
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400
    
    resultado, prenda = Prenda.actualizar(
        id,
        datos.get('nombre'),
        datos.get('marca_id'),
        datos.get('precio')
    )
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == -2:
        return jsonify({"error": "Nombre, marca_id y precio son requeridos"}), 400
    if resultado == -3:
        return jsonify({"error": "ID de marca inválido"}), 400
    if resultado == -4:
        return jsonify({"error": "Marca no encontrada"}), 404
    if resultado == 0:
        return jsonify({"error": "Prenda no encontrada"}), 404
    
    return jsonify(prenda), 200

@bp_prendas.route('/<string:id>', methods=['DELETE'])
def eliminar_prenda(id):
    resultado = Prenda.eliminar(id)
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == -2:
        return jsonify({"error": "No se puede eliminar la prenda porque está asociada a ventas"}), 400
    if resultado == 0:
        return jsonify({"error": "Prenda no encontrada"}), 404
    
    return jsonify({"mensaje": "Prenda eliminada"}), 200