#!flask/bin/python
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

import json
from flask import Flask, Response, render_template, request
from helloworld.flaskrun import flaskrun
import requests

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


@application.route('/get_ip', methods=['GET'])
def get_ip():
    # print(get_ip_meta())
    return Response(json.dumps(get_ip_meta()), mimetype='application/json', status=200)


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
