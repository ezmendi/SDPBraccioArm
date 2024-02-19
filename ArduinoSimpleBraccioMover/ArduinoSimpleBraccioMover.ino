
#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  Braccio.begin();    // Initialize Braccio with default stiffness
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read incoming data
    // Check if command starts with "MOVE"
    if (command.startsWith("MOVE,")) {
      moveArm(command); // Call moveArm with the command if it starts with "MOVE"
    } else {
      Serial.println(command); // Echo back the received data for other commands
    }
  }
}

void moveArm(String command) {
  // Print the received command for debugging
  Serial.println("Executing: " + command);

  // Example command: MOVE,90,45,0,0,0,0
  int pos[6]; // Array to hold positions for each servo
  int index = 0;
  int lastIndex = 4; // Correct starting index to skip "MOVE,"
  for (int i = 0; i < 6; i++) {
    index = command.indexOf(',', lastIndex + 1);
    if (index == -1 && i < 5) { // Ensure we break only if we're missing values before the last expected position
      Serial.println("Incomplete command received.");
      return; // Exit the function if no more values are found and we haven't filled the pos array
    }
    pos[i] = command.substring(lastIndex + 1, i < 5 ? index : command.length()).toInt();
    lastIndex = index;
  }

  Braccio.ServoMovement(20, pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]);
}
