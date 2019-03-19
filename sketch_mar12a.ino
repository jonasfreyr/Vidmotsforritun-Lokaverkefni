int xPin = A0;
int yPin = A1;

int xPosition = 0;
int yPosition = 0;



void setup() {
  // put your setup code here, to run once:
  pinMode(xPin, INPUT);
  pinMode(yPin, INPUT);

  Serial.begin(9600);

  

}

void loop() {
  // put your main code here, to run repeatedly:
  xPosition = analogRead(xPin);
  yPosition = analogRead(yPin);

  Serial.print(xPosition);
  Serial.print(yPosition);

}
