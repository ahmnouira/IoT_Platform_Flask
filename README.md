# IoT Platform developped using flask
==============================================================================================
This is an IoT platform developped using flask where people can veiw the temperature, humidity and gaz state 

## Overview
==============================================================================================
Some photos about this project:
 
![login](/images/login.png)

![regsiter](/images/register.png)

![dashboard](/images/dashbaord.png)

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
1. you need to have [mysql](https://www.mysql.com/) server installed in your machine, if you are working in Linux just run 
    sudo apt-get update && apt-get install mysql-server
2. type `sudo mysql` to enter to the database
3. .....

#### run the app
After installing, run the server using
    flask run 

## As a Docker container running on your machine
1. install [Docker](https://www.docker.com/)
2. run `docker version` to check if docker is installed 
3. run `docker build -t iot_flask_platform .` to build the docker image
3. `docker images` list the local avaible images
4. `docker run --name iot_flask_platform -d -p 8000:5000 --rm iot_flask_platform` to start the container 

