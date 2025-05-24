from garminconnect import Garmin
import json

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
activities = client.get_activities(0, 1)  # Retrieve the last 10 activities
print(type(activities))
#print(json.dumps(activities, indent=2))  # Display raw activity data

# Analyze specific activity details
for activity in activities:
	activity_id = activity["activityId"]
	details = client.get_activity(activity_id)
	print('----------activity------------')
	#print(type(activity), len(activity))
	#print(activity)
	print('----------details------------')
	#print(type(details), len(details))
	#print(details)
	print('----------details by JSON dump ------------')
	#print(json.dumps(details, indent=4))

	# Extract interval details if available
	i = 0
	if "splitSummaries" in details:
		print(f'---------- printing splits -------')
		for split in details["splitSummaries"]:
			print(f'---------- printing split number {i} -------')
			print(f"  noOfSplits {split['noOfSplits']}:")
			print(f"  splitType {split['splitType']}:")
			print(f"  averageSpeed {split['averageSpeed']}:")
			print(f"  Distance: {split['distance']} meters")
			print(f"  Duration: {split['duration']} seconds")
			print(f"  Ascent: {split['elevationGain']} meters")
			i += 1
	else:
		print('---------No splits---------')
