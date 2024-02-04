import cv2
import numpy as np
import math

# Camera Specifications
IMAGE_WIDTH = 1280  # 720p resolution width
IMAGE_HEIGHT = 720  # 720p resolution height
FOV_DEGREES = 60  # Horizontal field of view of the camera in degrees
KNOWN_WIDTH_MM = 35  # Known width of the strawberry in millimeters

# Conversion of FOV from degrees to radians for calculation
FOV_RADIANS = math.radians(FOV_DEGREES)

# Calculate the focal length in pixels
focal_length_px = IMAGE_WIDTH / (2.0 * math.tan(FOV_RADIANS / 2.0))

# GStreamer pipeline for 720p webcam capture
pipeline_str = (
    "v4l2src device=/dev/video0 ! "
    "videoconvert ! "
    "videoscale ! "
    "video/x-raw, width=640, height=480 ! "
    "appsink"
)

# Initialize video capture with GStreamer pipeline
cap = cv2.VideoCapture(pipeline_str, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Could not open GStreamer pipeline.")
    exit()

# Function definitions for distance and coordinate estimation
def estimate_distance_mm(pixel_width):
    return (KNOWN_WIDTH_MM * focal_length_px) / pixel_width

def estimate_coordinates(x, y, w, h):
    object_center_x = x + w / 2
    object_center_y = y + h / 2
    dx_mm = (object_center_x - IMAGE_WIDTH / 2) * (KNOWN_WIDTH_MM / w)
    dy_mm = (object_center_y - IMAGE_HEIGHT / 2) * (KNOWN_WIDTH_MM / w)
    return dx_mm, dy_mm

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert frame to HSV color space for color detection
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range for red color and create masks
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    lower_red_alt = np.array([170, 120, 70])
    upper_red_alt = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask2 = cv2.inRange(hsv_frame, lower_red_alt, upper_red_alt)
    red_mask = cv2.bitwise_or(mask1, mask2)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Estimate distance and coordinates
        distance_mm = estimate_distance_mm(w)
        dx_mm, dy_mm = estimate_coordinates(x, y, w, h)
        
        # Display the bounding box and distance
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"X: {dx_mm:.2f} mm, Y: {dy_mm:.2f} mm, Z: {distance_mm:.2f} mm", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Show the frame
    cv2.imshow('Frame', frame)

    # Break from the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
