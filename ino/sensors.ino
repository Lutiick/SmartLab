#include <SoftwareSerial.h>
#include <ESP8266WebServer.h>

const char* ssid = "shemo";
const char* password = "35353535";
float bar;
float hum;
float temp;
float temp_imu;
String data;
byte led_stat;
SoftwareSerial mySerial(D5, D6); // RX, TX

IPAddress ip(192, 168, 1, 50); 
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
ESP8266WebServer server(80);

float time;
time = 0;
bool timer() {
  if (millis() - time > 10000) {
    time = millis();
    return true;
  }
  else {
    return false;
  }
}

void main() {
  data = "temperature:"
  data += temp
  data += "\nhumidity:"
  data += hum
  data += "\npressure:"
  data += bar
  server.send(200, "text/plain", data)
}

void sensors() {
if (mySerial.available() > 0)
  {
    String filter = mySerial.readStringUntil('#');
    hum = mySerial.parseFloat();
    temp = mySerial.parseFloat();
    temp_imu = mySerial.parseFloat();
    bar = mySerial.parseFloat();
    mySerial.flush();
  }
}

void setup() {
  Serial.begin(9600);
  mySerial.begin(4800);
  delay(10);

  // prepare GPIO2
  pinMode(2, OUTPUT);
  digitalWrite(2, 0);
  
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.config(ip, gateway, subnet, gateway);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Start the server
  server.begin();
  server.on('/', main);
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());

}

void loop() {
  if (timer()) {
    sensors();
  }
  server.handleClient();
}
