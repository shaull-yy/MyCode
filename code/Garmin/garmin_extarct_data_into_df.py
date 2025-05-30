import pandas as pd
from garminconnect import Garmin
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import time
from datetime import datetime
import os
import sys
import json
import shutil
import tkinter as tk
from tkinter import StringVar
#sys.path.append('C:/_Shaul/Projects/_My_Code/code/My_Utilities')
from utl_my_logging import my_logging

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

	#-------- Main part of of function -------
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
	submit_btn.focus_set()  # Set the Submit button as the focused widget
	root.bind("<Return>", lambda event: submit())  # Bind Enter key to the Submit button
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


def build_data_df(one_line: dict, all_raw_trans_df):
	if not all_raw_trans_df.empty:
		all_raw_trans_df = pd.concat([all_raw_trans_df, pd.DataFrame([one_line])], ignore_index=True)
	else:
		all_raw_trans_df = pd.DataFrame([one_line])  # Initialize with the first row
	return all_raw_trans_df

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
	ax.plot(df_no_intervals['start_date_2'], df_no_intervals['avg speed km/hr'], label='None Interval Runs', marker='o', linestyle=':')
	ax.plot(df_intervals['start_date_2'], df_intervals['avg speed km/hr'], label='Interval runs', marker='s', linestyle=':')
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

def upd_split_info(activity, all_raw_trans_df):
	activity_id = activity.get("activityId")
	activity_name = activity.get('activityName')
	activity_start_date = activity.get("startTimeLocal", 0)
	activity_type  = activity.get("activityType", 0).get("typeKey", 0)
	activity_distance  = activity.get("distance", 0)
	activity_duration  = activity.get("duration", 0)
	activity_average_speed  = activity.get("averageSpeed", 0)
	activity_average_HR  = activity.get("averageHR", 0)
	activity_avg_stride_len  = activity.get("avgStrideLength", 0)
		
	details = client.get_activity(activity_id)
	# Check if splits exist in the activity
	if "splitSummaries" in details:
		for split in details["splitSummaries"]:
			# Append each split as a row
			split_info = {
				'activity_id': activity_id,
				'activity_name': activity_name,
				'activity_start_date': activity_start_date,
				'activity_type': activity_type,
				'activity_distance': activity_distance,
				'activity_duration': activity_duration,
				'activity_average_speed': activity_average_speed,
				'activity_average_HR': activity_average_HR,
				'activity_avg_stride_len': activity_avg_stride_len,
				
				"lap_type": split.get("splitType", "Unknown"),
				"lap_split_number": split["noOfSplits"],
				"lap_distance": split.get("distance",0),
				"lap_duration": split["duration"],
				"lap_elevation_gain": split.get("elevationGain", 0),  
				"lap_average_speed": split.get("averageSpeed", 0),				
				"lap_average_HR": split.get("averageHR", 0),
				"lap_average_run_cadence": split.get("averageRunCadence", 0),
				"lap_stride_length": split.get("strideLength", 0)
			}
			all_raw_trans_df = build_data_df(split_info, all_raw_trans_df)
	else:
		# Handle activities with no splits
		split_info = {
				'activity_id': activity_id,
				'activity_name': activity_name,
				'activity_start_date': activity_start_date,
				'activity_type': activity_type,
				'activity_distance': activity_distance,
				'activity_duration': activity_duration,
				'activity_average_speed': activity_average_speed,
				'activity_average_HR': activity_average_HR,
				'activity_avg_stride_len': activity_avg_stride_len,
				
				"lap_type": 0,
				"lap_split_number": 0,
				"lap_distance": 0,
				"lap_duration": 0,
				"lap_elevation_gain": 0,  
				"lap_average_speed": 0,				
				"lap_average_HR": 0,
				"lap_average_run_cadence": 0,
				"lap_stride_length": 0
			}
		all_raw_trans_df = build_data_df(split_info, all_raw_trans_df)

	return all_raw_trans_df

