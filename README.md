# IoT Platform developped using flask

This is an IoT platform developped using flask where people can veiw the temperature, humidity and gaz state 

## Video

[![iot_platform_flask](/images/dashboard.png)](/images/video.mp4) 

## Overview

Some photos about this project:
 
![dashboard](/images/dashboard.png)

![login](/images/login.png)

![regsiter](/images/register.png)

## Running this app

This app is designed to run in different ways:
1. As a standalone app running on your machine
1. As a Docker container running on your machine

## As a standalone app

1. install [python](https://www.python.org/)
2. `git clone` the project then `cd` into the directory
3. run `virtualenv -p /usr/bin/python3 venv`or `python -m venv venv` to create a virtual environment
4. activate it using `source venv/bin/activate`
5. `pip install -r requirements.txt` to install the app libaries and it dependencies

### setting up the databse 

1. you need to have [mysql server](https://www.mysql.com/) installed in your machine, if you are working in linux just typr ` sudo apt-get update && apt-get install mysql-server`
2. type `sudo mysql` to enter to the database
3. .....

#### run the app

After installing, run the server using `flask run`
Access the running app in a browser at the URL written to the console (most likely http://localhost:5000)

## As a Docker container running on your machine

1. install [Docker](https://www.docker.com/)
2. install [Docker compose toolset](https://docs.docker.com/compose/install/)
2. run `docker version` to check if docker is installed 
2. run `docker-compose --version` to check if docker-compose is installed
3. run `docker-compose up -d --build` to build the docker image of the flask app and mysql database
3. `docker images` list the local avaible images
4. go to http://localhost:8000 to start the container 

