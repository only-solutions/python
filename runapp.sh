#!/usr/bin/bash
#Open Terminal 
#First build and deploy the front end in Docker:

if [ ! -d public-html ]
then
  echo Go to directory containing public-html first
  read a
fi
#shutdown any existing docker instance and restart
sudo /etc/init.d/apache2 stop
sudo docker stop clientapp
sudo docker rm clientapp
sudo docker rm clientapp
sudo docker build -t my-apache2 .
sudo docker run -dit --name clientapp -p 8080:80 my-apache2

#Docker should now be running in the background

#Run REST server

echo
echo
echo
echo
echo
echo Instructions:
echo Open web browser and open front end
echo http://localhost:8080

echo Enter a word in the "tags" field
echo Click Browse... and select a picture to upload
echo Click Submit

echo Verify file was uploaded and JSON database was updated:
echo \(from main directory\)
echo cat mydb.json
echo ls public-html/uploads/storage/box
echo \(uploaded file should be listed\)

echo
echo
echo Starting REST server:
cd server
python3 serverstore.py 
