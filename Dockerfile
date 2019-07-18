
FROM python:3.5-alpine

COPY app app 
COPY migrations migrations
COPY main.py boot.sh ./
COPY requirements.txt requirements.txt 


# RUN python -m venv venv 
# RUN source venv/bin/activate
RUN pip install -r requirements.txt 
RUN pip install gunicorn --user
RUN pip install pymysql --user
ENV FLASK_APP main.py

# runtime configuration 
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

