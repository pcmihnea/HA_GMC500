#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include "config.h"

#define HTTP_CLIENT_URI       ("/api/appdaemon/gmc")
#define HTTP_SERVER_URI       (HTTP_CLIENT_URI)
#define HTTP_SERVER_ARGS_MAX  (5)
#define HTTP_SERVER_CPM_POS   (2)
#define HTTP_SERVER_ACPM_POS  (3)
#define HTTP_SERVER_uSV_POS   (4)


WebServer server(80);
HTTPClient client;

String httpClientAddr = HTTP_CLIENT_ADDR;
String measValues[3] = {"", "", ""};
bool newValues = false;

void handleNotOK() {
  digitalWrite(LED_BUILTIN, HIGH);
  server.send(404, "text/plain", "NOK");
  digitalWrite(LED_BUILTIN, LOW);
}

void handleOK() {
  digitalWrite(LED_BUILTIN, HIGH);
  if ((server.method() == HTTP_GET) && (server.args() == HTTP_SERVER_ARGS_MAX)) {
    measValues[0] = server.arg(HTTP_SERVER_CPM_POS);
    measValues[1] = server.arg(HTTP_SERVER_ACPM_POS);
    measValues[2] = server.arg(HTTP_SERVER_uSV_POS);
    server.send(200, "text/plain", "OK.ERR0");
    newValues = true;
  }
  else {
    handleNotOK();
  }
  digitalWrite(LED_BUILTIN, LOW);
}

void setup(void) {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  httpClientAddr += HTTP_CLIENT_URI;
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PSWD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  while (!MDNS.begin("esp32")) {
    delay(500);
  }
  server.on(HTTP_SERVER_URI, handleOK);
  server.onNotFound(handleNotOK);
  server.begin();

  digitalWrite(LED_BUILTIN, LOW);
}

void loop(void) {
  server.handleClient();
  if (true == newValues) {
    digitalWrite(LED_BUILTIN, HIGH);
    client.begin(httpClientAddr + "?CPM=" + measValues[0] + "&ACPM=" + measValues[1] + "&uSV=" + measValues[2]);
    (void)client.GET();
    client.end();
    newValues = false;
    digitalWrite(LED_BUILTIN, LOW);
  }
  delay(2);
}
