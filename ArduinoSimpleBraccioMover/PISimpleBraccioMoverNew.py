import serial
import time

def send_command(ser, command):
    print(f"Sending: {command}")
    ser.write(command.encode('utf-8'))
    response = ser.readline().decode('utf-8').rstrip()
    print("Arduino:", response)
    time.sleep(1)  # Add a short delay to ensure the arm has time to move

if __name__ == '__main__':
    ser = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)  # Wait for the connection to establish

    # Send five distinct MOVE commands to the Braccio arm
    send_command(ser, "MOVE,0,90,10,90,90,10\n")    # Stretches straight
    time.sleep(5)  # Wait for the connection to establish

    send_command(ser, "MOVE,0,87,10,70,90,70\n")  # Gripper Closes
    time.sleep(5)  # Wait for the connection to establish

    #send_command(ser, "MOVE,0,90,90,90,90,70\n")   # Stretches straight
    #time.sleep(5)  # Wait for the connection to establish

    #send_command(ser, "MOVE,0,90,45,180,90,70\n")  # standard position
    #time.sleep(5)  # Wait for the connection to establish

    send_command(ser, "MOVE,180,120,30,10,90,70\n")  # Base rotates
    time.sleep(5)

    send_command(ser, "MOVE,180,120,30,10,90,10\n")  # Gripper opens

    ser.close()
