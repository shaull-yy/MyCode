import csv
#from contextlib import nullcontext

input_file_name = 'C:\\_Shaul\\Python\\Garmin_Data_A.csv'
record_file_name = 'C:\\_Shaul\\Python\\Garmin_Records_A.csv'
run_data_lst = [[0, 0]]
istart = 0
iend = 0
leg_length = 1000  # in meters
leg_length_variance = 25000 / (60 * 60) / 2 # variance is the distance the runner runs in 1 sec at velocity of 25km/hr divided by 2
print()
print('leg_length_variance:', leg_length_variance)

data_file = open(input_file_name, 'rt')

# Loaf file into run_data_lst list
i = -1
csvFile = csv.reader(data_file)
for lines in csvFile:
	i = i + 1
	if i == 0:
		continue
	lines[0] = float(lines[0])
	lines[1] = float(lines[1])
	run_data_lst.append(lines)

data_file.close()

lenx = len(run_data_lst)
print('run_data_lst size:',lenx)
# print(run_data_lst)

def calc_leg():
	global istart
	global iend
	stop_for = False
	for iend in range(istart + 1, lenx ):
		#breakpoint()
		if istart == 298 and iend == 299:
			zz = 1 + 1
		leg_dist = run_data_lst[iend][1] - run_data_lst[istart][1]
		if leg_dist >= (leg_length - leg_length_variance)  or leg_dist >= leg_length:
			stop_for = True
			time_length = run_data_lst[iend][0] - run_data_lst[istart][0]
			return leg_dist, time_length
	return -1, -1



x, y = calc_leg()
print("First leg calc:","\n> Start index:", istart, "\n> End Index:", iend, "\n> Leg length", x, "\n> Time Length", y)

record_lst = []
for i in range(len(run_data_lst) -1):
	istart = i
	x, y = calc_leg()
	if x != -1:
		record_lst.append([istart, iend, x, y])

print('Num records in "record_lst":', len(record_lst))
fastest_1km = min(record_lst, key=lambda x: x[3] )
print('\nFasterst 1 km pace is', round(fastest_1km[3] / 60 ,2))

#print(record_lst)
#exit()

with open(record_file_name, 'w', newline='') as file:
	file_writer = csv.writer(file)
	file_writer.writerows(record_lst)

