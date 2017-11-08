# zabbix-ansible

Use "import.py" to pull Hosts out of Zabbix to create a Ansible Hosts File.
The script will pull all hosts assigned to a Host-Group (=ZABBIX_ANSIBLE_GRP) and create Groups in Ansible based on the other groups the host belongs to.

Example:
Host In Zabbix:

  Host-1:
      - AnsibleManaged (=ZABBIX_ANSIBLE_GRP)
      - DNS-Servers
      - NTP-Servers

Results in Ansible Hosts:

  [DNS-Server]
  Host-1

  [NTP-Server]
  Host-1



You can either use the python-script or the pre-packed Docker Container.

Usage:
docker run -it \
-v /mnt/server/infra/ansible/:/mnt/zabbix-ansible/ \
-e ZABBIX_IP='<IP of you Zabbix Server>' \
-e ZABBIX_USER='<Your username>' \
-e ZABBIX_PASSWORD='<Your password>' \
-e ZABBIX_ANSIBLE_GRP='<Host-Group to be checked>' \
-e UPDATE_RATE="60" \
dirkwoellhaf/zabbix-ansible:v0.9 \
python /coding/zabbix-ansible/import.py


docker service create \
  --name ZabbixAnsible \
  --replicas 2 \
  --restart-condition any \
  --restart-max-attempts 50 \
  --restart-delay 60s \
  --mount type=bind,src=/mnt/server/infra/ansible,dst=/mnt/zabbix-ansible \
  -e ZABBIX_IP="<IP of you Zabbix Server>" \
  -e ZABBIX_USER="<Your username>" \
  -e ZABBIX_PASSWORD='<Your password>' \
  -e ZABBIX_ANSIBLE_GRP='<Host-Group to be checked>' \
  -e UPDATE_RATE="60" \
  dirkwoellhaf/zabbix-ansible:v0.9 \
  python /coding/zabbix-ansible/import.py
