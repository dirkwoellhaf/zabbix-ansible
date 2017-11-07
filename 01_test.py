#!/usr/bin/env python

import json
import requests
import sys
import time
import getpass
import configparser

def zabbix_login(zabbix_ip, zabbix_user, zabbix_password):
    # create credentials structure
    zabbix_data = '{"jsonrpc": "2.0", "method": "user.login", "params": {"user": "dwoellha", "password": "Devil123"},"id": 1,"auth": null}'
    zabbix_data=json.loads(zabbix_data)
    zabbix_data["params"]["user"] = zabbix_user
    zabbix_data["params"]["password"] = zabbix_password

    # log in to API
    post_response = requests.post("http://"+str(zabbix_ip)+"/zabbix/api_jsonrpc.php", json=zabbix_data, verify=False)
    # get token from login response structure
    auth = json.loads(post_response.text)

    return auth['result']

def zabbix_GetGroup(zabbix_groups):
    #zabbix_data=json.loads(zabbix_groups)
    #print len(zabbix_groups)
    count = 0
    while count < len(zabbix_groups):
        if zabbix_groups[count]['name'] != "AnsibleManaged":
            zabbix_group = zabbix_groups[count]['name']
        count +=1

    return zabbix_group

def zabbix_GetHosts(zabbix_ip, zabbix_auth):

    # create credentials structure
    zabbix_data = '{"jsonrpc": "2.0", "method": "host.get", "params": {"selectGroups": "extend","selectInterfaces": "extend"},"auth": "f64781e72a7536d2d17ae8befc6c699e","id": 1}'
    zabbix_data=json.loads(zabbix_data)

    #print zabbix_data

    zabbix_data["params"]["auth"] = zabbix_auth
    #print zabbix_data
    # log in to API
    post_response = requests.post("http://"+str(zabbix_ip)+"/zabbix/api_jsonrpc.php", json=zabbix_data, verify=False)

    #print post_response.text
    zabbix_data = json.loads(post_response.text)
    zabbix_hosts = len(zabbix_data['result'])
    print str(zabbix_hosts)+ " Hosts found in Zabbix to be managed by Ansible"
    hosts = {}
    hosts['hosts'] = zabbix_hosts
    count = 0
    while count < len(zabbix_data['result']):
        if "AnsibleManaged" in str(zabbix_data['result'][count]['groups']):
            print zabbix_data['result'][count]['host']
            print "  - IP: " + zabbix_data['result'][count]['interfaces'][0]['ip']
            print "  - Grp: " + zabbix_GetGroup(zabbix_data['result'][count]['groups'])
        count +=1
    #return auth['result']

#-------------------------------------------------


if __name__ == '__main__':
    config = configparser.ConfigParser()
    zabbix_auth = zabbix_login("10.1.17.46", "dwoellha", "Devil123")
    zabbix_GetHosts("10.1.17.46", zabbix_auth)
