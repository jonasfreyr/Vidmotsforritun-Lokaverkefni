#include<SPI.h>
#include <nRF24L01.h>
#include<RF24.h>


const byte address[6] = "00002";

RF24 radio(9, 10);

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);

  // Power amplitude level: minimum
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}

void loop() {
  // Ef að data er tilbúið (móttekið)
  if(radio.available()) {
    // Búa til tómann streng
    char text[32] = "";
    // Bæta við received data yfir í tóma strenginn
    radio.read(&text, sizeof(text));
    Serial.print(text);
  }
}
