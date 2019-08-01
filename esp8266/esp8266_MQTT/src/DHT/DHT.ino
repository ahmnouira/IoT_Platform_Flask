// Libraries
#include "DHT.h"

// Pin
#define DHTPIN 2  // GPIO2: D4 

// Use DHT11 sensor
#define DHTTYPE DHT11

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Start Serial
  Serial.begin(9600);
  // Init DHT
  dht.begin();
  }
  
void loop() {
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
  // Wait 2 seconds between measurements.
  delay(2000);
}
