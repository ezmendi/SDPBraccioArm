#!/usr/bin/env python3
import serial
import time

# Function to send a move command to the Arduino
def send_move_command(ser, command):
    ser.write((command + "\n").encode())
    print(f"Sent: {command}")
    response = ser.readline().decode('utf-8').rstrip()
    print(f"Arduino: {response}")
    time.sleep(2)  # Wait for the Braccio to move

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    
    # Example command to move the Braccio arm
    move_command = "MOVE,90,45,180,90,90,10"  # Adjust values as needed
    
    # Send the move command to the Arduino
    send_move_command(ser, move_command)
    
    # Optionally, add more move commands or logic as needed
