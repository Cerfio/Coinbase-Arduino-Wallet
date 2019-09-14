#include <ArduinoJson.h>
#include <Ethernet.h>
#include <SPI.h>

EthernetClient client;

void setup() {
  // Initialize Serial port
  Serial.begin(9600);
  while (!Serial)
    continue;
  // Initialize Ethernet library
  byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
  Serial.println(F("Started to configure Ethernet"));
  if (!Ethernet.begin(mac)) {
    Serial.println(F("Failed to configure Ethernet"));
    return;
  }
  // Connect to HTTP server
  //Serial.println(F("Connecting..."));
  //Serial.print("IP = ");
  //Serial.println(Ethernet.localIP());
  client.setTimeout(10000);
}

void request(byte index)
{
  //Serial.println(index);
  if (!client.connect("192.168.1.31", 5000)) {
    Serial.println(F("Connection failed"));
    return;
  }

  Serial.println(F("Connected!"));
  String myString = "GET /?index=";
  myString.concat(index);
  myString.concat(F(" HTTP/1.1"));
  client.println(myString);
  client.println(F("Host: arduinojson.org"));
  client.println(F("Connection: close"));
  if (client.println() == 0) {
    Serial.println(F("Failed to send request"));
    return;
  }
  delay(1000);
  // Check HTTP status
  char status[32] = {0};
  Serial.println(status);
  client.readBytesUntil('\r', status, sizeof(status));

  // Skip HTTP headers
  char endOfHeaders[] = "\r\n\r\n";
  if (!client.find(endOfHeaders)) {
    Serial.println(F("Invalid response"));
    //return;
  }

  // Allocate the JSON document
  // Use arduinojson.org/v6/assistant to compute the capacity.
  const size_t capacity = JSON_ARRAY_SIZE(3) + JSON_OBJECT_SIZE(1) + 3*JSON_OBJECT_SIZE(7) + 480;
  DynamicJsonDocument doc(capacity);

  // Parse JSON object
  DeserializationError error = deserializeJson(doc, client);
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }
  Serial.println(doc["jeton"][0]["name_jeton"].as<char*>());
  Serial.println(doc["jeton"][1]["name_jeton"].as<char*>());
  Serial.println(doc["jeton"][2]["name_jeton"].as<char*>());
  client.stop();
}

void loop() {
  for(byte i = 0; i != 15; i+=3) {
    request(i);
    delay(5000);
  }
  delay(10000); //Wait of 10secs
}
