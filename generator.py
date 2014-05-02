# -*- coding: utf-8 -*-
import db as database
import json
import os

path_ffmap = './'
path_fastd = './fastd/'

class FastdConfig(object):
    def __init__(self):
        self.db = database.DB()

    def genFastdConf(self):
        node_list = self.db.getNodeList()
        for node in node_list:
            with open(os.path.abspath(os.path.join(path_fastd, node['hostname'] + '.conf')), 'w') as f:
                conf = """\
#Hostname: {hostname}
#MAC: {mac}
#Koordinaten: {coords}
#Nick: {nickname}
#Mail: {email}
#Token: {token}
key "{key}";
""".format(**node)
                f.write(conf)

class FFmapConfig(object):
    def __init__(self):
        self.db = database.DB()

    def genJson(self):
        node_list = self.db.getNodeList()
        json = {}
        for node in node_list:
            temp = {}
            temp['name'] = node['hostname']
            if node['key']:
                temp['vpn'] = True
            if node['coords']:
                temp['gps'] = node['coords']
            json.update({node['mac']: temp})
        return json

    def genAliasJson(self):
        with open(os.path.abspath(os.path.join(path_ffmap, 'aliases.json')), 'w') as f:
            f.write(json.dumps(self.genJson(), sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ ==  "__main__":
    ffmap = FFmapConfig()
    ffmap.genAliasJson()
    fastd = FastdConfig()
    fastd.genFastdConf()
