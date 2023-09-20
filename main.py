from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route('/api/geolocation', methods=['POST'])
def obter_localizacao():
    dados = request.get_json()
    latitude = dados['latitude']
    longitude = dados['longitude']

    # Valida o formato dos dados enviados
    if valida_formato(latitude, longitude) is True:
        pass
    else:
        response = {
            'Erro': 'Você inseriu dados inválidos, insira apenas coordenadas numéricas.'
        }
        return jsonify(response), 400

    # Utiliza a função validar_dados para verificar a validade das coordenadas inseridas
    if not validar_dados(latitude, longitude):
        response = {
            'Erro': 'Você inseriu coordenadas inválidas.'
        }
        return jsonify(response), 400

    # Utiliza a API da OpenStreetMap para consultar a localização
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}'
    response_url = requests.get(url)
    data = response_url.json()

    # Extrai a cidade, estado e país do response
    endereco = data.get('address', {})
    cidade = endereco.get('city')
    estado = endereco.get('state')
    pais = endereco.get('country')

    response = {
        'cidade': cidade,
        'estado': estado,
        'pais': pais
    }

    return jsonify(response), 200

def valida_formato(latitude, longitude):
    try:
        float(latitude),
        float(longitude)

        return True

    except ValueError:

        return False

def validar_dados(latitude, longitude):
    if latitude is None or longitude is None:
        return False

    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return False

    return True

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))