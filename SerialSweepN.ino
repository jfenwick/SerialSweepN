/*
  SerialSweepN
  Reads serial data until the null byte and turns that data into servo movement for n servos

  Note: Change numServos to number of servos and set servoPins to correct pins
*/
#include <Servo.h> 

const int numServos = 2;
Servo servos[numServos];
int servoPins[] = {9, 10};
char serialData[numServos * 3];
char tempData[3];

void setup() {
  Serial.begin(115200);
  Serial.println("Ready");
  for (int i=0; i < numServos; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(20);
  }
}

void loop() {
  if (Serial.available()) {
    Serial.readBytesUntil('\0', serialData, numServos * 3);
    
    for (int i=0; i < numServos; i++) {
      memmove(tempData, serialData + i * 3, 3);
      servos[i].write(atoi(tempData));
    }
  }
}
