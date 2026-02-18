from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Reemplaza con tu API key de OpenWeatherMap
WEATHER_API_KEY = '45300b921bf415e803970f7a5936949b'

@app.route('/')
def index():
    return render_template('clima.html')

@app.route('/api/clima')
def obtener_clima():
    try:
        # 1. Obtener ubicación por IP
        ip_response = requests.get('https://ipwho.is/')
        ubicacion = ip_response.json()
        

        lat = ubicacion.get('latitude')
        lon = ubicacion.get('longitude')
        ciudad = ubicacion.get('city')
        
        # 2. Obtener clima de esa ubicación
        weather_url = f'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'es'
        }
        
        clima_response = requests.get(weather_url, params=params)
        clima = clima_response.json()
        
        resultado = {
            'ciudad': ciudad,
            'pais': ubicacion.get('country_name'),
            'temperatura': clima['main']['temp'],
            'descripcion': clima['weather'][0]['description'],
            'humedad': clima['main']['humidity'],
            'viento': clima['wind']['speed'],
            'icono': clima['weather'][0]['icon']
        }
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)