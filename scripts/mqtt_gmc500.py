import json
import logging

import paho.mqtt.publish as publish
from flask import Flask, request

HTTP_PORT = 80

app = Flask(__name__)

PRIVATE_CONFIG = {}
GMC_USER_ID = ''
GMC_DEV_ID = ''


@app.route('/gmc500', methods=['GET'])
def gmc500():
    try:
        if request.args['AID'] == GMC_USER_ID and request.args['GID'] == GMC_DEV_ID:
            mqtt_publish('homeassistant/sensor/GMC500/state',
                         {'CPM': float(request.args['CPM']), 'ACPM': float(request.args['ACPM']),
                          'uSV': float(request.args['uSV'])},
                         False)
    except Exception:
        logging.exception('REQUEST')
    return "OK.ERR0", 200


def mqtt_publish(topic, payload, retain):
    try:
        publish.single(hostname=PRIVATE_CONFIG['MQTT']['HOSTNAME'], port=1883, client_id='gmc500',
                       auth={'username': PRIVATE_CONFIG['MQTT']['USERNAME'],
                             'password': PRIVATE_CONFIG['MQTT']['PASSWORD']},
                       topic=topic, payload=json.dumps(payload), retain=retain)
    except Exception:
        logging.exception('MQTT_PUBLISH')


if __name__ == '__main__':
    try:
        logging.info('INIT')
        f = open('private_config.json')
        PRIVATE_CONFIG = json.load(f)
        f.close()
        if bool(PRIVATE_CONFIG['MQTT']) and bool(PRIVATE_CONFIG['GMC500']):
            pass
        GMC_USER_ID = PRIVATE_CONFIG['GMC500']['USER_ID']
        GMC_DEV_ID = PRIVATE_CONFIG['GMC500']['DEV_ID']
        SAMPLE_INTERVAL = PRIVATE_CONFIG['GMC500']['PERIOD'] * 60
        for value in ['CPM', 'ACPM', 'uSV']:
            mqtt_publish('homeassistant/sensor/GMC500_' + value + '/config',
                         {"name": 'GMC500_' + value,
                          "state_topic": 'homeassistant/sensor/GMC500/state',
                          "value_template": '{{ value_json.' + value + ' }}',
                          "device_class": 'aqi', "unit_of_measurement": value,
                          "unique_id": GMC_USER_ID + GMC_USER_ID + value,
                          "expire_after": SAMPLE_INTERVAL * 2},
                         True)
        logging.info('LOOP')
        app.run(port=HTTP_PORT, host='0.0.0.0')
    except Exception:
        logging.exception('MAIN')
