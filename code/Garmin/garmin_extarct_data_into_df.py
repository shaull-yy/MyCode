import pandas as pd
from garminconnect import Garmin
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import time
from datetime import datetime
import os
import json
import shutil
import tkinter as tk
from tkinter import StringVar

def get_activities_count(default_activities_count):
	num = 0
	upd_db = ''
	def submit():
		nonlocal num, upd_db
		num = entry.get()  # Retrieve input
		upd_db = upd_db_radio_var.get()
		root.destroy()

	def stop_program():
		nonlocal num, upd_db
		num = 0
		upd_db = ''
		root.destroy()

	def close_with_escape(event=None):
		nonlocal num, upd_db  # Access the enclosing scope's variable
		num = 0
		upd_db = ''
		root.destroy()  # Close the window	

	def clear_entry_on_focus(event):
		if entry.get() == default_activities_count:
			entry.delete(0, tk.END)  # Clear the entry

#-------- Main of function -------
	default_activities_count = str(default_activities_count)
	root = tk.Tk()
	root.geometry('600x250')
	root.title(f'Set How Many Activities to Extract')
	# Bind Escape key to close the window
	root.bind("<Escape>", close_with_escape)
	# set up ui
	font_size = 10
	btn_width = 17
	current_row = 3
	#root.bind_escape()		
	root.columnconfigure(1, weight=1) 
	upd_db_radio_var = StringVar(value="yes")

	# Labels
	file_name_lable = tk.Label(root, text=f'Number of Activities to Extract:', font=("Arial", font_size))
	file_name_lable.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 0), padx=(5, 0))
	# text box for insert a number
	current_row += 1
	entry = tk.Entry(root)
	entry.grid(row=current_row, column=0, sticky=tk.NW, pady=(10, 5), padx=(5, 0))
	entry.insert(0, default_activities_count)
	entry.bind("<FocusIn>", clear_entry_on_focus)  # Bind focus event to clear default value

	current_row += 1
	radio_btn_row = current_row
	# Buttons
	submit_btn = tk.Button(root, text='Submit', command=submit, width=btn_width, bg='light gray')
	submit_btn.grid(row=current_row, column=0, sticky=tk.NW, pady=(10, 5), padx=(5, 0))
	current_row += 1

	stop_btn = tk.Button(root, text='Abort Program', command=stop_program, width=btn_width, bg='light gray')
	stop_btn.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 5), padx=(5, 0))

	radio_btn1 = tk.Radiobutton(root, text='Dont UPD Garmin DB (Tests)', variable=upd_db_radio_var, value='no')
	radio_btn1.grid(row=radio_btn_row, column=1,sticky=tk.NW, pady=(0, 5), padx=(5, 0))
	radio_btn_row +=1
	radio_btn2 = tk.Radiobutton(root, text='UPD Garmin DB', variable=upd_db_radio_var, value='yes')
	radio_btn2.grid(row=radio_btn_row, column=1,sticky=tk.NW, pady=(0, 5), padx=(5, 0))

	root.mainloop()
	return num, upd_db 


def build_data_df(one_line: dict, data_df):
	if not data_df.empty:
		data_df = pd.concat([data_df, pd.DataFrame([one_line])], ignore_index=True)
	else:
		data_df = pd.DataFrame([one_line])  # Initialize with the first row
	return data_df

