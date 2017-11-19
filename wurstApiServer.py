#!/usr/bin/env python3
from flask import Flask , request, jsonify, redirect, url_for, send_from_directory
from dbConnector import DbConnector, InvalidPubMethodError
import json
api = Flask(__name__)

@api.route('/ean', methods=['PUT'])
def getEan():
    dbConn = DbConnector('wurst.db')
    attr = json.loads(request.data.decode())
    try:
        ean = dbConn.getCode(attr['volume'],attr['method'])
        ret = {'ean':ean}
    except InvalidPubMethodError as e:
        ret = {'error':e.message}
    dbConn.close()
    return json.dumps(ret)

@api.route('/code', methods=['PUT'])
def getCode():
    dbConn = DbConnector('wurst.db')
    attr = json.loads(request.data.decode())
    try:
        code = dbConn.getCode(attr['volume'],attr['method'])
        ret = {'code':code}
    except InvalidPubMethodError as e:
        ret = {'error':e.message}
    dbConn.close()
    return json.dumps(ret)

@api.route('/code/<code>', methods=['GET'])
def useCode(code):
    dbConn = DbConnector('wurst.db')
    valid = dbConn.useCode(code)
    dbConn.close()
    return json.dumps({'valid':valid})

@api.route('/method/<method>', methods=['post','put','delete'])
def methodStuff(method):
    dbConn = DbConnector('wurst.db')
    if request.method == 'PUT': 
        dbConn.addPubMethod(method)
        return ''
    if request.method == 'POST': 
        dbConn.enablePubMethod(method)
        return ''
    if request.method == 'DELETE':
        dbConn.blackList(method)
        return ''

    dbConn.close()


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000,debug=False)
