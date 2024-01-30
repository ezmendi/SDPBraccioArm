#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

void setup() {
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Braccio.begin();
}

void loop() {
   /*
   Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
   M1=base degrees. Allowed values from 0 to 180 degrees
   M2=shoulder degrees. Allowed values from 15 to 165 degrees
   M3=elbow degrees. Allowed values from 0 to 180 degrees
   M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
   M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
   M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the tongue is open, 73: the gripper is closed.
  */
  
                       //(step delay, M1, M2, M3, M4, M5, M6);
  Braccio.ServoMovement(5,           0,  90, 10, 90, 90,  10);  //STRETCHES STRAIGHT
  Braccio.ServoMovement(20,           0,  90, 10, 90, 90,  70);   //GRIPPER CLOSES
  Braccio.ServoMovement(20,           0,  90, 10, 90, 180,  70); // GRIPPER TWISTS
  Braccio.ServoMovement(20,           0,  90, 10, 90, 180,  70); // ARM BENDS AT ELBOW
  Braccio.ServoMovement(20,           180,  90, 10, 90, 90,  70); // BASE ROTATES
  Braccio.ServoMovement(20,           180,  90, 10, 90, 90,  10); // GRIPPER OPENS


  //Wait 1 second
  //delay(1000);

  //Braccio.ServoMovement(20,           180,  165, 0, 0, 180,  10);  

  //Wait 1 second
  //delay(1000);
}
