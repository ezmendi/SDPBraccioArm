import serial
import time
import math

shoulder_length = 13  # Example value, adjust according to your arm's dimensions
elbow_length = 23  # Example value, adjust according to your arm's dimensions

def calculate_angles(y, z, shoulder_length=shoulder_length, elbow_length=elbow_length):
    # Subtract 8cm from y to adjust for the joint being 8cm above the base
    y_adjusted = y - 8  # Adjust y to represent the distance from the joint

    # Calculate the shoulder angle
    shoulder_angle = math.acos(((y_adjusted**2 + z**2) + shoulder_length ** 2 - elbow_length ** 2) / (2 * math.sqrt(y_adjusted**2 + z**2) * shoulder_length)) + math.atan(y_adjusted/z)
    shoulder_angle = math.degrees(shoulder_angle) # Convert to degrees and adjust

    # Calculate the elbow angle
    elbow_angle = math.acos((shoulder_length**2 + elbow_length**2 - (y_adjusted**2 + z**2)) / (2 * elbow_length * shoulder_length))
    elbow_angle = math.degrees(elbow_angle) + shoulder_angle - 90 - math.degrees(math.atan(y_adjusted/z)) # Convert to degrees

    return shoulder_angle, elbow_angle


def send_command(ser, base_angle, y, z, wrist_angle, grip_angle):
    # Calculate the shoulder and elbow angles based on the given y and z
    shoulder_angle, elbow_angle = calculate_angles(y, z, shoulder_length, elbow_length)
    shoulder_angle = 180 - shoulder_angle
    # Construct the command string
    command = f"MOVE,{base_angle},{shoulder_angle},{elbow_angle},{wrist_angle},{90},{grip_angle}\n"
    print(f"Sending: {command}")
    ser.write(command.encode('utf-8'))
    response = ser.readline().decode('utf-8').rstrip()
    print("Arduino:", response)
    time.sleep(1)  # Add a short delay to ensure the arm has time to move

def main(y, z):
    ser = serial.Serial('COM6', 9600, timeout=1)
    time.sleep(2)  # Wait for the connection to establish

    # Example command with y and z coordinates
    send_command(ser, 0, y, z, 90, 90)  # YoSu will need to replace y, z, wrist_angle, and grip_angle with actual values
    time.sleep(5)

    ser.close()

if __name__ == '__main__':
    main()