def handle_garmin_db(db_file_name, db_df, db_name_for_msg):
	file_path = os.path.dirname(db_file_name)  # Extracts the directory path
	file_name, suffix = os.path.splitext(os.path.basename(db_file_name))
	backup_file_name = file_path + '/bck_' + file_name + '_' + date_stamp + suffix
	if os.path.exists(db_file_name):
		shutil.copy2(db_file_name, backup_file_name)
		current_garmin_db_df = pd.read_excel(db_file_name)
		new_garmin_db_df = pd.concat([current_garmin_db_df, db_df]).drop_duplicates(['activity_id'])
		new_garmin_db_df['start_date_2'] = pd.to_datetime(new_garmin_db_df['start_date_2'], errors='coerce')
		new_garmin_db_df['start_date_2'] = new_garmin_db_df['start_date_2'].dt.date
		#print(new_garmin_db_df)
		new_garmin_db_df = new_garmin_db_df.sort_values(by='start_date_2')
		new_garmin_db_df.to_excel(db_file_name, index=False)
		current_garmin_db_len = len(current_garmin_db_df)
		new_garmin_db_len = len(new_garmin_db_df)
		current_garmin_db_df_exists = True
	else:
		loging.print_message('W', f'There is no Garmin permenant DB excel file for {db_name_for_msg} \n  A new excel DB is created from the {db_name_for_msg} dataframe')
		db_df.to_excel(db_file_name, index=False)
		current_garmin_db_len = 0
		new_garmin_db_len = len(db_df)
		current_garmin_db_df_exists = False
	
	db_df_len = len(db_df)
	return current_garmin_db_df_exists, db_df_len, current_garmin_db_len, new_garmin_db_len


#---------------- MAIN --------------------
#-------------init-------------
loging = my_logging(False, __file__)
loging.start_program_msg()

json_file_path = 'C:/_Shaul/Projects/_My_Code/oper_params/garmin_oper.json'
with open(json_file_path, 'r') as file:
	basic_oper = json.load(file)

email = basic_oper.get('email', '')
password = basic_oper.get('password', '')
default_activities_count = basic_oper.get('default_activities_count')
date_time = end_time = time.time()
date_stamp = datetime.fromtimestamp(end_time).strftime('%y%m%d-%H%M-%S')
output_trans_file = basic_oper.get('output_trans_file', '').replace('<yyymmdd-hhmmss>', date_stamp)
all_raw_transactions_file = basic_oper.get('all_raw_transactions_file', '').replace('<yyymmdd-hhmmss>', date_stamp)
garmin_incremental_extract_file_name = basic_oper.get('garmin_incremental_extract_file_name', '').replace('<yyymmdd-hhmmss>', date_stamp)
garmin_split_db_file_name = basic_oper.get('garmin_split_db_file_name')
output_activ_level_trans_file = basic_oper.get('output_activ_level_trans_file').replace('<yyymmdd-hhmmss>', date_stamp)
garmin_activ_db_file_name = basic_oper.get('garmin_activ_db_file_name')
garmin_activities_plot = basic_oper.get('garmin_activities_plot')
del basic_oper

activities_count, upd_garmin_db = get_activities_count(default_activities_count)
activities_count = int(activities_count)
loging.print_message('I',f'Number of activities to extarct from Garmin: {activities_count}')
loging.print_message('I',f'Update Garmin DB IND: {upd_garmin_db}')
if activities_count == 0:
	loging.print_message('F',f'User has set the number of activities to extarct from Garmin to 0')

activity_level_columns = [
	'activity_id', 'activity_name', 'activity_start_date', 'activity_type', 'activity_distance',
	'activity_duration', 'activity_average_speed', 'activity_average_HR', 'activity_avg_stride_len', 'start_date_2']

all_raw_trans_df = pd.DataFrame(None)

#-------------END Init ------------

# Login to Garmin Connect
try:
	client = Garmin(email, password)
	client.login()
	loging.print_message('I',"Logged in to Garmin successfully")
except Exception as e:
	loging.print_message('F',f"Failed to log-in to Garmin. Error Details: {e}")

# Fetch recent activities
activities = client.get_activities(0, activities_count)  # Retrieve the last X activities

# Iterate over activities, create the all_raw_trans_df data frame
for activity in activities:
	all_raw_trans_df = upd_split_info(activity, all_raw_trans_df)

all_raw_trans_df['activity_intervals_ind'] = all_raw_trans_df['activity_name'].apply(
	lambda x: 'No-Intervals' if 'run free' in x.lower() else 'Intervals')
