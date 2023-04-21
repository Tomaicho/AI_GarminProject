import matplotlib.pyplot as plt

# Example list of sedentary intervals
sedentary_intervals = [(0, 1800), (3600, 5400), (7200, 9000)]

# Create a new figure and axis object
fig, ax = plt.subplots()

# Set the axis limits and labels
ax.set_xlim(0, 24 * 60 * 60)  # assuming 24-hour day in seconds
ax.set_xlabel('Time (s)')

# Plot each interval as a horizontal bar
for interval in sedentary_intervals:
    start_time_s, end_time_s = interval
    ax.broken_barh([(start_time_s, end_time_s - start_time_s)], (0, 1), facecolors='red')

# Show the plot
plt.show()