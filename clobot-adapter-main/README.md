# clobot-adapter
.env 설정
MQTT_BROKER_HOST=192.168.103.49  
MQTT_BROKER_PORT=1883  
MQTT_TOPIC_PREFIX=ce/v2/co-evolution/  
MQTT_KEEPALIVE=60  
MQTT_RETRY_INTERVAL=5  
TCP_SERVER_HOST=0.0.0.0  
TCP_SERVER_PORT=9999  

인스톨  
python 3.10 이상  
pip install -r requirements.txt  

adapter 실행  
python3 src/adapter.py  

rcs-sample 실행  
python3 rcs_sample/rcs.py  

로봇 접속  
ssh root@로봇ip -p 8022  
password root  

코드 업데이트 or 파일 업로드  
scp -P 8022 -r ./src root@로봇ip:/root/clobot  

scp -P 8022 -r ./map.json root@로봇ip:/root/clobot  
