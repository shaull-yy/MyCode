import pandas as pd
import os
from datetime import datetime
from openpyxl import load_workbook

log_flag = False
total_files = 0
total_renamed = 0
# Instructions. Input file should be an excel with one worsheet
# Column with name "Folder Name" must have the folder path and it must end with / (like: C:\_Shaul\Python\_My_Code\Tools\)
# Column with name "File Name" must have the OLD file name (like: text1.txt)
# Column with name "New File Name" must have the New file name (like: text1_new.txt)

def rename_one_file(old_file_name, new_file_name):
	status = ""
	old_file_exists = os.path.exists(old_file_name)
	new_file_exists = os.path.exists(new_file_name)
	if old_file_exists == True and new_file_exists == False:
		os.rename(old_file_name,new_file_name)
		status = "OK"
	else:
		if old_file_exists == False:
			print(f'>> Error - Old file notfound, file name is: {old_file_name}')
			status = '>> Error - Old file notfound'
		if new_file_exists == True:
			print(f'>> Error - New file exists, file name is: {new_file_name}')
			if status == "":
				status = '>> Error - New file exists'
			else:
				status = status + " | " + ">> Error - New file exists"
	return status

# Main
input_file_name = 'C:/_Shaul/Python/_My_Code/Tools/Renam_Files_Test_File.xlsx'
input_file = pd.read_excel(input_file_name)
logging_data = pd.DataFrame(columns=['Folder Path', 'Old File', 'New File', 'Rename Status'])
logging_data_ix = 0
#input_file.head()
input_file2 = pd.DataFrame()
#input_file2['Full File Name'] = input_file['Full File Name']
input_file2['Folder Name'] = input_file['Folder Name']
input_file2['Old Full File Name'] = input_file['Folder Name'] + input_file['File Name']
input_file2['New File Name'] = input_file['New File Name']
if log_flag == True:
	print(input_file2.head())

for xl_row in input_file2.itertuples(index=False):
	#print(xl_row[0],xl_row[1],xl_row[2],xl_row[3])
	total_files += 1
	folder_path = xl_row[0]
	old_file_name = xl_row[1]
	new_file_name = xl_row[2]
	if log_flag == True:
		print(f"Old: {old_file_name}    New: {new_file_name}")
	rename_status = rename_one_file(old_file_name, new_file_name)
	if rename_status == 'OK':
		total_renamed += 1
	logging_data.loc[logging_data_ix] = [folder_path, old_file_name, new_file_name, rename_status]
	logging_data_ix += 1

now=datetime.now()
logging_data.loc[logging_data_ix] = ['Date: '+ now.strftime("%A, %B %d, %Y"),'','','']   # format: "Friday, April 18, 2025"
logging_data_file_name = input_file_name
dot_position = input_file_name.rfind('.')
logging_data_file_name = input_file_name[:dot_position] + '_LOG' + input_file_name[dot_position:]
logging_data.to_excel(logging_data_file_name, index=False)

wb = load_workbook(logging_data_file_name)
ws = wb.active
for col in ws.columns:
    max_length = max(len(str(cell.value)) for cell in col if cell.value)  # Find longest cell
    col_letter = col[0].column_letter  # Get column letter
    ws.column_dimensions[col_letter].width = max_length + 2  # Adjust width

wb.save(logging_data_file_name)
#print("Excel file saved with adjusted column widths!")
os.startfile(logging_data_file_name)

print(f'\nProgram ended succesfully\nTotal Files in input file: {total_files} \nTotal files renames: {total_renamed}')
print(f'\nProgram used the following input file: {input_file_name}')
print(f'The ""log_flag"" flag is set to {log_flag} ')
print(f'The log file with rename status is in file: {logging_data_file_name} ')