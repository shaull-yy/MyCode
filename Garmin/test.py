import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Sample data
dates = [datetime(2025, 5, i) for i in range(1, 11)]  # Dates from May 1 to May 10, 2025
speed = np.linspace(5, 15, len(dates))  # Speed in km/hr (linear progression from 5 to 15)
pace = 60 / speed  # Corresponding pace in min/km

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot speed over time
ax.plot(dates, speed, 'b-', marker='o', label='Speed')
ax.set_xlabel('Date')

# Custom y-axis ticks and labels in "speed-pace" format
ticks = np.linspace(5, 15, 10)  # Speed ticks from 5 to 15
labels = [f"{int(tick)}-{round(60 / tick, 1)}" for tick in ticks]  # Speed-pace labels
ax.set_yticks(ticks)
ax.set_yticklabels(labels)
ax.set_ylabel('Speed (km/hr) - Pace (min/km)', color='b')
ax.tick_params(axis='y', labelcolor='b')

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.xticks(rotation=45)

# Add grid and title
plt.title('Speed and Pace Over Time')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Show the plot
plt.tight_layout()
plt.show()
