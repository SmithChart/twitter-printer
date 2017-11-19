#!/usr/bin/env python3
import requests
import json
import unittest
class DbClientError(Exception):
    def __init__(self,message):
        self.message = message

class DbClient(object):
    def __init__(self,method,url):
        self.baseUrl = url
        self.method = method

    def getEan(self,volume):
        r = requests.put(self.baseUrl + '/ean', data = json.dumps({'method':self.method, 'volume':volume}))
        if 'ean' in r.json().keys():
            return r.json()['ean']
        elif 'error' in r.json().keys():
            raise DbClientError("Server says: %s"%(r.json()['error']))

    def getCode(self,volume):
        r = requests.put(self.baseUrl + '/code', data = json.dumps({'method':self.method, 'volume':volume}))
        if 'code' in r.json().keys():
            return r.json()['code']
        elif 'error' in r.json().keys():
            raise DbClientError("Server says: %s"%(r.json()['error']))
            

    def useCode(self,code):
        r = requests.get(self.baseUrl + '/code/'+code )
        if r.status_code == 200:
            return r.json()['valid']

    def addPubMethod(self,method):
        r = requests.put(self.baseUrl + '/method/'+method)

    def blackListPubMethod(self,method):
        r = requests.delete(self.baseUrl + '/method/'+method)

    def enablePubMethod(self,method):
        r = requests.post(self.baseUrl + '/method/'+method)

class TestDbClient(unittest.TestCase):
    def test_all(self):
        c = DbClient('test','http://127.0.0.1:5000') 
        c.addPubMethod('test')
        c.enablePubMethod('test')
        code = c.getCode(1)
        code2 = c.getCode(1)
        self.assertTrue(c.useCode(code), 'added code can not be used')
        c.blackListPubMethod('test')
        self.assertFalse(c.useCode(code2), 'backlisting does not work')
        with self.assertRaises(DbClientError) as e:
            code = c.getCode(1)
        c.enablePubMethod('test')
        self.assertTrue(c.useCode(code2), 'method enableing does not work')
        
    def test_ean(self):
        c = DbClient('test','http://127.0.0.1:5000') 
        c.addPubMethod('test')
        c.enablePubMethod('test')
        code = c.getEan(1)
        code2 = c.getEan(1)
        self.assertTrue(c.useCode(code), 'added code can not be used')
        c.blackListPubMethod('test')
        self.assertFalse(c.useCode(code2), 'backlisting does not work')
        with self.assertRaises(DbClientError) as e:
            code = c.getCode(1)
        c.enablePubMethod('test')
        self.assertTrue(c.useCode(code2), 'method enableing does not work')
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
