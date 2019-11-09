import requests
from flask import Flask, request, escape

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

# api-endpoint
from utils import cleanArrayAndConvertToFloat

base_url = "https://bigml.io/andromeda/"
big_auth = "?username=skurniawan&api_key=f6d118792a9143f8d8851c44c8931a26338d8951"
prediction_endpoint = "prediction"
dataset_endpoint = "dataset/5dc4ec3cf80b1640d7003584"
model_endpoint = "logisticregression/5dc4ed04f80b1640d7003587"

final_dataset_url = base_url + dataset_endpoint +  big_auth
final_prediction_url = base_url + prediction_endpoint +  big_auth

input_data_file = "input_file_2.csv"
normal_data_file = "normalization_data.csv"
biometrics_normal_data_file = "biometrics_normalization_data.csv"
with open(input_data_file) as f:
    content = f.readlines()

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
    player_data[x-1] = player_values

player_biometrics=[]
for x in range(6, 14):
    content_split = content[x].split(',')
    player_biometrics.append(float(content_split[1]))

r = requests.get(url=final_dataset_url)
data = r.json()
fields = data['fields']
fieldMapping= {}
for field, value in fields.items():
    fieldMapping[value['name']] = field



input_data_json = {}
for i in range(number_of_years):
    for j in range(number_of_attributes):
        field = fieldMapping[player_data_headers[j]+"_"+str(i+1)]
        input_data_json[field] = (player_data[i][j] - mean_data[j])/stddev_data[j]

i=0
for value in player_biometrics:
    normalized_value = (value - biometrics_mean_data[i])/biometrics_stddev_data[i]
    input_data_json[biometrics_key_values[i]] = normalized_value
    i=i+1


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
if response['prediction']['000002'] == '1':
    can = "HELL NO!!"
else: can = "HELL YEAH!!"
probability = response['probability']

print("Can the player be ALL-STAR? -->  %s" % can)
print("What is the Probability? --->  %f" % probability)


# extracting latitude, longitude and formatted address
# of the first matching location


