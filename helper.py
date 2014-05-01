import re

class InputParser(object):
    regex = {
        'hostname': '/^[-a-zA-Z0-9_]{1,32}$/',
        'key': '/^([a-fA-F0-9]{64})?$/',
        'email': '''/^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$/''',
        'nickname': '/^[-a-zA-Z0-9_ äöüÄÖÜß]{1,64}$/',
        'mac': '/^([a-fA-F0-9]{12}|([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2})$/',
        'coords': '/^(-?[0-9]{1,3}(\.[0-9]{1,15})? -?[0-9]{1,3}(\.[0-9]{1,15})?)?$/'
    }

    def __init__(self):
        pass

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

    def validate(self, req):
        invalid = []
        missing = []
        unknown = []
        errors = False
        res = {}
        data = self.getData(req)

        for key in self.regex.keys():
            if not data[key]:
                missing.append(key)
                errors = True

        for key in data.keys():
            value = data[key].replace(" ", "")
            if key not in self.regex.keys():
                unknown.append(key)
                errors = True
            elif not re.search(self.regex[key], value, re.MULTILINE):
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
