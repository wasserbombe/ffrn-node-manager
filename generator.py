# -*- coding: utf-8 -*-
import db as database
import json
import os
import configparser

config = configparser.ConfigParser()
config.read('settings.conf')
path_fastd = config['CONFIG']['fastd_path']
path_ffmap = config['CONFIG']['ffmap_path']

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

    def calcMAC(self, mac):
        mlist = mac.split(':')
        mlist = [int(x, 16) for x in mlist]
        mlist[0] += 0x02
        mlist[3] = ((mlist[3] + 1) % 0x100)
        return ':'.join([format(x , 'x') for x in mlist])

    def genJson(self):
        node_list = self.db.getNodeList()
        json = {}
        for node in node_list:
            temp = {}
            temp['name'] = node['hostname']
            if node['coords']:
                temp['gps'] = node['coords']
            json.update({self.calcMAC(node['mac'].lower()): temp})
        return json

    def genAliasJson(self):
        with open(os.path.abspath(os.path.join(path_ffmap, 'aliases.json')), 'w') as f:
            f.write(json.dumps(self.genJson(), sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ ==  "__main__":
    ffmap = FFmapConfig()
    ffmap.genAliasJson()
    fastd = FastdConfig()
    fastd.genFastdConf()
