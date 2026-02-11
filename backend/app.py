"""
Основное Flack приложение для API учета товаров
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os

# Создаем Flask приложение
app = Flask(__name__)

#Включаем CORS для работы с фронтендом
CORS(app)

#Основной маршрут
@app.route('/')
def home():
    """Главная страница API"""
    return jsonify({
        'message': 'API системы учета товаров',
        'version': '1.0.0',
        'endpoint': {
            'GET /': 'Информация об API',
            'GET /health': "проверка состояния сервера"
        }
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "OK"}), 200

# Запуск приложения
if __name__ == '__main__':
    #Создаем папку для данных, если ее нет
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Создана папка 'data' ")

        print('=' * 40)
        print("Сервер запущен")
        print("Фронтенд: frontend/index.html")
        print('=' * 40)

        #Запускаем сервер
    app.run(debug=True, host='0.0.0.0', port=5000)

