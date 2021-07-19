install packages:

sudo snap install docker
sudo apt install apache2
sudo apt install net-tools
sudo apt install python3-venv
sudo apt install python3-pip
sudo pip install Flask
sudo pip install flask_restful
sudo pip install flask_cors

Edit paths in REST backend server application:
server/serverstore.py
UPLOAD_FOLDER = '/home/here/github/python/public-html/uploads'
JSON_DB = '/home/here/github/python/mydb.json'
DB_BACKUP = '/home/here/github/python/backups'

run script:
chmod a+rx ./runapp.sh
./runapp.sh

Open another terminal to run "interleaving" test program which uses individual consumer and producer processes:  multiproc2.py
./runapp2.sh
