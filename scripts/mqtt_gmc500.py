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
            for value in ['CPM', 'ACPM', 'uSV']:
                publish.single('gmc500/values/' + value,
                               hostname=PRIVATE_CONFIG['MQTT']['HOSTNAME'], port=1883, client_id='gmc500',
                               auth={'username': PRIVATE_CONFIG['MQTT']['USERNAME'],
                                     'password': PRIVATE_CONFIG['MQTT']['PASSWORD']},
                               payload=float(request.args[value]))
    except Exception:
        logging.exception('EXCEPTION')
    finally:
        return "OK.ERR0", 200


if __name__ == '__main__':
    try:
        f = open('private_config.json')
        PRIVATE_CONFIG = json.load(f)
        f.close()
        if bool(PRIVATE_CONFIG['MQTT']) and bool(PRIVATE_CONFIG['GMC500']):
            pass
        GMC_USER_ID = PRIVATE_CONFIG['GMC500']['USER_ID']
        GMC_DEV_ID = PRIVATE_CONFIG['GMC500']['DEV_ID']
        app.run(port=HTTP_PORT, host='0.0.0.0')
    except Exception:
        logging.exception('EXCEPTION')
