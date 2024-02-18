import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import statistics
from scipy.spatial.transform import Rotation as R

data = np.loadtxt(r"C:\Users\achen\Dropbox\code\treehacks10\put-me-in-coach\good_data\accel_data(12).csv", delimiter=",")

time = data[:,0]
# data[:,1:]*=-1
data[:,9]*=-1
# 9
length = 1
fixed_point = np.array([0, 0])

# Initialize the figure and axis for plotting
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)

# Create a line object. This will be updated in the animation

line1, = ax.plot([], [], lw=2, color='blue')
line2, = ax.plot([], [], lw=2, color='red')
line3, = ax.plot([], [], lw=2, color='green')

def init():
    """Initialize the background of the animation."""
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line1, line2, line3

def update(degrees):
    """Update the animation by one step."""
    """Update the animation based on the current degrees of rotation for each line."""
    degree1, degree2, degree3 = degrees
    # Calculate the new endpoint of the first line using its degree
    angle1 = np.deg2rad(degree1)
    new_point1 = fixed_point + np.array([np.cos(angle1), np.sin(angle1)]) * length
    line1.set_data([fixed_point[0], new_point1[0]], [fixed_point[1], new_point1[1]])

    # Calculate the new endpoint of the second line using its degree
    # The second line starts from the endpoint of the first line
    angle2 = np.deg2rad(degree2)
    new_point2 = new_point1 + np.array([np.cos(angle2), np.sin(angle2)]) * length
    line2.set_data([new_point1[0], new_point2[0]], [new_point1[1], new_point2[1]])

    angle3 = np.deg2rad(degree3)
    new_point3 = new_point2 + np.array([np.cos(angle3), np.sin(angle3)]) * 0.2
    line3.set_data([new_point2[0], new_point3[0]], [new_point2[1], new_point3[1]])


    return line1, line2, line3

def calculate_angle(x, z):
    # Calculate the angle in radians
    theta_radians = np.arctan2(z, x)

    # Convert the angle to degrees
    theta_degrees = np.degrees(theta_radians)

    return theta_degrees

def rotation_from_vectors(v1, v2):
    """
    Calculate the rotation matrix required to rotate from vector v1 to vector v2.
    Also, calculate the Euler angles that represent the rotation around the x, y, and z axes.

    Parameters:
    v1, v2: Input vectors between which to calculate the rotation. Must be 3D vectors.

    Returns:
    rotation_matrix: The 3x3 rotation matrix.
    euler_angles: Rotation around the x, y, and z axes in radians.
    """
    # Normalize input vectors
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)

    # Use scipy to calculate the rotation vector and matrix
    rotation_vector = R.align_vectors([v2_u], [v1_u])[0].as_rotvec()
    rotation_matrix = R.from_rotvec(rotation_vector).as_matrix()

    # Convert rotation matrix to Euler angles
    euler_angles = R.from_matrix(rotation_matrix).as_euler('xyz', degrees=False)

    return rotation_matrix, euler_angles

def rotation_angle_2d(v1, v2):
    """
    Calculate the rotation angle in degrees required to rotate v1 to align with v2 in 2D.

    Parameters:
    v1, v2: Input 2D vectors.

    Returns:
    angle_degrees: The rotation angle around the z-axis in degrees to align v1 with v2.
    """
    # Normalize the vectors
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)

    # Calculate the angle using the dot product and cross product
    angle_radians = np.arctan2(v2_u[1], v2_u[0]) - np.arctan2(v1_u[1], v1_u[0])

    # Ensure the angle is in the range [-pi, pi]
    angle_radians = np.arctan2(np.sin(angle_radians), np.cos(angle_radians))

    # Convert the angle to degrees
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees


degrees = []

degree_bicep = rotation_angle_2d([statistics.mean(data[:10,13]),statistics.mean(data[:10,15])],[0,10])
print([statistics.mean(data[:10,13]),statistics.mean(data[:10,15])])
print(degree_bicep)

degree_forearm = rotation_angle_2d([statistics.mean(data[:10,1]),statistics.mean(data[:10,3])], [0,-10])
print([statistics.mean(data[:10,1]),statistics.mean(data[:10,3])])
print(degree_forearm)

#7 8 9, 10 11 12
degree_hand = rotation_angle_2d([statistics.mean(data[:10,7]),statistics.mean(data[:10,9])], [0,-10])
print([statistics.mean(data[:10,7]),statistics.mean(data[:10,9])])
print(degree_hand)


times = []
for i in range(len(time)-1):
    time_curr = time[i+1]-time[i]
    times.append(time_curr)

    degree_rotated_bicep = (data[i,17]  * time_curr) * 180 / np.pi
    degree_bicep += degree_rotated_bicep

    degree_rotated_forearm = (data[i,5]  * time_curr) * 180 / np.pi + 0.5*(data[i,4]  * time_curr) * 180 / np.pi
    degree_forearm += degree_rotated_forearm

    degree_rotated_hand = (-data[i,11]  * time_curr) * 180 / np.pi
    degree_hand += degree_rotated_hand


    degrees.append([degree_bicep, degree_forearm, degree_hand])
    # degrees.append([rotation_angle_2d([data[i,13],data[i,15]],
    #                         [0,10]),
    #                 rotation_angle_2d([data[i,1],data[i,3]],
    #                         [0,-10])])

degrees += [[-180,-180, -180]] * 20
# print(degrees)


# Create the animation

ani = FuncAnimation(fig, update, frames=degrees, init_func=init, blit=True)
# plt.plot(time, data[:,5], label = "y")

fps = 1/(sum(times)/len(times))
print("FPS:", fps)

# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
# ani.save('animation.mp4', writer = writer)
writer = animation.PillowWriter(fps=fps,
                                metadata=dict(artist='Me'),
                                bitrate=1800)
ani.save('scatter.gif', writer=writer)

print("done")
# plt.show()

