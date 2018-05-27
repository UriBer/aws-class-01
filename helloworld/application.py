#!flask/bin/python
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import json
from flask import Flask, Response, render_template, request
from helloworld.flaskrun import flaskrun
import requests

import boto3
import datetime

application = Flask(__name__, template_folder='templates')

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


@application.route('/get_ip', methods=['GET'])
def get_ip():
    # print(get_ip_meta())
    # return time and path to url to database
    return Response(json.dumps(get_ip_meta()), mimetype='application/json', status=200)

@application.route('/temp/<temp>', methods=['GET'])
def get_temp(temp):

    response = get_ip_meta()
    my_ses = boto3.Session(region_name = 'us-east-1')
    dynamodb = my_ses.resource('dynamodb')
    table = dynamodb.Table('eb_try_logger')

    item={
    'ip_addr': str(response), 
    'path': temp,
    'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'time': datetime.datetime.now().strftime("%H:%M:%S"),
    'ip_meta' : response, # res_data
    'name':'chilkibilki'
    }
    
    print(item)
    table.put_item(Item=item)
    return Response(json.dumps(item), mimetype='application/json', status=200)

@application.route('/bi', methods=['GET'])
def get_bi():
    my_ses = boto3.Session(region_name = 'us-east-1')
    dynamodb = my_ses.resource('dynamodb')
    table = dynamodb.Table('eb_try_logger')
    resp = table.scan()

    #return Response(json.dumps(str(resp)), mimetype='application/json', status=200)
    return render_template('index.html', response=str(resp), title='bi')

@application.route('/new/<param>', methods=['GET'])
def get_param(param):
    return render_template('index.html', name=ret_meta_ip(), options=options())


@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


def options():
    my_list = ["one", "two"]
    #my_dict = {'a' : 'addd','b' : 'dddd','c' :'llll'}
    return my_list


def get_ip_meta():
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://ipinfo.io/{}'.format(user_ip) 
    
    return requests.get(service_url).json()


if __name__ == '__main__':
    flaskrun(application)
