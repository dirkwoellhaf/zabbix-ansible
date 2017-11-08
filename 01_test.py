#!/usr/bin/env python

import json
import requests
import os
import sys
import time
import getpass
import configparser

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ScriptVersion = "0.9"


def zabbix_login(zabbix_ip, zabbix_user, zabbix_password):
    # create credentials structure
    zabbix_data = '{"jsonrpc": "2.0", "method": "user.login", "params": {"user": "", "password": ""},"id": 1,"auth": null}'
    zabbix_data=json.loads(zabbix_data)
    zabbix_data["params"]["user"] = zabbix_user
    zabbix_data["params"]["password"] = zabbix_password

    # log in to API
    post_response = requests.post("http://"+str(zabbix_ip)+"/zabbix/api_jsonrpc.php", json=zabbix_data, verify=False)
    # get token from login response structure
    auth = json.loads(post_response.text)
    if auth['result']:
        print "Login successful: "+ auth['result']
        return auth['result']
    else:
        print "ERR"

def zabbix_GetGroup(zabbix_groups):
    #zabbix_data=json.loads(zabbix_groups)
    #print len(zabbix_groups)
    AnsibleGroup = "AnsibleManaged"
    count = 0
    while count < len(zabbix_groups):
        if zabbix_groups[count]['name'] != AnsibleGroup:
            zabbix_group = zabbix_groups[count]['name']
        count +=1

    return zabbix_group

def zabbix_GetHosts(zabbix_ip, zabbix_auth, zabbix_ansible_grp):

    # create credentials structure
    zabbix_data = '{"jsonrpc": "2.0", "method": "host.get", "params": {"selectGroups": "extend","selectInterfaces": "extend"}, "auth": "'+zabbix_auth+'", "id": 1}'
    zabbix_data=json.loads(zabbix_data)

    # log in to API
    post_response = requests.post("http://"+str(zabbix_ip)+"/zabbix/api_jsonrpc.php", json=zabbix_data, verify=False)

    #print post_response.text
    zabbix_data = json.loads(post_response.text)
    zabbix_hosts = len(zabbix_data['result'])
    print str(zabbix_hosts)+" Hosts found in Zabbix"
    hosts = {}
    hosts['hosts'] = zabbix_hosts
    zabbix_groups = []
    zabbix_hosts = []
    count = 0
    while count < len(zabbix_data['result']):
        if zabbix_ansible_grp in str(zabbix_data['result'][count]['groups']):
            host = zabbix_data['result'][count]['host']
            host_ip = zabbix_data['result'][count]['interfaces'][0]['ip']
            host_dns = zabbix_data['result'][count]['interfaces'][0]['dns']
            host_grp = zabbix_GetGroup(zabbix_data['result'][count]['groups']).replace(" ","")

            print host
            if zabbix_data['result'][count]['interfaces'][0]['useip'] == "0":
                print "  - DNS: " + host_dns
                host_connect=host_dns
            else:
                print "  - IP: " + host_ip
                host_connect=host_ip
            print "  - Grp: " + host_grp

            if host_grp not in zabbix_groups:
                zabbix_groups.append(host_grp)

            if host not in zabbix_hosts:
                zabbix_hosts.append(host_connect+"@"+host_grp)
        count +=1
    #return auth['result']
    #print zabbix_groups

    return zabbix_groups,zabbix_hosts

def CreateConfigFile(Config, zabbix_groups, zabbix_hosts):
    for group in zabbix_groups:
        Config.add_section(group)

    for host in zabbix_hosts:
        host=host.split("@")
        Config.set(host[1], host[0])

    return Config

#-------------------------------------------------


if __name__ == '__main__':
    zabbix_ip = os.environ['ZABBIX_IP']
    zabbix_user = os.environ['ZABBIX_USER']
    zabbix_password = os.environ['ZABBIX_PASSWORD']
    zabbix_ansible_grp = os.environ['ZABBIX_ANSIBLE_GRP']

    print ""
    print "Version: "+ScriptVersion
    print "ZABBIX IP: "+zabbix_ip
    print "ZABBIX USER: "+zabbix_user
    print "ANSIBLE-GRP: "+zabbix_ansible_grp

    Config = configparser.SafeConfigParser(allow_no_value=True)
    zabbix_auth = zabbix_login(zabbix_ip, zabbix_user, zabbix_password)
    zabbix_groups,zabbix_hosts = zabbix_GetHosts(zabbix_ip, zabbix_auth, zabbix_ansible_grp)
    Config = CreateConfigFile(Config, zabbix_groups,zabbix_hosts)

    with open('/mnt/zabbix-ansible/'+'hosts', 'wb') as configfile:
        Config.write(configfile)
