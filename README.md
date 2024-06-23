## To Install Python Dependencies

### Download PIP3 Dependencies
sudo apt-get install python-virtualenv
python3 -m venv .distribuidos-venv
source .distribuidos-venv/bin/activate
pip3 install -r requirements.txt
pip3 install pymongo
pip3 install kafka-python
pip3 install git+https://github.com/dpkp/kafka-python.git

### Start Prometheus (keep it running in a terminal)
tar -xvzf ./prometheus-2.53.0.linux-amd64.tar.gz
cp prometheus.yml ./prometheus-2.53.0.linux-amd64
cd ./prometheus-2.53.0.linux-amd64 && ./prometheus

### Start MongoDB (for linux)
sudo systemctl start mongod

### Start MongoDB (for macOS)
brew tap mongodb/brew
brew install mongodb-community@6.0
sudo brew services start mongodb/brew/mongodb-community@6.0
brew services list

### Load up MongoDB
mongosh < ./source/scripts/load_mongodb.js

### Enter Kafka's folder
tar -xvzf ./kafka_2.12-3.5.0.tgz
cd kafka_2.12-3.5.0

### Start Kafka Zookeeper (keep it running in a terminal)
./bin/zookeeper-server-start.sh config/zookeeper.properties

### Start Kafka Broker (keep it running in another terminal)
./bin/kafka-server-start.sh config/server.properties

### Create our topic (run this in a third terminal)
./bin/kafka-topics.sh --create --topic medication-request --bootstrap-server localhost:9092
