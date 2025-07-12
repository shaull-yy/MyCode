
import pandas as pd
from ortools.sat.python import cp_model
from collections import defaultdict
import random

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
HOURS = [1, 2, 3, 4, 5, 6, 7]
CLASSROOMS = ['Room A', 'Room B', 'Room C']

classes = {
	'class-1': {'math': 3, 'grammar': 4, 'physics': 5, 'chemistry': 4},
	'class-2': {'math': 4, 'grammar': 3, 'physics': 3, 'chemistry': 4},
	'class-3': {'math': 2, 'grammar': 3, 'physics': 6, 'chemistry': 4},
}

teachers = {
	'Shaul': {'subject': 'math', 'hours': 11},
	'Galit': {'subject': 'grammar', 'hours': 20},
	'Neta': {'subject': 'physics', 'hours': 15},
	'Yuval': {'subject': 'chemistry', 'hours': 12},
}

unavailable = {
	'Shaul': [('Sunday', i) for i in HOURS] + [('Monday', i) for i in HOURS],
	'Galit': [('Tuesday', i) for i in [1, 2, 3]],
	'Neta': [('Wednesday', i) for i in [6, 7]] + [('Thursday', i) for i in [1, 2, 3]],
	'Yuval': [('Monday', i) for i in [3, 4]] + [('Thursday', i) for i in [1, 2, 3]],
}

preferred_slots = {
	'Shaul': [('Wednesday', i) for i in [1, 2]],
	'Galit': [('Monday', i) for i in [1, 2]],
	'Neta': [('Tuesday', i) for i in [1, 2]],
	'Yuval': [('Wednesday', i) for i in [1, 2]],
}

def schedule_teachers(classes, teachers, unavailable):
	model = cp_model.CpModel()
	all_classes = list(classes.keys())
	all_subjects = set(subj for cl in classes.values() for subj in cl)
	all_teachers = teachers.keys()
	time_slots = [(day, hour) for day in DAYS for hour in HOURS]
	random.shuffle(time_slots)

	subject_to_teacher = {info['subject']: name for name, info in teachers.items()}
	teacher_to_subject = {name: info['subject'] for name, info in teachers.items()}

	assign = {}
	for c in all_classes:
		for day, hour in time_slots:
			for subject in all_subjects:
				assign[(c, day, hour, subject)] = model.NewBoolVar(f"{c}_{day}_{hour}_{subject}")

	classroom_used = {}
	for day, hour in time_slots:
		for room in CLASSROOMS:
			classroom_used[(day, hour, room)] = model.NewBoolVar(f"classroom_{day}_{hour}_{room}")

	for c in all_classes:
		for subject, hours in classes[c].items():
			model.Add(sum(assign[(c, d, h, subject)] for (d, h) in time_slots) == hours)

	for c in all_classes:
		for (d, h) in time_slots:
			model.Add(sum(assign[(c, d, h, s)] for s in all_subjects) <= 1)

	for t in all_teachers:
		subject = teacher_to_subject[t]
		for (d, h) in time_slots:
			model.Add(sum(assign[(c, d, h, subject)] for c in all_classes) <= 1)

	for t in all_teachers:
		subject = teacher_to_subject[t]
		for c in all_classes:
			for (d, h) in unavailable.get(t, []):
				model.Add(assign[(c, d, h, subject)] == 0)

	for t in all_teachers:
		subject = teacher_to_subject[t]
		model.Add(sum(assign[(c, d, h, subject)] for c in all_classes for (d, h) in time_slots) <= teachers[t]['hours'])

	for (d, h) in time_slots:
		model.Add(sum(assign[(c, d, h, s)] for c in all_classes for s in all_subjects) <= len(CLASSROOMS))

	late_hours = [6, 7]
	penalty_vars = []
	for t in all_teachers:
		subject = teacher_to_subject[t]
		for c in all_classes:
			for (d, h) in time_slots:
				if h in late_hours:
					v = assign[(c, d, h, subject)]
					penalty_vars.append(v)

	preferred_vars = []
	for t in all_teachers:
		subject = teacher_to_subject[t]
		prefs = preferred_slots.get(t, [])
		for c in all_classes:
			for (d, h) in prefs:
				if (d, h) in time_slots:
					v = assign[(c, d, h, subject)]
					preferred_vars.append(v)

	model.Maximize(sum(preferred_vars) - sum(penalty_vars))

	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
		print("❌ No feasible solution found.")
		return None

	schedule = defaultdict(lambda: defaultdict(str))
	for c in all_classes:
		for (d, h) in time_slots:
			for s in all_subjects:
				if solver.Value(assign[(c, d, h, s)]):
					schedule[c][(d, h)] = f"{s} ({subject_to_teacher[s]})"
	return schedule

def export_to_excel(schedule, filename="class_schedule.xlsx"):
	writer = pd.ExcelWriter(filename, engine='xlsxwriter')
	for c, slots in schedule.items():
		rows = []
		for day in DAYS:
			row = []
			for h in HOURS:
				row.append(slots.get((day, h), '---'))
			rows.append(row)
		df = pd.DataFrame(rows, index=DAYS, columns=[f"Hour {h}" for h in HOURS])
		df.to_excel(writer, sheet_name=c)
	writer.close()
	print(f"✅ Schedule exported to: {filename}")

if __name__ == "__main__":
	schedule = schedule_teachers(classes, teachers, unavailable)
	if schedule:
		export_to_excel(schedule)
	else:
		print("Scheduling failed.")
