from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html')
    else:
        housing_age = int(request.form['housing_age'])
        total_rooms = int(request.form['total_rooms'])
        total_bedrooms = int(request.form['total_bedrooms'])
        households = int(request.form['households'])
        median_income = int(request.form['median_income'])
        ocean_proximity = request.form['ocean_proximity']
        h_ocean = 0
        inland = 0
        island = 0
        near_bay = 0
        near_ocean = 0
        if ocean_proximity == "<H OCEAN":
            h_ocean = 1
        elif ocean_proximity == "INLAND":
            inland = 1
        elif ocean_proximity == "ISLAND":
            island = 1
        elif ocean_proximity == "NEAR BAY":
            near_bay = 1
        elif ocean_proximity == "NEAR OCEAN":
            near_ocean = 1
        test_input = np.array([[housing_age, total_rooms, median_income, h_ocean, inland, island, near_bay, near_ocean, total_bedrooms / total_rooms, total_rooms / households]])
        with open('../model.pkl', 'rb') as file:
            data = pickle.load(file)
        
        regressor_loaded = data["model"]
        prediction = regressor_loaded.predict(test_input)
        return render_template("index.html", prediction_text = "The Predicted Housing Price is {}".format(prediction))
