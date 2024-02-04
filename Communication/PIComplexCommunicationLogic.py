import serial
import time

def send_command_to_arduino(command):
    # Specify the serial port and baud rate
    serial_port = '/dev/ttyUSB0'  # Adjust this to match your Arduino's serial port
    baud_rate = 9600  # Must match the baud rate set in your Arduino sketch

    try:
        # Initialize serial connection
        with serial.Serial(serial_port, baud_rate, timeout=1) as arduino:
            print(f"Sending command: {command}")
            arduino.write((command + '\n').encode())  # Send command
            time.sleep(0.5)  # Wait for the command to be sent
            
            # Wait for the response (if any) and print it
            while arduino.in_waiting:
                response = arduino.readline().decode().strip()
                print(f"Arduino: {response}")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")

# Example command to move the arm
test_command = "MOVE,90,45,0,0,0,0"

# Send the test command
send_command_to_arduino(test_command)
