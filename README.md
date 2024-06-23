# What?
HomeAssistant integration of a GQ Electronics GMC500+ Geiger Muller Counter (GMC).  
May also work on other models from their [WiFi-enabled GMCs range](https://www.gqelectronicsllc.com/support/GMC_Selection_Guide.htm).  
 
# Why?
By design, GQ Electronics' WiFi-enabled Geiger counters are to be connected to the vendor's own global server, to provide a extensive mapping of [counters around the world](https://www.gmcmap.com/).  
The measurements are transmitted periodically as unsecured HTTP GET requests, with no prior authentication or even handshaking.  
The device allows customizing a few parameters of the HTTP requests, most notably the destination IP/hostname. As such, local data sampling is possible as a faster and more reliable solution, given no dependency on Internet resources.  
There are two approaches in implementing the receiving (HTTP) server:  
- native, running directly on a [Home Assistant Docker installation](https://www.home-assistant.io/installation/linux#install-home-assistant-container), or on a separate device.  
- proxy, by means of a ESP32 used as a relay between the GMC500 and the HomeAssistant installation running [AppDaemon add-on](https://github.com/hassio-addons/addon-appdaemon). The external device is one method to circumvent Appdaemon's [limited](https://appdaemon.readthedocs.io/en/latest/APPGUIDE.html#restful-api-support) REST API, since it doesn't support `80` as its server port.  

# How?
## 1. Configure the device
The Geiger counter can be configured on-device, via the buttons and LCD screen, but an easier option is via the official software, [GQ GMC Data Viewer](http://www.gqelectronicsllc.com/downloads/download.asp?DownloadID=61).  
- (Optional) Update firmware by [requesting the latest version from the manufacturer](https://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=8895).  
- Connect to the PC is done via the mini-USB port - it will be enumerated as a CH340 USB-to-Serial device.  
- In the main software window, configure the device model (i.e. GMC-500) and COM port, then open the `Other` window via the `Settings` menu.  
- Input the WiFi access-point connection `SSID` and `Password`.  
- The device sends a request in a defined structure, for example `http://www.GMCmap.com/log2.asp?AID=0230111&GID=0034021&CPM=15&ACPM=13.2&uSV=0.075`. Some parts are configurable:  
	- Website: IP/hostname of the local server (in example `www.GMCmap.com`) - set it to local server/HomeAssistant IP address, eg. `192.168.0.2`,  
	- URL: request URL (in example `log2.asp`) - set to `gmc500` (native server) or `/api/appdaemon/gmc` (proxy server),  
	- User ID: relevant if using the global server solution (in example `0230111`) - set it to a numeric value, eg. `555`,  
	- Geiger Counter ID: relevant if using the global server solution (in example `0034021`) - set it to a numeric value, eg. `01234`,  
	- Period: time between requests, in minutes - set it to preferred value, eg. `1`.  
	
## 2. Configure the server/relay
### 2.1. Native server
- Install the required python libraries: `sudo pip install Flask paho_mqtt gunicorn` ([why gunicorn?](https://flask.palletsprojects.com/en/2.0.x/deploying))
- Edit the [`private_config.json`](scripts/private_config.json) file by configuring:
	- used MQTT broker (`HOSTNAME`, `USERNAME`, `PASSWORD`),  
	- user-specific values defined at step one (`USER_ID`, `DEV_ID`, `PERIOD`).  
- Run the [Python script](scripts/mqtt_gmc500_native.py) as root: `sudo gunicorn mqtt_gmc500_native:app -b 0.0.0.0:80`.  

### 2.2. Proxy server
- Edit the [`config.h`](appl/http_relay/config.h) file by configuring:
	- WiFi credentials (`WIFI_SSID`, `WIFI_PSWD`),  
	- AppDaemon IP address (same as HomeAssistant) and port (default 5050) (`HTTP_CLIENT_ADDR`),   
	- Optionally, enable the auto-reboot feature (as a workaround for WiFi sporadic issues, such as disconnects) by setting the reset period (`RESTART_TIMER_MSEC`). A value of `0` disables it.   
- Install the official [Arduino ESP32 package](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html), then build and flash the project.  
- Copy the [http_gmc500_appdaemon.py](scripts/mqtt_gmc500_appdaemon.py) file to the Appdaemon [app folder](https://github.com/hassio-addons/addon-appdaemon/blob/main/appdaemon/DOCS.md) (for eg. `/config/appdaemon/apps` in a Home Assistant OS installation).
- Modify the values inside the script as per the ones defined at step one (`USER_ID`, `DEV_ID`).  
- Add the new module to app list file `apps.yaml` (present in the same folder as above), by appending the following lines:  
```
mqtt_gmc500:
  module: mqtt_gmc500_appdaemon
  class: mqtt_gmc500
```
- Wait for Appdaemon to automatically reload the new module, or restart it manually. 

## 3. Configure the HomeAssistant instance
User configuration is not necessary, as [MQTT auto-discovery](https://www.home-assistant.io/docs/mqtt/discovery/) is implemented.  

# Who/where/when?
All the reverse-engineering, development, integration, and documentation efforts are based on the latest software and hardware versions available at the time of writing (June 2024), and licensed under the GNU General Public License v3.0.
