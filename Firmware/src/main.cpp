#include <WiFi.h>
#include <PubSubClient.h>
#include "config.h"
#include <ArduinoJson.h>
#include "DHT.h"

DHT dht(DHT_PIN, DHT_TYPE);

WiFiClient espClient;
PubSubClient client(espClient);

void setup(){
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  client.setServer(MQTT_BROKER, MQTT_PORT);
  dht.begin();
}

unsigned long lastReconnectAttempt = 0;

bool reconnect(){
  if (!client.connected()) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt > 5000) {
      lastReconnectAttempt = now;
      Serial.println("Connecting to MQTT...");
      if(client.connect(CLIENT_ID)){
        Serial.println("Connected to MQTT");
        return true;
      }else{
        Serial.print("Failed rc=");
        Serial.println(client.state());
        return false;
      }
    }else{
      return false;
    }
  }else{
    return true;
  }
} 

unsigned long lastPublishAttempt = 0;

void readAndPublish(){
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  unsigned long now = millis();

  if(now - lastPublishAttempt > 5000){    
    lastPublishAttempt = now;
    JsonDocument doc;
    doc["humidity"] = humidity;
    doc["temperature"] = temperature;
    doc["device_id"] = DEVICE_ID;
    char jsonBuffer[200];
    serializeJson(doc, jsonBuffer);
    
    if(client.publish(MQTT_TOPIC, jsonBuffer)){
      Serial.println("Data published to MQTT");
    }else{
      Serial.println("Failed to publish data to MQTT");
    }
  }
}  


void loop(){
  if(reconnect()){
    readAndPublish();
  }
  client.loop();
}