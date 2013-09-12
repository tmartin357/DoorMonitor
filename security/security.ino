/*
--------------------------------------------------------------------------
LICENCE
--------------------------------------------------------------------------
This security.ino is part of SPSUAUVDoorMonitor.

SPSUAUVDoorMonitor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SPSUAUVDoorMonitor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SPSUAUVDoorMonitor. If not, see http://www.gnu.org/licenses/.
--------------------------------------------------------------------------
*/

float tolerance = 0.02; //ammount closed can be under before it is considered open
float closedVoltage = 5.00;
boolean opened;
int led = 13;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  
  pinMode(led, OUTPUT); 
  
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * (5.0 / 1023.0);
  
  if(voltage < closedVoltage - tolerance) {//isOpen
    Serial.println(0);
    opened = true;
    digitalWrite(led, HIGH);
  } else {
    Serial.println(1);
    opened = false;
    digitalWrite(led, LOW);
  }
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * (5.0 / 1023.0);
  
  //Check Voltage
  boolean nowOpen = false;
  if(voltage < closedVoltage - tolerance) {//isOpen
    nowOpen = true;
  }
  
  if(opened != nowOpen) {//stateChange
    opened = nowOpen;
    if (nowOpen) {
      Serial.println(0);
      digitalWrite(led, HIGH);
    } else {
      Serial.println(1);
      digitalWrite(led, LOW);
    }
  }
}
