#!usr/bin/env python
#-*-coding:utf-8-*-

import psycopg2 as _postgre


class PGConnector(object):

    def __init__(self, db_name = "", config = {}):
        if db_name:
            self._dataBase_name = db_name
        else:
            self._dataBase_name = "sigtel"
        if not config:
            self._config = {
                'database': 'TELESSAUDE_SG',
                'user':'postgres',
                'password' :'admin',
                'host' : 'localhost',
                'port':'5432'
                }
        else:
            self._config = config
        self._conn = None

    def getConnection(self):
        if self._conn == None:
            self._conn = _postgre.connect(**self._config)
        return self._conn

    def isConnect(self):
        if self._conn == None or self._conn.closed != 0:
            return False
        else:
            return True

    def closeConnection(self):
        if self._conn != None:
            self._conn.close()

    def executeQuery(self, query):
        cur = self.getConnection().cursor()
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result;

    def executeQueryOne(self, query):
        cur = self.getConnection().cursor()
        cur.execute(query)
        result = cur.fetchone()
        if not result:
            return None
        out = {}
        for idx, col in enumerate(cur.description):
            out[col.name] = result[idx]
        cur.close()
        return out;

    def execute(self, query,commit = False):
        # print query
        cur = self.getConnection().cursor()
        cur.execute(query)
        if commit:
            self.getConnection().commit()
        cur.close()

    def rollback(self):
        self.getConnection().rollback()

    def commit(self):
        self.getConnection().commit()

    def __del__(self):
        self.closeConnection();
        del self;
