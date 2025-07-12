
import pandas as pd
from ortools.sat.python import cp_model
from collections import defaultdict
import random

# Load input from Excel
INPUT_FILE = "file:///C:/_Shaul/Projects/_My_Code/code/scheduling_inputs.xlsx"

def load_input():
	xl = pd.read_excel(INPUT_FILE, sheet_name=None)

	# Load base data
	days_hours = list(zip(xl["DaysHours"]["Day"], xl["DaysHours"]["Hour"]))
	classrooms = xl["Classrooms"]["Classroom"].tolist()

	# Load classes and subjects
	df_classes = xl["Classes"]
	classes = defaultdict(dict)
	for _, row in df_classes.iterrows():
		classes[row["Class"]][row["Subject"]] = int(row["Hours"])

	# Load teachers
	df_teachers = xl["Teachers"]
	teachers = {}
	for _, row in df_teachers.iterrows():
		teachers[row["Teacher"]] = {
			"subject": row["Subject"],
			"hours": int(row["Weekly Hours"])
		}

	# Load unavailability
	df_unavailable = xl["Unavailability"]
	unavailable = defaultdict(list)
	for _, row in df_unavailable.iterrows():
		unavailable[row["Teacher"]].append((row["Day"], int(row["Hour"])))

	# Load preferences
	df_preferences = xl["Preferences"]
	preferred_slots = defaultdict(list)
	for _, row in df_preferences.iterrows():
		preferred_slots[row["Teacher"]].append((row["Day"], int(row["Hour"])))

	return days_hours, classrooms, classes, teachers, unavailable, preferred_slots

def schedule_teachers(days_hours, classrooms, classes, teachers, unavailable, preferred_slots):
	model = cp_model.CpModel()
	all_classes = list(classes.keys())
	all_subjects = set(subj for cl in classes.values() for subj in cl)
	all_teachers = teachers.keys()
	random.shuffle(days_hours)  # add randomness

	subject_to_teacher = {info['subject']: name for name, info in teachers.items()}
	teacher_to_subject = {name: info['subject'] for name, info in teachers.items()}

	# Assignment variables
	assign = {}
	for c in all_classes:
		for day, hour in days_hours:
			for subject in all_subjects:
				assign[(c, day, hour, subject)] = model.NewBoolVar(f"{c}_{day}_{hour}_{subject}")

	# Each class gets required hours
	for c in all_classes:
		for subject, hours in classes[c].items():
			model.Add(sum(assign[(c, d, h, subject)] for (d, h) in days_hours) == hours)

	# No double-booking within a class
	for c in all_classes:
		for (d, h) in days_hours:
			model.Add(sum(assign[(c, d, h, s)] for s in all_subjects) <= 1)

	# No teacher teaches two classes at once
	for t in all_teachers:
		subject = teacher_to_subject[t]
		for (d, h) in days_hours:
			model.Add(sum(assign[(c, d, h, subject)] for c in all_classes) <= 1)

	# Unavailable time restrictions
	for t in all_teachers:
		subject = teacher_to_subject[t]
		for c in all_classes:
			for (d, h) in unavailable.get(t, []):
				model.Add(assign[(c, d, h, subject)] == 0)

	# Weekly teaching limit
	for t in all_teachers:
		subject = teacher_to_subject[t]
		model.Add(sum(assign[(c, d, h, subject)] for c in all_classes for (d, h) in days_hours) <= teachers[t]['hours'])

	# Classroom capacity
	for (d, h) in days_hours:
		model.Add(sum(assign[(c, d, h, s)] for c in all_classes for s in all_subjects) <= len(classrooms))

	# Late hour penalty
	late_hours = [6, 7]
	penalty_vars = []
	for t in all_teachers:
		subject = teacher_to_subject[t]
		for c in all_classes:
			for (d, h) in days_hours:
				if h in late_hours:
					v = assign[(c, d, h, subject)]
					penalty_vars.append(v)

	# Preferred slot bonus
	preferred_vars = []
	for t in all_teachers:
		subject = teacher_to_subject[t]
		prefs = preferred_slots.get(t, [])
		for c in all_classes:
			for (d, h) in prefs:
				if (d, h) in days_hours:
					v = assign[(c, d, h, subject)]
					preferred_vars.append(v)

	model.Maximize(sum(preferred_vars) - sum(penalty_vars))

	# Solve
	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
		print("❌ No feasible solution found.")
		return None

	schedule = defaultdict(lambda: defaultdict(str))
	for c in all_classes:
		for (d, h) in days_hours:
			for s in all_subjects:
				if solver.Value(assign[(c, d, h, s)]):
					schedule[c][(d, h)] = f"{s} ({subject_to_teacher[s]})"
	return schedule

def export_to_excel(schedule, filename="class_schedule.xlsx"):
	writer = pd.ExcelWriter(filename, engine='xlsxwriter')
	hours = sorted(set(h for (_, h) in next(iter(schedule.values())).keys()))
	for c, slots in schedule.items():
		rows = []
		days = sorted(set(d for (d, _) in slots))
		for day in days:
			row = [slots.get((day, h), '---') for h in hours]
			rows.append(row)
		df = pd.DataFrame(rows, index=days, columns=[f"Hour {h}" for h in hours])
		df.to_excel(writer, sheet_name=c)
	writer.close()
	print(f"✅ Schedule exported to: {filename}")

if __name__ == "__main__":
	days_hours, classrooms, classes, teachers, unavailable, preferred_slots = load_input()
	schedule = schedule_teachers(days_hours, classrooms, classes, teachers, unavailable, preferred_slots)
	if schedule:
		export_to_excel(schedule)
	else:
		print("Scheduling failed.")
