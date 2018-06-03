#!flask/bin/python
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import json
from flask import Flask, Response, render_template, request
from helloworld.flaskrun import flaskrun
import requests
import boto3 
from boto3.dynamodb.conditions import Key
from helloworld.setmetadata import db_set_item

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

@application.route('/new_visitor/<site>', methods=['POST'])
def get_temp(site):
    # get ip metadata from the fuction
    response = get_ip_meta()
    # get json data from the post body
    post_data = request.get_json()
    # build request data
    Item = build_request_data(site, post_data, response)
    db_set_item('eb_try_logger', Item)
    
    return Response(json.dumps(Item), mimetype='application/json', status=200)

@application.route('/bi', methods=['GET'])
def get_bi():
    my_ses = boto3.Session(region_name = 'us-east-1')
    dynamodb = my_ses.resource('dynamodb')
    table = dynamodb.Table('eb_try_logger')
    resp = table.scan()
    for item in resp['Items']:
        print(item)
    return Response(json.dumps(str(resp['Items'])), mimetype='application/json', status=200)
    #return render_template('index.html', response=json.dumps(resp['Items']), title='bi')

# get result for one site
@application.route('/bi/<db_key>/<db_value>', methods=['GET'])
def get_bi_site(db_key, db_value):
    my_ses = boto3.Session(region_name = 'us-east-1')
    dynamodb = my_ses.resource('dynamodb')
    table = dynamodb.Table('eb_try_logger')
    if db_key and db_value:
        resp = table.scan(FilterExpression=Key(db_key).eq(db_value))
    else:
        # when result not found, return table (presevent error handling in code...)
        resp = table.scan()

    for item in resp['Items']:
        print(item['site'])
    '''
    res = []
    res = json.loads(resp['Items'][0])
    '''
    #return Response(json.dumps(str(resp['Items'])), mimetype='application/json', status=200)
    #return render_template('index.html', response=json.dumps(resp['Items']), title='bi')
    return render_template('index.html', response=json.dumps(resp), title='bi')


@application.route('/bi/graph')
def showgraph():
    data_provider = [
        {
            'category': 'סחוג',
            'column-1': 8,
            'column-2': 5
        },
        {
            "category": "עמבה",
            "column-1": 6,
            "column-2": 7
        },
        {
            "category": "סחוג עם עמבה",
            "column-1": 2,
            "column-2": 3
        }
    ]
    return render_template('bi_graph.html', data=data_provider, chart_title='מה המצב אחי')

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
    res = requests.get(service_url).json()
    # arrange data so it won't be missing when entering dynamo
    if 'country' not in res:
        res['country'] = 'mock_country'
    if 'ip_geo' not in res:
        res['ip_geo'] = 'mock_geo'
    if 'loc' not in res:
        res['loc'] = 'mock_loc'
    if 'city' not in res:
        res['city'] = 'mock_city'
        
    return res

# build item for logger
# site is in the url
# post data contains the page in the site 
# response is for ip metadata
def build_request_data(site, post_data, response):
    Item={
    'ip_addr': response['ip'], 
    'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'time': datetime.datetime.now().strftime("%H:%M:%S"),
    'site': site,
    'ip_geo' : response['loc'], # res_data
    'ip_country': response['country'],
    'ip_city': response['city'],
    'page': post_data['page']
    }
    
    return Item

'''
def db_set_item(table, item):
        # create a session for boto to access the credentials that the ec2 holds
    my_ses = boto3.Session(region_name = 'us-east-1')
    # connect to the resource dynmodb using the session
    dynamodb = my_ses.resource('dynamodb')
    # refer to the table
    table = dynamodb.Table(table)

    print(item)
    # insert the item
    table.put_item(Item=item)
'''

if __name__ == '__main__':
    flaskrun(application)
