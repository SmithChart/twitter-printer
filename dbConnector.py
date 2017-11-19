#!/usr/bin/env python3
import os
import sqlite3
import time
import random
import hashlib
import unittest
import weakref
import os
import uuid
class WrongDbFileError(Exception):
    def __init__(self, message):
        self.message = message
class InvalidPubMethodError(Exception):
    def __init__(self, message):
        self.message = message
class DbConnector(object):
    def __init__(self,dbFile):
        self.conn = False
        self.dbFile = None
        random.seed()
        db_filename = dbFile 
        schema_filename = 'wurstDB.sql'
        db_is_new = not os.path.exists(db_filename)
        with sqlite3.connect(db_filename) as self.conn:
            if db_is_new:
                with open(schema_filename, 'rt') as f:
                    schema = f.read()
                    self.conn.executescript(schema)
                    self.conn.commit()
        self.dbFile = dbFile
    def close(self):
        if self.conn:
            self.conn.close() 
            self.conn = False
            self.dbFile = None

    def getEan(self,volume,pubMethod):
        dateCreate = int(time.time())
        c = self.conn.cursor()
        ean = ""
        for i in range(0,11):
            ean += str(random.randrange(0,10))
        c.execute("SELECT valid FROM pubMethod WHERE pubMethod = ?",[str(pubMethod)])
        valid = False
        for val in c.fetchall():
            val, = val
            if val == 1:
                valid = True
        if not valid:
            raise InvalidPubMethodError("%s is not a valid PubMethod"%pubMethod) 
        c.execute("INSERT INTO wurst(code, valid, used, dateGenerated, pubMethod) VALUES (?,?,?,?,?)",[str(ean),volume,0,dateCreate,str(pubMethod)])
        self.conn.commit()
        return ean 

    def getCode(self,volume,pubMethod):
        dateCreate = int(time.time())
        c = self.conn.cursor()
        m = hashlib.sha256()
        m.update(str(random.random()).encode())
        code = m.hexdigest()
        c.execute("SELECT valid FROM pubMethod WHERE pubMethod = ?",[str(pubMethod)])
        valid = False
        for val in c.fetchall():
            val, = val
            if val == 1:
                valid = True
        if not valid:
            raise InvalidPubMethodError("%s is not a valid PubMethod"%pubMethod) 
        c.execute("INSERT INTO wurst(code, valid, used, dateGenerated, pubMethod) VALUES (?,?,?,?,?)",[str(code),volume,0,dateCreate,str(pubMethod)])
        self.conn.commit()
        return code

    def useCode(self,code):
        dateUse = int(time.time())
        c = self.conn.cursor()
        c.execute("SELECT wurst.valid,used FROM  wurst INNER JOIN pubMethod ON pubMethod.pubMethod = wurst.pubMethod WHERE code == ? and used < wurst.valid and pubMethod.valid != 0",[str(code)])
        ret = False
        for row in c.fetchall():
            valid, used = row
            c.execute("UPDATE wurst SET used = used + 1, dateUsed = ? WHERE code == ? and used < valid",[dateUse,str(code)])
            ret = True
        self.conn.commit()
        return ret

    def addPubMethod(self,pubMethod):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO pubMethod(pubMethod) VALUES (?)",[str(pubMethod)])
        self.conn.commit()
        
    def blackList(self,pubMethod):
        c = self.conn.cursor()
        c.execute("UPDATE OR IGNORE pubMethod SET valid = 0 WHERE pubMethod == ?",[str(pubMethod)])
        self.conn.commit()
        
    def enablePubMethod(self,pubMethod):
        c = self.conn.cursor()
        c.execute("UPDATE OR IGNORE pubMethod SET valid = 1 WHERE pubMethod == ?",[str(pubMethod)])
        self.conn.commit()
        

class TestDbConnector(unittest.TestCase):
    def setUp(self):
        self.dbFileName = "/tmp/"+str(uuid.uuid4())

    def test_init(self): 
        db1 = DbConnector(self.dbFileName)
        self.assertIsNotNone(DbConnector(self.dbFileName), 'DB connection failed')
        db1.close()

    def test_close(self): 
        db2 = DbConnector(self.dbFileName)
        db2.close()
        self.assertEqual(db2.conn , False, 'DB connection is not closed')
            
    def test_getCode(self):
        db1 = DbConnector(self.dbFileName)
        db1.addPubMethod('test')
        db1.getCode(1,'test')
        with self.assertRaises(InvalidPubMethodError) as e:
            db1.getCode(1,'test3')
        db1.close()

    def test_getEan(self):
        db1 = DbConnector(self.dbFileName)
        db1.addPubMethod('test')
        print(db1.getEan(1,'test'))
        with self.assertRaises(InvalidPubMethodError) as e:
            db1.getCode(1,'test3')
        db1.close()

    def test_useCode(self):
        db1 = DbConnector(self.dbFileName)
        db1.addPubMethod('test')
        c = db1.getCode(2,'test')
        c2 = db1.getCode(1,'test')
        t = db1.useCode('1')
        self.assertEqual(t , False, 'did accept unknown code')
        t = db1.useCode(c)
        self.assertEqual(t , True, 'did not accept known code')
        t = db1.useCode(c)
        self.assertEqual(t , True, 'did accept volume of 2 only once')
        t = db1.useCode(c)
        self.assertEqual(t , False, 'did accept volume of 2 too often')
        t = db1.useCode(c2)
        self.assertEqual(t , True, 'code was affected by another code')
        db1.close()

    def test_blacklist(self):
        db1 = DbConnector(self.dbFileName)
        db1.addPubMethod('test')
        db1.addPubMethod('test2')
        c = db1.getCode(2,'test')
        c2 = db1.getCode(1,'test2')
        db1.blackList('test')
        t = db1.useCode(c)
        self.assertEqual(t , False, 'blacklisted pubMethods are accepted')
        t = db1.useCode(c2)
        self.assertEqual(t , True, 'not blacklisted pubMethods are not accepted')
        c = db1.conn.cursor()
        c.execute("UPDATE pubMethod SET valid = 1 WHERE pubMethod == ?",['test'])
        db1.conn.commit()
        db1.close()

    def tearDown(self):
        os.remove(self.dbFileName)

if __name__ == "__main__":
    unittest.main(verbosity=2)
