import socket
from flask import Blueprint, jsonify, request

network_bp = Blueprint('network', __name__)

@network_bp.route('/network_name', methods=['GET'])
def get_network_name():
    try:
        # Obtiene el nombre del host y lo asocia con la dirección IP
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        print("AQUI ", socket.gethostbyaddr(host_ip))
        # Obtén el nombre de la red asociada con la dirección IP
        network_name = socket.gethostbyaddr(host_ip)[0]

        # Devuelve el nombre de la red en formato JSON
        return jsonify({'network_name': network_name})

    except Exception as e:
        return jsonify({'error': str(e)})