def convert_speed2pace(speed):
	if speed != 0:
		pace_seconds = 1000 / speed
		minutes = int(pace_seconds // 60)
		seconds = int(pace_seconds % 60)
		return f"{minutes:02}:{seconds:02}"
	else:
		return "20:00"

def draw_plot(garmin_df):
	df_intervals = garmin_df[garmin_df['no intervals ind'] == 0]
	df_no_intervals = garmin_df[garmin_df['no intervals ind'] == 1]

	#speed = [3,4,5,6,7,8,9,10,11,12] #np.linspace(5, 15, len(dates))  # Speed in km/hr (linear progression from 5 to 15)

	fig, ax = plt.subplots(figsize=(10, 5))
	ax.plot(df_no_intervals['start date 2'], df_no_intervals['avg speed km/hr'], label='None Interval Runs', marker='o', linestyle=':')
	ax.plot(df_intervals['start date 2'], df_intervals['avg speed km/hr'], label='Interval runs', marker='s', linestyle=':')
	# Custom y-axis ticks and labels in "speed-pace" format
	ticks = [3,4,5,6,7,8,9,10,11,12] #np.linspace(5, 15, 10)  # Speed ticks from 5 to 15
	labels = [f"{int(tick)}/{round(60 / tick, 1)}" for tick in ticks]  # Speed-pace labels
	ax.set_yticks(ticks)
	ax.set_yticklabels(labels)
	ax.set_xlabel('Date')
	ax.set_ylabel('AVG Speed (km/hr) / Pace (min/km)')
	ax.tick_params(axis='y', labelcolor='b')
	# Format x-axis
	#ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
	#ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))  # Format as 'Jan-2025'
	ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Major ticks at 1-month intervals
	plt.xticks(rotation=45)

	ax.legend(loc="upper left")
	plt.grid(True, which='both', linestyle='--', linewidth=0.5)	
	plt.title("Speed and Pace Over Time")

	plt.tight_layout()
	plt.savefig(garmin_activities_plot)  # Saves as PNG
	print(f'Plot is saved into: {garmin_activities_plot}')
	#plt.show()


#---------------- MAIN --------------------
#-------------init-------------
json_file_path = 'C:/_Shaul/Python/_My_Code/oper_params/garmin_oper.json'
with open(json_file_path, 'r') as file:
	basic_oper = json.load(file)

email = basic_oper.get('email', '')
password = basic_oper.get('password', '')
default_activities_count = basic_oper.get('default_activities_count')
date_time = end_time = time.time()
date_stamp = datetime.fromtimestamp(end_time).strftime('%y%m%d-%H%M%S')
output_trans_file = basic_oper.get('output_trans_file', '').replace('<yyymmdd-hhmmss>', date_stamp)
garmin_incremental_extract_file_name = basic_oper.get('garmin_incremental_extract_file_name', '').replace('<yyymmdd-hhmmss>', date_stamp)
garmin_db_file_name = basic_oper.get('garmin_db_file_name')
garmin_activities_plot = basic_oper.get('garmin_activities_plot')
del basic_oper

activities_count, upd_garmin_db = get_activities_count(default_activities_count)
activities_count = int(activities_count)
print('activities_count:', activities_count)
print('Update Garmin DB IND:', upd_garmin_db)
if activities_count == 0:
	print(f'User has set the number of activities to extarct ()"activities_count") to {activities_count} - Aborting')
	exit(0)


data_df = pd.DataFrame(None)

#-------------END Init ------------

# Login to Garmin Connect
try:
	client = Garmin(email, password)
	client.login()
	print("Logged in successfully!")
except Exception as e:
	print(f"Fatal Error - Aborting, Failed to log-in. Error Details: {e}")
	exit(1)

# Fetch recent activities
activities = client.get_activities(0, activities_count)  # Retrieve the last X activities

# Iterate over activities
for activity in activities:
	activity_id = activity["activityId"]
	activity_name = activity['activityName']
	start_date = activity.get("startTimeLocal", 0)
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
				"averageSpeed": split.get("averageSpeed", 0),
				"distance": split.get("distance",0),
				"averageHR": split.get("averageHR", 0),
				"averageRunCadence": split.get("averageRunCadence", 0),
				"strideLength": split.get("strideLength", 0),
				"maxDistance": split.get("maxDistance", 0)
			}
			data_df = build_data_df(split_info, data_df)
	else:
		# Handle activities with no splits
		split_info = {
				"Activity ID": activity_id,
				"activity name": activity_name,
				"start date": start_date,
				"splitType": 0,
				"Split Number": 0,
				"distance": activity.get("distance",0),
				"duration": activity.get("duration",0),
				"elevationGain": activity.get("elevationGain", 0),  # Default to 0 if not present
				"averageSpeed": activity.get("averageSpeed", 0),
				"distance": activity.get("distance",0),
				"averageHR": activity.get("averageHR", 0),
				"averageRunCadence": 0,
				"strideLength": 0,
				"maxDistance": 0
			}
		data_df = build_data_df(split_info, data_df)


