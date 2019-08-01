from flask_mqtt import Mqtt
from app import App,db
from app.models import Dht11, Gaz, Cards
import json
from flask_socketio import SocketIO
from flask import request
from flask_login import current_user

mqtt = Mqtt(App)
socketio = SocketIO(App)


# don't need it because, we have to subscribe and then ONLY read messages from card

"""""
@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'], data['qos'])
"""


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print(client, userdata, flags, rc)
    mqtt.subscribe('test')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    pay_int = []
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)
    pay = str(data['payload']).split()
    print('pay :', pay)
    #try:
     #   for nub in pay:
      #      if float(nub):
       #         pay_int.append(nub)

    card_id = pay[0]
    temp = pay[1]
    hum = pay[2]
    gaz = pay[3]
    print('card_id: ', card_id, 'temp:', temp, 'hum', hum)

    #print('REQUST --->', request.base_url)
    #current_user_cards = Cards.query.filtre_by()
    dht11 = Dht11(temperature=str(temp), humidity=str(hum), card_id=int(card_id))
    db.session.add(dht11)
    db.session.commit()

   # except ValueError:
      #  print('--> Please verify your data')



@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # print(level, buf)
    pass



