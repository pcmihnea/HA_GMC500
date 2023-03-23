import mqttapi as mqtt
import json

GMC_USER_ID = '555'
GMC_DEV_ID = '01234'

class mqtt_gmc500(mqtt.Mqtt):
    def initialize(self):
        try:
            self.register_endpoint(self.http_gmc500, "gmc")
            for value in ['CPM', 'ACPM', 'uSV']:
                self.mqtt_publish('homeassistant/sensor/GMC500_' + value + '/config',
                            payload=json.dumps({
                                "name": 'GMC500_' + value,
                                "state_topic": 'homeassistant/sensor/GMC500/state',
                                "value_template": '{{ value_json.' + value + ' }}',
                                "icon": 'mdi:air-filter',
                                "state_class": 'measurement',
                                "unit_of_measurement": value,
                                "unique_id": GMC_USER_ID + GMC_DEV_ID + value,
                                "expire_after": 240}),
                            retain=True)
            self.log('Registered.')
        except Exception as e:
            self.log(e)