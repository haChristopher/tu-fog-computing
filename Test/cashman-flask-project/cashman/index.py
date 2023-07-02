from flask import Flask, jsonify, request

app = Flask(__name__)

incomes = [{"description": "salary", "amount":5000}]





#endpoint 1 - GET
@app.route("/incomes")
def get_incomes():
    #convert py obj. into JSON
    return jsonify(incomes)

#endpoint 2 - POST
@app.route("/incomes", methods=["POST"])
def add_income():
    #extract the JSON payload and convert it into py obj. or list
    incomes.append(request.get_json())
    return '', 204