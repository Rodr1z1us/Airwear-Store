from flask import Blueprint, request, jsonify
from app.modelos.marca import Marca

bp_marcas = Blueprint('marcas', __name__)

@bp_marcas.route('/', methods=['GET'])
def obtener_marcas():
    marcas = Marca.obtener_todos()
    return jsonify(marcas), 200

@bp_marcas.route('/<string:id>', methods=['GET'])
def obtener_marca(id):
    resultado, marca = Marca.obtener(id)
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == 0:
        return jsonify({"error": "Marca no encontrada"}), 404
    
    return jsonify(marca), 200

@bp_marcas.route('/', methods=['POST'])
def crear_marca():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400
    
    resultado, marca = Marca.crear(datos.get('nombre'))
    if resultado == -1:
        return jsonify({"error": "El nombre es requerido"}), 400
    
    return jsonify(marca), 201

@bp_marcas.route('/<string:id>', methods=['PUT'])
def actualizar_marca(id):
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400
    
    resultado, marca = Marca.actualizar(id, datos.get('nombre'))
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == -2:
        return jsonify({"error": "El nombre es requerido"}), 400
    if resultado == 0:
        return jsonify({"error": "Marca no encontrada"}), 404
    
    return jsonify(marca), 200

@bp_marcas.route('/<string:id>', methods=['DELETE'])
def eliminar_marca(id):
    resultado = Marca.eliminar(id)
    if resultado == -1:
        return jsonify({"error": "ID inválido"}), 400
    if resultado == -2:
        return jsonify({"error": "No se puede eliminar la marca porque está asociada a prendas o ventas"}), 400
    if resultado == 0:
        return jsonify({"error": "Marca no encontrada"}), 404
    
    return jsonify({"mensaje": "Marca eliminada"}), 200