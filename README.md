# What?
HomeAssistant integration of a GQ Electronics GMC500+ Geiger Muller Counter (GMC).  
May also work on other models from their [WiFi-enabled GMCs range](https://www.gqelectronicsllc.com/support/GMC_Selection_Guide.htm).  
 
# Why?
By design, GQ Electronics' WiFi-enabled Geiger counters are to be connected to the vendor's own global server, to provide a extensive mapping of [counters around the world](https://www.gmcmap.com/).  
The measurements are transmitted periodically as unsecured HTTP GET requests, with no prior authentication or even handshaking.  
The device allows customizing a few parameters of the HTTP requests, most notably the destination IP/hostname. As such, local data sampling is possible as a faster and more reliable solution - no dependency on Internet resources.  

# How?

## 1. Configure the device
The Geiger counter can be configured on-device, via the buttons and LCD screen, but an easier option is via the official software, [GQ GMC Data Viewer](http://www.gqelectronicsllc.com/downloads/download.asp?DownloadID=61).  
- (Optional) Update firmware by [requesting the latest version from the manufacturer](https://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=8895).  
- Connect to the PC is done via the mini-USB port - it will be enumerated as a CH340 USB-to-Serial device.  
- In the main software window, configure the device model (i.e. GMC-500) and COM port, then open the `Other` window via the `Settings` menu.  
- Input the WiFi access-point connection `SSID` and `Password`.  
- The device sends a request in a defined structure, for example `http://www.GMCmap.com/log2.asp?AID=0230111&GID=0034021&CPM=15&ACPM=13.2&uSV=0.075`. Some parts are configurable:  
	- Website: IP/hostname of the local server (in example `www.GMCmap.com`) - set it to local server IP address, eg. `192.168.0.2`,  
	- URL: request URL (in example `log2.asp`) - set to `gmc500`,  
	- User ID: relevant if using the global server solution (in example `0230111`) - set it to a numeric value, eg. `555`,  
	- Geiger Counter ID: relevant if using the global server solution (in example `0034021`) - set it to a numeric value, eg. `01234`,  
	- Period: time between requests, in minutes - set it to preferred value, eg. `1`.  
	
## 2. Configure the server/relay
Since the Python script relies on non-standard libraries, a [Home Assistant Docker installation](https://www.home-assistant.io/installation/linux#install-home-assistant-container) is assumed to be already working. Also, a MQTT broker (for example Mosquito) is also [installed](https://mosquitto.org/download), [configured](https://mosquitto.org/man/mosquitto-conf-5.html) and [accessible in HA](https://www.home-assistant.io/docs/mqtt/broker).  
As a alternative, a separate PC can also be used for interfacing to the GMC500.  
- Install the required python libraries: `sudo pip install Flask paho_mqtt gunicorn` ([why gunicorn?](https://flask.palletsprojects.com/en/2.0.x/deploying))
- Edit the [`private_config.json`](scripts/private_config.json) file by configuring the:
	- used MQTT broker (`HOSTNAME`, `USERNAME`, `PASSWORD`),  
	- user-specific values defined at step one (`USER_ID`, `DEV_ID`, `PERIOD`).  
- Run the [Python script](scripts/mqtt_gmc500.py) as root: `sudo gunicorn mqtt_gmc500:app -b 0.0.0.0:80`

## 3. Configure the HomeAssistant instance
User configuration is not necessary, as [MQTT auto-discovery](https://www.home-assistant.io/docs/mqtt/discovery/) is implemented.  

# Who/where/when?
All the reverse-engineering, development, integration, and documentation efforts are based on the latest software and hardware versions available at the time of writing (October 2022), and licensed under the GNU General Public License v3.0.
