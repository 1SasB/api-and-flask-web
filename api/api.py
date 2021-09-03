from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json

import ast

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_all_users():
    json_file = open('MOCK_DATA.json','r')
    mock_data = json.load(json_file)
    json_file.close()

    return {'data': mock_data}, 200  # return all users and 200 OK

@app.route('/users/<int:id>', methods=['GET'])
def get_a_users(id):
    json_file = open('MOCK_DATA.json')
    mock_data = json.load(json_file)
    for i in mock_data:
        if i['id'] == id:
            user = i

    return {"data": [user]}, 200  # return a user and 200 OK

@app.route('/users', methods=['POST'])
def post():
    parser = reqparse.RequestParser()
    request_data = request.get_json()

    json_file = open('MOCK_DATA.json', 'r+')
    mock_data = json.load(json_file)
    last_id = mock_data[-1]['id']
    request_data['id'] = last_id + 1

    mock_data.append(request_data)
    json_file.seek(0)

    json.dump(mock_data, json_file)
    json_file.close()

    return {'user': [request_data]}, 201

    
    

@app.route('/users/<int:id>', methods=['PATCH'])
def patch(id):
    update = request.get_json()
    update_keys = update.keys()
    json_file = open('MOCK_DATA.json', 'r+')
    mock_data = json.load(json_file)
    json_file.close()
    print("over")
    for i in mock_data:
        if i['id'] == id:
            print(i)
            for j in update_keys:
                i[j] = update[j] 

    json_file_a = open('MOCK_DATA.json', 'w')
    json.dump(mock_data,json_file_a)
    json_file_a.close()

    return {'user': [mock_data['id' == id]]}, 201

    # json.dump(user,json_file)
    # return {'user':user}

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_a_user(id):
    json_file = open('MOCK_DATA.json', 'r+')
    mock_data = json.load(json_file)
    json_file.close()
    print("over")
    new_json = []
    for i in mock_data:
        if not i['id'] == id:
            new_json.append(i)

    json_file_a = open('MOCK_DATA.json', 'w')
    json.dump(new_json, json_file_a)
    json_file_a.close()

    return {'user': [mock_data['id' == id]]}, 200




if __name__ == '__main__':
    app.run()  