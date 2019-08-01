/* you need to have mosquitto installed in your PC 
 *  
 *  On Linux : sudo apt-get upddate && sudo apt-get install mosquitto mosquitto-clients 
 */


/* import libs */

// ESP 8266 lib
#include <ESP8266WiFi.h>
// MQTT lib used 
#include <PubSubClient.h>
// Temperature/Humidity sensor 
#include "DHT.h" 

/* variables */
                   
//  sensor data connected to GPIO2: D4
#define DHTPIN 2 
// DHT11 sensor type
#define DHTTYPE DHT11
// see the flask app 
#define card_id  1  
// delay 
#define wait 5000

// Update these with values suitable for your network.
const char* ssid = "crepe et gaufre";
const char* password = "crepes@gaufres";

// your mqtt_server broker and topic to connect to  
const char* mqtt_server = "192.168.1.5";    // use ifconfig on Linux or ipconfig on Windows
const char* topic = "test"; 

// create objects, instances
DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;     // time last message was published
char msg[50];         // lenght of the message

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP()); // print the IP address of the ESP2866
}

// used to see the published messaged has arrived 
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  Serial.println("------------------------------------------------------------");Serial.println(); 
}

// check ESP266 and MQTT broker connections
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
  
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      // client.publish(topic, "NodeMCU connected");
      // ... and resubscribe
      client.subscribe(topic);
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  
  Serial.begin(115200);
  setup_wifi();
  // Init DHT
  dht.begin();
  client.setServer(mqtt_server, 1883);  //1883: MQTT defaut port 
  client.setCallback(callback); // for to see the response from the broker
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > wait) {  // delay 5000 
     lastMsg = now;
    // Reading temperature and humidity
    float h = dht.readHumidity();
    // Read temperature as Celsius
    float t = dht.readTemperature();
    
    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t) ) {
    Serial.println("Failed to read from DHT sensor!");
    return;
    }
  
    // Display data
    Serial.print("Humidity: ");
    Serial.print(h);
    Serial.print(" %\t");
    Serial.print("Temperature: ");
    Serial.print(t);
    Serial.println(" *C "); 
    
    snprintf (msg, 50, "%d %.2f %.f", card_id, t, h);  // to sytle the message to send exmp : "1 23.00 54"
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish(topic, msg);  /// publish the msg
  }
}
