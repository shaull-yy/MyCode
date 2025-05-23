import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Example DataFrame
data = {
    "Start Date": ["2025-05-01", "2025-05-08", "2025-05-15", "2025-05-22"],
    "Speed (km/h)": [12, 10, 8, 6],  # Speed in km/h
}
df = pd.DataFrame(data)
df["Start Date"] = pd.to_datetime(df["Start Date"])

# Calculate pace from speed (pace = 60 / speed in min/km)
df["Pace (min/km)"] = 60 / df["Speed (km/h)"]

# Plotting
fig, ax1 = plt.subplots()

# Plot speed on primary y-axis
ax1.plot(df["Start Date"], df["Speed (km/h)"], color='blue', marker='o', label="Speed (km/h)")
ax1.set_xlabel("Start Date")
ax1.set_ylabel("Speed (km/h)", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.legend(loc="upper left")
ax1.grid()

# Secondary y-axis for pace
ax2 = ax1.twinx()
ax2.plot(df["Start Date"], df["Pace (min/km)"], color='orange', marker='s', label="Pace (min/km)")
ax2.set_ylabel("Pace (min/km)", color='orange')
ax2.tick_params(axis='y', labelcolor='orange')
ax2.legend(loc="upper right")

# Rotate x-axis labels
plt.xticks(rotation=45)

plt.title("Speed and Pace Over Time")
plt.tight_layout()
plt.show()
