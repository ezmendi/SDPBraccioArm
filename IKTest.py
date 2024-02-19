import numpy as np
import matplotlib.pyplot as plt
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import ikpy.utils.plot as plot_utils

# Create a kinematic chain for demonstration
# This could represent a simplified robotic arm
chain = Chain(name='Braccio_arm', links=[
    OriginLink(),
    URDFLink(
      name="base",
      origin_translation=[0, 0, 0.078],  # BASE_HGT in meters
      origin_orientation=[0, 0, 0],
      rotation=[0, 0, 1],  # Assuming rotation around the Y-axis for the base
    ),
    URDFLink(
      name="shoulder",
      origin_translation=[0, 0, 0.124],  # HUMERUS in meters
      origin_orientation=[0, 0, 0],
      rotation=[0, 1, 0],  # Assuming rotation around the X-axis for the shoulder
    ),
    URDFLink(
      name="elbow",
      origin_translation=[0, 0.124, 0],  # ULNA in meters, placed along the Y-axis for demonstration
      origin_orientation=[0, 0, 0],
      rotation=[0, 1, 0],  # Assuming rotation around the X-axis for the elbow
    ),

    URDFLink(
        name="wrist_rotation",
        origin_translation=[0, 0.124, 0],  # Adjusted for continuity in the arm's structure
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1],  # Corrected to assume rotation around the Z-axis for wrist rotation
        )

])

# Target position and orientation
target_position = np.array([0.09, 0.09, 0.17])  # Adjusted Z for reachable target above the base
target_orientation = np.eye(3)  # Identity matrix for neutral orientation

# Create the target frame (4x4 homogeneous transformation matrix)
target_frame = np.eye(4)
target_frame[:3, 3] = target_position
target_frame[:3, :3] = target_orientation

# Adapted code: Correctly call inverse_kinematics with the target_frame
angles = chain.inverse_kinematics(target_frame[:3, 3])

print("Calculated joint angles:", angles)

# Use forward kinematics to get the real end-effector position from the calculated angles
real_frame = chain.forward_kinematics(angles)

print("Desired position:", target_position)
print("Computed joint angles:", angles)
print("End effector position from FK:", real_frame[:3, 3])

# Plotting
fig, ax = plot_utils.init_3d_figure()
chain.plot(angles, ax=ax, target=target_position)
plt.show()
