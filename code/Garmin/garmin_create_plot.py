import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import json

json_file_path = 'C:/_Shaul/Projects/_My_Code/oper_params/garmin_oper.json'
with open(json_file_path, 'r') as file:
	basic_oper = json.load(file)

garmin_split_db_file_name = basic_oper.get('garmin_split_db_file_name')
garmin_activ_db_file_name = basic_oper.get('garmin_activ_db_file_name')
garmin_activities_plot = basic_oper.get('garmin_activities_plot')
del basic_oper

garmin_data_df = pd.read_excel(garmin_split_db_file_name)

garmin_data_df = garmin_data_df.iloc[-30:]
print('>>>>>> Showing only the last 30 activities')

# Map `activity_intervals_ind` to colors
color_map = {'No-Intervals': 'blue', 'Intervals': 'orange'}
garmin_data_df['bar_color'] = garmin_data_df['activity_intervals_ind'].map(color_map)

# Create the figure and axes
fig, ax1 = plt.subplots(figsize=(15, 6))

# Plot the all_laps_distance as bars
bar_colors = garmin_data_df['bar_color']
ax1.bar(
	garmin_data_df['start_date_2'], garmin_data_df['all_laps_distance'], color=bar_colors, label='Lap Distance (m)'
)

# Set labels for bar plot
ax1.set_xlabel('Date')
ax1.set_ylabel('Lap Distance (m)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Format the x-axis to display dates as 'Jan-2025'
date_format = DateFormatter('%b-%Y')
ax1.xaxis.set_major_formatter(date_format)

# Create a second y-axis for the line plot
ax2 = ax1.twinx()

# Plot activity_average_speed as a line with marker size for elevation_gain
line = ax2.plot(
	garmin_data_df['start_date_2'],
	garmin_data_df['all_laps_average_speed_km/hr'],
	color='green',
	#marker='o',
	label='Avg Speed (m/s)',
)
norm = plt.Normalize(min(garmin_data_df['all_laps_elevation_gain']), max(garmin_data_df['all_laps_elevation_gain']))
cmap = plt.cm.coolwarm  # Use a colormap where red is high, blue is low
# Plot with marker colors set by all_laps_elevation_gain
#plt.scatter(x, y, c=all_laps_elevation_gain, cmap=cmap, s=100)  # s sets marker size, constant here

sc = ax2.scatter(
	garmin_data_df['start_date_2'],
	garmin_data_df['all_laps_average_speed_km/hr'],
	c=garmin_data_df['all_laps_elevation_gain'], cmap=cmap, s=100 # Marker size represents elevation gain
	#color='green'
)
cbar = fig.colorbar(sc, ax=ax2, label='Elevation Gain')  # Attach colorbar to the scatter plot

# Add labels for elevation gain near the markers
for i, row in garmin_data_df.iterrows():
	ax2.text(
		row['start_date_2'],  # X-coordinate
		row['all_laps_average_speed_km/hr'] + 0.1,  # Y-coordinate
		str(int(row['all_laps_elevation_gain'])),  # Text label (elevation gain)
		color='black',  # Label color
		fontsize=9,  # Font size
		ha='center',  # Horizontal alignment
		va='bottom'   # Vertical alignment
	)

# Set labels for line plot
ax2.set_ylabel('Avg Speed (m/s)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Add a legend
fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

# Add the title to the left side of the y-axis
fig.text(
	0.02, 0.5,  # Position: 0.02 (x), 0.5 (y) in figure coordinates
	'Activity Data Visualization',  # Text content
	rotation='vertical',  # Rotate the text
	va='center',  # Vertical alignment
	ha='center',  # Horizontal alignment
	fontsize=12,  # Optional: Adjust the font size
)
# Adjust the layout to provide space for the left-side title
plt.subplots_adjust(left=0.1)  # Increase the left margin
#plt.title('Activity Data Visualization')
#plt.tight_layout()
plt.show()