all_raw_trans_df['start_date_2'] = pd.to_datetime(all_raw_trans_df['activity_start_date'], errors='coerce')
all_raw_trans_df['start_date_2'] = all_raw_trans_df['start_date_2'].dt.date
run_laps_df = all_raw_trans_df[all_raw_trans_df['lap_type'] == 'RWD_RUN']
activity_level_df = all_raw_trans_df[activity_level_columns].drop_duplicates(['activity_id'])

run_laps_df_grp = run_laps_df.groupby(["activity_id","activity_name","activity_start_date", "lap_type", 
									   "activity_intervals_ind", "start_date_2"]).agg(
	all_laps_avg_speed = ('lap_average_speed', 'mean'),
	interval_count= ('activity_id', 'count'),
	all_laps_distance=('lap_distance', 'sum'),
	all_laps_elevation_gain=('lap_elevation_gain', 'sum'),
	all_laps_average_HR=('lap_average_HR', 'mean'),
	all_laps_average_run_cadence=('lap_average_run_cadence', 'mean'),
	all_laps_average_stride_length=('lap_stride_length', 'mean')
).reset_index()
run_laps_df_grp['all_laps_average_speed_km/hr'] = run_laps_df_grp['all_laps_avg_speed'] * 3600 / 1000
run_laps_df_grp['all_laps_avg_pace_sec'] = 60 / run_laps_df_grp['all_laps_average_speed_km/hr']
run_laps_df_grp['all_laps_avg_pace'] =  run_laps_df_grp['all_laps_avg_speed'].apply(convert_speed2pace)


#------------ Merge new data with local excel (local "database")
#work_with_trans_only = input('\n>>Enter 0 for updating the garmin db \n>> Enter any char to generate trans file only')
if upd_garmin_db == 'yes':
	(current_garmin_split_db_exists, 
	run_laps_df_grp_len, 
	current_garmin_split_db_len, 
	new_garmin_split_db_len
	) = handle_garmin_db(garmin_split_db_file_name, run_laps_df_grp, 'Split Level Data base')

	(current_garmin_split_db_exists, 
		activity_level_df_len, 
		current_garmin_activ_db_len, 
		new_garmin_activ_db_len
		) = handle_garmin_db(garmin_activ_db_file_name, activity_level_df, 'Activity Level Data base')

else:
	current_garmin_split_db_len = 0
	current_garmin_activ_db_len = 0
	new_garmin_activ_db_len = 0
	new_garmin_split_db_len = 0

#	if current_garmin_split_db_exists:
#		draw_plot(new_garmin_db_df)
#	else:
#		draw_plot(run_laps_df_grp)

#Keep transactions files from this run
run_laps_df_grp.to_excel(garmin_incremental_extract_file_name, index=False)
activity_level_df.to_excel(output_activ_level_trans_file, index=False)
#run_laps_df.to_excel(output_trans_file, index=False)
all_raw_trans_df.to_excel(all_raw_transactions_file, index=False)

msg_txt = ['Running Mode - Update Garmin Databases ("no" is for Test Mode)',
		   'All - Total raw transactions extracted from garmin site'
		   'Laps Transactions - Number of extracted laps rows',
		   'Lap DB - Number of rows from DB excel (before adding new data)',
		   'Lap DB - Number of rows in final DB excel (after adding new data, no dupl)',
		   'Lap DB - Number of rows added to the DB excel',
		   'Activity Transactions - Number of extracted activity level rows',
		   'Activity DB - Number of rows from DB excel (before adding new data)',
		   'Activity DB - Number of rows in final DB excel (after adding new data, no dupl)',
		   'Activity DB - Number of rows added to the DB excel'
		   ]
msg_numbrs = [upd_garmin_db,
			  len(all_raw_trans_df),
			  run_laps_df_grp_len,
			  current_garmin_split_db_len,
			  new_garmin_split_db_len,
			  new_garmin_split_db_len - current_garmin_split_db_len,
			  activity_level_df_len,
			  current_garmin_activ_db_len,
			  new_garmin_activ_db_len,
			  new_garmin_activ_db_len - current_garmin_activ_db_len
			]
loging.print_running_statistics(msg_txt, msg_numbrs)
loging.stop_program_msg()
