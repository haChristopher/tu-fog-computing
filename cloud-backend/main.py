import os
from flask import Flask, jsonify, request
import pymongo
import config, certifi


url = f"mongodb+srv://{config.db_user}:{config.db_}@fog.m9hlcut.mongodb.net/?retryWrites=true&w=majority"
cluster = pymongo.MongoClient(url, tlsCAFile=certifi.where(), connect=False)
db = cluster['weather-storage'] 

# Creates the application and loads configuration from config.py or environment variables
# This is good for using docker
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    current_version = "v1"
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
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/api/<version>', methods=['POST'])
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

           




    ############ Error handling #############
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
