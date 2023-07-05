import os
from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient
import config
import certifi
from flask_swagger import swagger
from flask_cors import CORS

url = f"mongodb+srv://{config.db_user}:{config.db_}@fog.m9hlcut.mongodb.net/?retryWrites=true&w=majority"
cluster: MongoClient = pymongo.MongoClient(url, tlsCAFile=certifi.where(), connect=False)
db = cluster['weather-storage'] 

# Creates the application and loads configuration from config.py or environment variables
# This is good for using docker
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # allows the react App (dashbors to fetch data from the flask app)
    cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    current_version = "v2"
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass




################################ Main routes ################################
    @app.route('/api/<version>/submit', methods=['POST'])
    def submit_data(version):
        if str(version).lower() != current_version:
            return jsonify({'error': 'Version not supported yet'}), 400
        else:
            try:
                if not request.is_json:
                    return jsonify({'error': 'Invalid JSON'}), 400

                # Get the JSON data from the request
                data = request.get_json()

                # Define the required fields
                required_fields = ['lat', 'lon', 'timezone', 'sunrise_unix', 'sunset_unix', 'temp', 'pressure',
                                   'humidity', 'wind_speed', 'weather_naming', 'timestamp']

                # Create a dictionary from the JSON data
                doc = {field: data[field] for field in required_fields}

                # Validate the required fields
                if any(value is None for value in doc.values()):
                    raise ValueError("Missing required fields")

            
                # send data to MongoDB
                collection = db['weather']
                if collection.insert_one(doc).acknowledged:
                    return jsonify({'message': 'success'}), 201
                else:
                    raise Exception("Error inserting data")

            except ValueError as e:
                print(f"Error: {str(e)}")
                return jsonify({'error': 'Data error'}), 500

            except Exception as e:
                # Handle server errors and exceptions
                print(e)
                return jsonify({'error': str(e)}), 500

           
    @app.route('/api/<version>/get_single', methods=['GET'])
    def get_data(version):
        if str(version).lower() != current_version:
            return jsonify({'error': 'Version not supported yet'}), 400
        else:
            # check if city exists
            city = request.args.get('city')
            if city is None:
                error_message = {'error': 'City parameter is missing'}
                return jsonify(error_message), 400
            else:
                # find city results in db 
                collection = db['weather_v3']
                city_data = collection.find({'city': city}).sort('time_of_measurement', -1).limit(10)
                results = []
                for data in city_data:
                    results.append({
                        'city': data['city'],
                        'country': data['country'],
                        'time_of_measurement': data['time_of_measurement'],
                        'temperature' : data["temperature"],
                        'pressure': data['pressure'],
                        'humidity': data['humidity'],
                        'wind_speed': data['wind_speed'],
                        'weather_naming': data['weather_naming'],
                        'timestamp_request': data['timestamp_request']
                    })
                  
                if len(results) == 0:
                    error_message = {'message': f'No data found for {city}'}
                    return jsonify(error_message), 404
                return jsonify(results)
                
    @app.route('/api/<version>/get_all', methods=['GET'])
    def get_all(version):
        if str(version).lower() != current_version:
            return jsonify({'error': 'Version not supported yet'}), 400
        else:
            # find city results in db 
            collection = db['weather_v3']
            # Get distinct city names
            distinct_cities = collection.distinct('city')

            # cities = ["Hamburg", "Berlin", "München"]
            results = []
            for city in distinct_cities:
                res = collection.find({'city': city}).sort('time_of_measurement', -1).limit(10)
                for data in res:
                    results.append({
                        'city': city,
                        'country': data['country'],
                        'time_of_measurement': data['time_of_measurement'],
                        'temperature' : data["temperature"],
                        'pressure': data['pressure'],
                        'humidity': data['humidity'],
                        'wind_speed': data['wind_speed'],
                        'weather_naming': data['weather_naming'],
                        'timestamp_request': data['timestamp_request']
                    })
                    if len(results) == 0:
                        error_message = {'message': f'No data found for {city}'}
                        return jsonify(error_message), 404
            return jsonify(results)


    ############ Error handling  + Additional #############
    @app.route("/spec")
    def spec():
        return jsonify(swagger(app))
    

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found :('}), 404
    

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
