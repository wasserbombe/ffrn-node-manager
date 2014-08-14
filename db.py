# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
import sqlalchemy.exc
import tables

class DB(object):
    def __init__(self):
        Session = sessionmaker(bind=tables.engine)
        self.session = Session()

    def __row2dict(self, row):
        """transform sqlalchemy row proxy into an dict"""
        if not row:
            raise ValueError("None isn't a valid value")
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)
        return d

    def __dictlist(self, res):
        """transform table object into a list of dicts"""
        l = []
        for row in res:
            l.append(self.__row2dict(row))
        return l

    def addNode(self, node):
        try:
            self.session.add(tables.Nodes(**node))
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def getNode(self, token):
        try:
            return self.__row2dict(self.session.query(tables.Nodes).filter(tables.Nodes.token == token).one())
        except:
            raise

    def getNodeList(self):
        try:
            return self.__dictlist(self.session.query(tables.Nodes).all())
        except:
            raise

    def updateNode(self, node):
        try:
            self.session.query(tables.Nodes).filter(tables.Nodes.token == node['token']).update(node)
            self.session.commit()
        except:
            raise

    def __checkValue(self, column, value, token):
        if token:
            if self.session.query(tables.Nodes).filter(tables.Nodes.token != token).filter(column == value).first():
                return True
            else:
                return False
        else:
            if self.session.query(tables.Nodes).filter(column == value).first():
                return True
            else:
                return False

    def checkHostname(self, hostname, token):
        return self.__checkValue(tables.Nodes.hostname, hostname, token)

    def checkMAC(self, mac, token):
        return self.__checkValue(tables.Nodes.mac, mac, token)

    def checkKey(self, key, token):
        return self.__checkValue(tables.Nodes.key, key, token)

    def checkToken(self, token):
        if self.session.query(tables.Nodes).filter(tables.Nodes.token == token).first():
            return True
        else:
            return False

    def getNodeMailMap(self):
        return self.session.query(tables.Nodes.hostname, tables.Nodes.email).all()
