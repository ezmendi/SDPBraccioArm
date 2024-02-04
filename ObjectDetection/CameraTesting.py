import cv2
import numpy as np
import time

# GStreamer pipeline for webcam capture
pipeline_str = (
    "v4l2src device=/dev/video0 ! "
    "videoconvert ! "
    "videoscale ! "
    "video/x-raw, width=640, height=480 ! "
    "appsink"
)

# Create GStreamer pipeline
cap = cv2.VideoCapture(pipeline_str, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Could not open GStreamer pipeline.")
    exit()

KNOWN_WIDTH = 35
FOCAL_LENGTH = 60

def estimate_distance(known_width, focal_length, pixel_width):
    return (known_width * focal_length) / pixel_width

while True:
    # Capture a frame from the GStreamer pipeline
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from GStreamer pipeline.")
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 90, 120])
    upper_red = np.array([10, 255, 90])
    lower_red_alt = np.array([160, 90, 40])
    upper_red_alt = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask2 = cv2.inRange(hsv_frame, lower_red_alt, upper_red_alt)
    red_mask = cv2.bitwise_or(mask1, mask2)

    red_detected = cv2.bitwise_and(frame, frame, mask=red_mask)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 100:  # Adjust this threshold as needed
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(red_detected, (x, y), (x+w, y+h), (0, 255, 0), 3)

            distance = estimate_distance(KNOWN_WIDTH, FOCAL_LENGTH, w)
            cv2.putText(red_detected, f"{distance:.2f}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the frames
    cv2.imshow('Frame', frame)
    cv2.imshow('Detected Red Areas in Color', red_detected)

    # Break from the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the GStreamer pipeline and close all windows
cap.release()
cv2.destroyAllWindows()
