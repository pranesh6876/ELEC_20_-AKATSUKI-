#include<Servo.h>
Servo servo;        // number of steps the motor has taken
int Ready=0;          //this signal means that the laptop is ready to receive the stepper value
int stepCount=20;
void setup() {
  servo.attach(7);
  // initialize the serial port:6015055
  Serial.begin(250000);
  servo.write(0);
}

void loop() {
  // step one step:
  while(Ready==0){
    Ready=Serial.parseInt();
  }
Serial.print("1");
  stepCount+=10;
  servo.write(stepCount);
  delayMicroseconds(30);
  Serial.print("1");//for the temp variable
  Serial.println(stepCount);
  Ready=0;
}
