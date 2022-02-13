import json
import logging
import time

import paho.mqtt.publish as publish
from flask import Flask, request

MQTT_HOSTNAME = '192.168.0.2'
MQTT_USERNAME = '_USERNAME_'
MQTT_PASSWORD = '_PASSWORD_'
MQTT_CLIENT_ID = 'gmc500'

GMC_USER_ID = '555'
GMC_DEVICE_ID = '01234'
GMC_URL = 'gmc500'

TIMEOUT_SEC = 5

app = Flask(__name__)


@app.route('/' + GMC_URL, methods=['GET'])
def gmc500():
    try:
        if request.args['AID'] == GMC_USER_ID and request.args['GID'] == GMC_DEVICE_ID:
            publish.single(MQTT_CLIENT_ID + '/sensors/values',
                           payload=json.dumps(
                               {'CPM': float(request.args['CPM']), 'ACPM': float(request.args['ACPM']),
                                'uSV': float(request.args['uSV'])}),
                           hostname=MQTT_HOSTNAME,
                           port=1883, client_id=MQTT_CLIENT_ID,
                           auth={'username': MQTT_USERNAME, 'password': MQTT_PASSWORD})
    except Exception:
        pass
    finally:
        return "OK.ERR0", 200


if __name__ == '__main__':
    try:
        time.sleep(TIMEOUT_SEC)
        log = logging.getLogger('werkzeug')
        log.disabled = True
        app.run(port=80, host='0.0.0.0')
    except Exception:
        logging.exception('EXCEPTION')
