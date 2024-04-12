import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate random data
x = np.random.normal(size=100)
y = np.random.normal(size=100)
z = np.random.normal(size=100)

# Create a 3D scatter plot with asterisk (*) shape for the points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, marker='*')  # Change marker here

# Set labels and title
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title('3D Scatter Plot')

# Show plot
plt.show()
