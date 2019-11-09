import csv
import io

import sys
from collections import OrderedDict
from imp import reload

reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from flask import Flask, escape, request, jsonify


from utils import cleanArrayAndConvertToFloat, getRandomJoke

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/backcourt/allstar/v1", methods=['POST'])
def do_something():
    base_url = "https://bigml.io/andromeda/"
    big_auth = "?username=skurniawan&api_key=f6d118792a9143f8d8851c44c8931a26338d8951"
    prediction_endpoint = "prediction"
    dataset_endpoint = "dataset/5dc4ec3cf80b1640d7003584"
    model_endpoint = "logisticregression/5dc4bc5e5e269e31f6004544"

    final_dataset_url = base_url + dataset_endpoint + big_auth
    final_prediction_url = base_url + prediction_endpoint + big_auth


    file = request.files['input']


    input_data_file = "input_file_2.csv"
    normal_data_file = "normalization_data.csv"
    biometrics_normal_data_file = "biometrics_normalization_data.csv"

    content = file.readlines()

    with open(normal_data_file) as f:
        normal_content = f.readlines()

    with open(biometrics_normal_data_file) as f:
        biometrics_normal_content = f.readlines()

    number_of_attributes = 12
    number_of_years = 4
    player_data = [[0.0 for x in range(number_of_attributes)] for y in range(number_of_years)]
    player_data_headers = content[0].split(',')
    player_data_headers.pop(0)
    player_data_headers[-1] = player_data_headers[-1].strip()

    mean_data = cleanArrayAndConvertToFloat(normal_content[1].split((',')))
    stddev_data = cleanArrayAndConvertToFloat(normal_content[2].split((',')))
    biometrics_key_values = biometrics_normal_content[0].split((','))
    biometrics_key_values.pop(0)
    biometrics_key_values[-1] = biometrics_key_values[-1].strip()
    biometrics_mean_data = cleanArrayAndConvertToFloat(biometrics_normal_content[1].split((',')))
    biometrics_stddev_data = cleanArrayAndConvertToFloat(biometrics_normal_content[2].split((',')))

    for x in range(1, 5):
        player_values = cleanArrayAndConvertToFloat(content[x].split(','))
        player_data[x - 1] = player_values

    player_biometrics = []
    for x in range(6, 14):
        content_split = content[x].split(',')
        player_biometrics.append(float(content_split[1]))

    r = requests.get(url=final_dataset_url)
    data = r.json()
    fields = data['fields']
    fieldMapping = {}
    for field, value in fields.items():
        fieldMapping[value['name']] = field

    input_data_json = {}
    for i in range(number_of_years):
        for j in range(number_of_attributes):
            field = fieldMapping[player_data_headers[j] + "_" + str(i + 1)]
            input_data_json[field] = (player_data[i][j] - mean_data[j]) / stddev_data[j]

    i = 0
    for value in player_biometrics:
        normalized_value = (value - biometrics_mean_data[i]) / biometrics_stddev_data[i]
        input_data_json[biometrics_key_values[i]] = normalized_value
        i = i + 1

    # defining a params dict for the parameters to be sent to the API

    # sending get request and saving the response as response object

    # data to be sent to api
    request_json = {}
    request_json['model'] = model_endpoint
    request_json['input_data'] = input_data_json

    # sending post request and saving response as response object
    r = requests.post(url=final_prediction_url, json=request_json)

    # extracting response text
    response = r.json();

    can = ""
    mvp_possibility = 0
    if response['prediction']['000002'] == '1':
        can = "HELL YEAH!!"
        mvp_possibility = 1
    else:
        can = "HELL NO!!"

    probability = response['probability']

    response = OrderedDict()

    res = "Can the player be ALL-STAR? -->  "+can+" |  What is the Probability? --->  " +  str(probability)
    response["Response_string"] = res
    response["MVP_Possibility"] = mvp_possibility
    response["Probability"] = probability
    response["Joke"] = getRandomJoke()

    return jsonify(response)


if __name__ == "__main__":
    app.run(port=5000,debug=True)