# -*- coding: utf-8 -*-
import re
import os
import binascii
import db as database

class InputParser(object):
    regex = {
        'hostname': r'''^[-a-zA-Z0-9_]{1,32}$''',
        'key': r'''^([a-fA-F0-9]{64})?$''',
        'email': r'''^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$''',
        'nickname': r'''^[-a-zA-Z0-9_ äöüÄÖÜß]{1,64}$''',
        'mac': r'''^(([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2})$'''
    }

    regex_token = {'token': r'''^[a-f0-9]{30}$'''}

    def __init__(self):
        pass

    def getNodeRegex(self):
        return self.regex

    def getRecoveryRegex(self):
        return {'email': self.regex['email'], 'mac': self.regex['mac']}

    def getTokenRegex(self):
        return self.regex_token

    def getNodeWithTokenRegex(self):
        x = self.regex.copy()
        y = self.regex_token.copy()
        x.update(y)
        return x

    def __normalizeStrings(self, struct):
        return dict((k.lower(), v) for k, v in struct.items())

    def getData(self, req):
        res = self.__normalizeStrings(req.form.to_dict())
        return res

    def __validationError(self, vres):
        res = {}
        res['status'] = 'error'
        res['type'] = 'ValidationError'
        res['validationResult'] = vres
        return res

    def validate(self, regex, data):
        invalid = []
        missing = []
        unknown = []
        errors = False
        res = {}

        for key in regex.keys():
            if key not in data.keys():
                missing.append(key)
                errors = True

        for key in data.keys():
            value = data[key]
            if key not in regex.keys():
                unknown.append(key)
                errors = True
            elif not re.search(regex[key], value, re.IGNORECASE):
                invalid.append(key)
                errors = True

        res['invalid'] = invalid
        res['missing'] = missing
        res['unknown'] = unknown
        res['hasErrors'] = errors

        if errors:
            return self.__validationError(res)
        else:
            return None

class Token(object):
    db = database.DB()
    def getToken(self):
        return binascii.b2a_hex(os.urandom(15)).decode('utf-8')
    def checkToken(self, token):
        if self.db.checkToken(token):
            return None
        else:
            return {'status':'error','type':'NodeNotFoundError','token': token}

class Dedup(object):
    db = database.DB()
    def checkDups(self, hostname, mac, key, token):
        if self.db.checkHostname(hostname, token):
            return {'status':'error', 'type':'NodeEntryAlreadyExistsError','hostname': hostname}
        elif self.db.checkMAC(mac, token):
            return {'status':'error', 'type':'MacEntryAlreadyExistsError','mac': mac}
        elif self.db.checkKey(key, token):
            return {'status':'error', 'type':'KeyEntryAlreadyExistsError','key': key}
        else:
            return None

class Recover(object):
    db = database.DB()
    def checkCombination(self, email, mac):
        try:
            reg_data = self.db.getNodeMac(mac)
        except:
            return {'status':'error', 'type':'MacEntryDoesNotExistError', 'mac':mac }

        if reg_data:
            if reg_data['email'] == email:
                return None
            else:
                return {'status':'error', 'type':'EmailEntryDoesNotMatchError', 'email':email }
