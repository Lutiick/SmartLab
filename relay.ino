#define SS_PIN D4  
#define RST_PIN D3 

#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WebServer.h>

const char* ssid = "shemo";
const char* password = "35353535";
IPAddress ip(192, 168, 1, 53); 
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

ESP8266WebServer server(80);
MFRC522 mfrc522(SS_PIN, RST_PIN);

boolean relay_stat = 0;
float current;
int pure_current_read;
float eps = 0.1 ;
float POWER; 
const int voltage = 220;
String CARD_ID;

void sendStatus() {
  String data = "";
  data += "relaystatus:";
  data += relay_stat;
  data += "\npower:";
  data += POWER;
  data += "\ncurrent:";
  data += current;
  data += "\nid:";
  data += CARD_ID;
  server.send(200, "text/plain", data);
}

int handleRFID() {
  if (! mfrc522.PICC_IsNewCardPresent()) {
    return 0;
  }
  if (! mfrc522.PICC_ReadCardSerial()) {
    return 0;
  }
  Serial.println();
  Serial.print(" UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  Serial.println();
  if (content.substring(1) == "86 4E C9 1F") {
    Serial.println(" Access Granted ");
    Serial.println(" Welcome Mr.Circuit ");
    delay(500);
    Serial.println(" Have FUN ");
    Serial.println();
    relay_stat = 1;
  }
  else {
    Serial.println(" Access Denied ");
    delay(500);
  }
  digitalWrite(D2, relay_stat);
}

void onRelay() {
  relay_stat = 1;
  digitalWrite(D2, relay_stat);
}

void offRelay() {
  relay_stat = 0;
  digitalWrite(D2, relay_stat);
}

void setup() 
{
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.begin(9600);

  pinMode(2, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(A0, INPUT);
  digitalWrite(2, 0);
  digitalWrite(D2, 0);

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
  server.on("/", sendStatus);
  server.on("/on", onRelay);
  server.on("/off", offRelay);
  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());
    delay(10);
}

void loop() {
  handleRFID();
  server.handleClient();
}
