# zabbix-ansible



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
