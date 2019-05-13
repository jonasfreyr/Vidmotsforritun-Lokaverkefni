#include<SPI.h>
#include <nRF24L01.h>
#include<RF24.h>

int xPin = 0;
int yPin = 1;
const int button = 4;

int xPosition = 0;
int yPosition = 0;
int buttonState = 0;

const byte address[6] = "00002";

RF24 radio(9, 10);

void setup() {
  Serial.begin(9600);

  pinMode(button, INPUT);
  digitalWrite(button, HIGH);
  
  radio.begin();
  radio.openWritingPipe(address);
  // Power amplitude level: minimum
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

void loop() {
  xPosition = analogRead(xPin);
  yPosition = analogRead(yPin);

  buttonState = digitalRead(button);

  
  // Búa til data til þess að senda
  char text[18];
  sprintf(text, "2, %i, %i, %i", xPosition, yPosition, buttonState);

  Serial.print(text);
  Serial.print("\n");
  
  // Senda data
  radio.write(&text, sizeof(text));
  // Bíða 1 sec þangað til sent er aftur
  delay(10);
}
