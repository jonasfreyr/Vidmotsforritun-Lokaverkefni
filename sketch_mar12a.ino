int xPin = A0;
int yPin = A1;
const int button = 4;


int xPosition = 0;
int yPosition = 0;

int buttonState = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(xPin, INPUT);
  pinMode(yPin, INPUT);

  pinMode(button, INPUT);
  
  Serial.begin(9600);

  

}

void loop() {
  // put your main code here, to run repeatedly:
  xPosition = analogRead(xPin);
  yPosition = analogRead(yPin);

  buttonState = digitalRead(button);

  Serial.println(buttonState);
 
  
  //Serial.println(xPosition);
  //Serial.println(yPosition);

}
