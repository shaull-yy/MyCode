
def are_lists_same(list1, list2, check_vals_and_order): #Return values: False - not same, 
												#				True - same values (checking values only, or vals and order of element by the last argument)
												#check_vals_and_order arguments: True - Check that lists are same by values and order of elements, 
												# 								 False - Check that lists are same by values only (cane be in diferent order)
	lists_same_not_inc_order = True
	lists_same_inc_order = True

	if len(list1) != len(list2):
		return False
	if list1 == list2:
		return True
	if check_vals_and_order:  # after the above if's, it is clear that the lists are not the same by vals and order
		return False
	# checking if lists have same elements
	for x in list1:
		if x not in list2:
			return False
	return True


import os
import glob
import time
from datetime import datetime, timedelta

def clean_files_keep_x_recent(folder_path, file_name_pattern, keep_x_files, only_b4_x_days):
	# Arguments:
	# file_name_pattern should be like 'trans_file_*.xlsx'
	# keep_x_files - we delete all files and keeping "keep_x_files" most recent files
	# only_b4_x_days - In addition to above condition, we only delete files that were modified "only_b4_x_days" days ago

	del_count = 0
	if folder_path == '':
		file_pattern = file_name_pattern
	else:
	# Get all files matching the pattern
		file_pattern = os.path.join(folder_path, file_name_pattern)
	
	# Get the current time and calculate the cutoff time (12 days ago) 
	cutoff_time = time.time() - (only_b4_x_days * 24 * 60 * 60) # 12 * 24 * 60 * 60 is 12 deys in minutes

	files = glob.glob(file_pattern)
	
	# Filter files based on modification time older than 12 days
	files = [file for file in files if os.path.getmtime(file) < cutoff_time]
	# Sort files by modification time (newest first)
	files_sorted = sorted(files, key=os.path.getmtime, reverse=True)

	# Keep the last keep_x_files files
	files_to_delete = files_sorted[keep_x_files:]

	# Delete the remaining files
	for file in files_to_delete:
		try:
			os.remove(file)
			del_count += 1
			print(f"File : {file} was deleted")
		except Exception as e:
			print(f"Error deleting {file}: {e}")

	print(f"Cleanup completed.  {del_count} files were deleted")
	return del_count


if __name__ == '__main__':
	list1 = [1,2,3,4,5]
	list2 = [1,2,3,4,5]
	list3 = [5,4,3,2,1]
	list4 = [1,2,3,4,5,6]

	print('--------------')
	print(are_lists_same(list1,list3,True))
	print(are_lists_same(list1,list3,False))