#print('---------data_df----------')
#print(data_df)
data_df_grp = data_df.groupby(["Activity ID","activity name","start date", "splitType"]).agg(
	avg_speed = ('averageSpeed', 'mean'),
	interval_count= ('Activity ID', 'count'),
	distance=('distance', 'sum'),
	elevationGain=('elevationGain', 'sum'),
	averageHR=('averageHR', 'mean'),
	averageRunCadence=('averageRunCadence', 'mean'),
	averageStrideLength=('strideLength', 'mean')
).reset_index()
data_df_grp = data_df_grp[data_df_grp['splitType'] == 'RWD_RUN']
data_df_grp['avg speed km/hr'] = data_df_grp['avg_speed'] * 3600 / 1000
data_df_grp['avg pace sec'] = 60 / data_df_grp['avg speed km/hr']
data_df_grp['avg pace'] =  data_df_grp['avg_speed'].apply(convert_speed2pace)
data_df_grp['no intervals ind'] = data_df_grp['activity name'].str.contains('run free', case=False).astype(int)
data_df_grp['start date 2'] = pd.to_datetime(data_df_grp['start date'], errors='coerce')
data_df_grp['start date 2'] = data_df_grp['start date 2'].dt.date


#------------ Merge new data with local excel (local "database")
#work_with_trans_only = input('\n>>Enter 0 for updating the garmin db \n>> Enter any char to generate trans file only')
current_garmin_db_df_exists = False
if upd_garmin_db == 'yes':
	# First backup current db:
	backup_file_name, suffix = os.path.splitext(garmin_db_file_name)
	backup_file_name = backup_file_name + '_' + date_stamp + suffix
	if os.path.exists(garmin_db_file_name):
		shutil.copy2(garmin_db_file_name, backup_file_name)
		current_garmin_db_df = pd.read_excel(garmin_db_file_name)
		current_garmin_db_df['start date 2'] = pd.to_datetime(current_garmin_db_df['start date 2'], errors='coerce')
		current_garmin_db_df['start date 2'] = current_garmin_db_df['start date 2'].dt.date
		new_garmin_db_df = pd.concat([current_garmin_db_df, data_df_grp]).drop_duplicates(['Activity ID', 'activity name'])
		new_garmin_db_df = new_garmin_db_df.sort_values(by='start date 2')
		new_garmin_db_df.to_excel(garmin_db_file_name, index=False)
		current_garmin_db_df_exists = True
	else:
		print('>> Warning/Error: There is no Garmin permenant DB excel file')
		print('>> A new excel DB is created from the "data_df_grp" dataframe')
		data_df_grp.to_excel(garmin_db_file_name, index=False)
		#current_garmin_db_df_exists = False

	if current_garmin_db_df_exists:
		draw_plot(new_garmin_db_df)
	else:
		draw_plot(data_df_grp)

#Keep files from this run
data_df_grp.to_excel(garmin_incremental_extract_file_name, index=False)
data_df.to_excel(output_trans_file, index=False)

print('====== program Ended Successfully ========')
print(f'Extracted number of rows from Garmin site: {len(data_df_grp)}')
if current_garmin_db_df_exists:
	print(f'Number of rows from excel DB (before adding extracted data): {len(current_garmin_db_df)}')
	print(f'Number of rows in final excel DB (after adding extracted data & remove duplicates): {len(new_garmin_db_df)}')
	print(f'Number of rows added to the final excel DB: {len(new_garmin_db_df) - len(current_garmin_db_df)}')
else:
	print(f'Number of rows from excel DB (before adding extracted data): 0 (excel db does not exist)')
	print(f'Number of rows in final excel DB (created from scratch): {len(data_df_grp)}')
