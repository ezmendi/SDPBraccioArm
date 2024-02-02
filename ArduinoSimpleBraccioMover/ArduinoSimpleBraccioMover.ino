
#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

#include <Braccio.h>
#include <Servo.h>

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    // Check if the command is a MOVE command
    if (data.startsWith("MOVE,")) {
      // Parse the command and move the Braccio arm
      moveArm(data);
    } else {
      Serial.print("You sent me: ");
      Serial.println(data);
    }
  }
}

void moveArm(String command) {
  // Parse the command for servo positions
  int pos[6];  // Array to hold positions for each servo
  int lastIndex = 4;  // Starting index to skip "MOVE,"
  for (int i = 0; i < 6; i++) {
    int index = command.indexOf(',', lastIndex + 1);
    pos[i] = command.substring(lastIndex + 1, index != -1 ? index : command.length()).toInt();
    lastIndex = index;
  }
  
  // Move the Braccio arm to the specified positions
  Braccio.ServoMovement(20, pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]);
  Serial.println("Movement executed");
}
