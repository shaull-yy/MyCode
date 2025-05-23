import pandas as pd
from garminconnect import Garmin
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

def build_data_df(one_line: dict, data_df):
	if data_df.empty:
		data_df = pd.DataFrame([one_line])  # Initialize with the first row
	else:
		data_df = pd.concat([data_df, pd.DataFrame([one_line])], ignore_index=True)
	return data_df

def convert_speed2pace(speed):
	pace_seconds = 1000 / speed
	minutes = int(pace_seconds // 60)
	seconds = int(pace_seconds % 60)
	return f"{minutes:02}:{seconds:02}"

# Login details
email = "shaull@yahoo.com"
password = "JustDoIt01"

# Login to Garmin Connect
try:
	client = Garmin(email, password)
	client.login()
	print("Logged in successfully!")
except Exception as e:
	print(f"Error logging in: {e}")
	exit()

# Fetch recent activities
activities = client.get_activities(0, 30)  # Retrieve the last 10 activities
#print('activities type:  ',type(activities))
# Prepare a list to store activity and split data

data_df = pd.DataFrame(None)

# Iterate over activities
for activity in activities:
	activity_id = activity["activityId"]
	activity_name = activity['activityName']
	start_date = activity.get("startTimeLocal", 0)
	#print('activity_name:   ',activity_name)
	details = client.get_activity(activity_id)

	# Check if splits exist in the activity
	if "splitSummaries" in details:
		for split in details["splitSummaries"]:
			# Append each split as a row
			split_info = {
				"Activity ID": activity_id,
				"activity name": activity_name,
				"start date": start_date,
				"splitType": split.get("splitType", "Unknown"),
				"Split Number": split["noOfSplits"],
				"distance": split["distance"],
				"duration": split["duration"],
				"elevationGain": split.get("elevationGain", 0),  # Default to 0 if not present
				"averageSpeed": split.get("averageSpeed", 0)
			}
			data_df = build_data_df(split_info, data_df)
	else:
		# Handle activities with no splits
		split_info = {
				"Activity ID": activity_id,
				"activity name": activity_name,
				"start date": start_date,
				"splitType": None,
				"Split Number": None,
				"distance": activity["distance"],
				"duration": activity["duration"],
				"elevationGain": split.get("elevationGain", 0),  # Default to 0 if not present
				"averageSpeed": split.get("averageSpeed", 0)
			}
		data_df = build_data_df(split_info, data_df)

# Create a DataFrame from the data

print('---------data_df----------')
print(data_df)
data_df_grp = data_df.groupby(["Activity ID","activity name","start date", "splitType"]).agg(
	avg_speed = ('averageSpeed', 'mean'),
	interval_count= ('Activity ID', 'count')
).reset_index()
data_df_grp = data_df_grp[data_df_grp['splitType'] == 'RWD_RUN']
data_df_grp['avg speed km/hr'] = data_df_grp['avg_speed'] * 3600 / 1000
data_df_grp['avg pace'] =  data_df_grp['avg_speed'].apply(convert_speed2pace)
data_df_grp['intervals ind'] = data_df_grp['activity name'].str.contains('run free', case=False).astype(int)
data_df_grp['start date 2'] = pd.to_datetime(data_df_grp['start date'], errors='coerce')
data_df_grp['start date 2'] = data_df_grp['start date 2'].dt.date

#------ plots ------
df_intervals = data_df_grp[data_df_grp['intervals ind'] == 1]
df_no_intervals = data_df_grp[data_df_grp['intervals ind'] == 0]

fic, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df_no_intervals['start date 2'], df_no_intervals['avg speed km/hr'], label='None Interval Runs', marker='o')
ax1.plot(df_intervals['start date 2'], df_intervals['avg speed km/hr'], label='Interval runs', marker='s')

ax1.set_xlabel('Date')
ax1.set_ylabel('Avg Speed (km/hr)')
#ax1.set_title('Pace Over Time')
ax1.legend(loc="upper left")
ax1.grid()

# Secondary y-axis for pace
# Link secondary y-axis to primary (speed to pace)
ax2 = ax1.twinx()
ax2.set_ylabel("Pace (min/km)", color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Synchronize pace ticks with speed
#pace_ticks = [60 / speed for speed in ax1.get_yticks()]  # Convert speed ticks to pace
speed_ticks = ax1.get_yticks()  # Get speed tick values
pace_ticks = [60 / speed if speed > 0 else None for speed in speed_ticks]  # Convert to pace
ax2.set_yticks(pace_ticks)  # Apply pace ticks
ax2.set_yticklabels([f"{int(tick):02}:{int((tick % 1) * 60):02}" for tick in pace_ticks])  # Format as min:sec
ax2.invert_yaxis()  # Reverse the order of the secondary y-axis

plt.title("Speed and Pace Over Time")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print('---------data_df_grp----------')
print(data_df_grp)
data_df.to_csv("garmin_activities_with_splits1.csv", index=False)
data_df_grp.to_csv("garmin_activities_with_splits2.csv", index=False)
