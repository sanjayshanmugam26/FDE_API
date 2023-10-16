import requests
import json
import pymongo
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def get_and_increment_unique_id():
    try:
        with open('unique_id.txt', 'r') as file:
            current_id = int(file.read())
    except FileNotFoundError:
        current_id = 1  # Start from 1 if the file doesn't exist

    # Increment the ID and save it for the next request
    new_id = current_id + 1
    with open('unique_id.txt', 'w') as file:
        file.write(str(new_id))

    return str(new_id).zfill(10)

def register(request):
    AWS_S3_Path = request.POST['S3_Path']

    # Initialize the S3 and API Gateway URLs
    s3_path_url = 'https://id47qb8xk6.execute-api.us-east-1.amazonaws.com/dev/s3path'  # URL of your S3 path endpoint

    # Prepare the data to send in the POST request
    data = {
        'rawPath': AWS_S3_Path,
        'unique_id': get_and_increment_unique_id()
    }

    # Send the POST request to the API Gateway
    try:
        response = requests.post(s3_path_url, json=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            print("POST request succeeded:")
            # Print the JSON response with indentation
            result = json.dumps(response.json(), indent=2)
            print(json.dumps(response.json(), indent=2))


            # Store the JSON response in MongoDB
            client = pymongo.MongoClient("mongodb+srv://smartsanjaymani12:sanjay0000@cluster0.ywbzqjs.mongodb.net/")  # Mongodb Cluster localhost
            db = client["Form1099"]  # Mongodb database name
            collection = db["Data"]  # Mongodb Collection name
            collection.insert_one(response.json())

        else:
            print("POST request failed with status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("An error occurred:", str(e))

    return render(request, "result.html", {'AWS_S3_Path': result})
