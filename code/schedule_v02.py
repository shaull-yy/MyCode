from ortools.sat.python import cp_model
from collections import defaultdict

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
HOURS = [1, 2, 3, 4, 5, 6, 7]

# Define input
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


def schedule_teachers(classes, teachers, unavailable):
	model = cp_model.CpModel()
	all_classes = list(classes.keys())
	all_subjects = set(subj for cl in classes.values() for subj in cl)
	all_teachers = teachers.keys()

	# Create teacher mapping
	subject_to_teacher = {info['subject']: name for name, info in teachers.items()}

	# Slot mapping
	time_slots = [(day, hour) for day in DAYS for hour in HOURS]

	# Create variables: (class, day, hour, subject) -> 1 if assigned
	assign = {}
	for c in all_classes:
		for day, hour in time_slots:
			for subject in all_subjects:
				assign[(c, day, hour, subject)] = model.NewBoolVar(f"{c}_{day}_{hour}_{subject}")

	# Constraint 1: Each class gets the required number of hours for each subject
	for c in all_classes:
		for subject, hours in classes[c].items():
			model.Add(
				sum(assign[(c, d, h, subject)] for (d, h) in time_slots) == hours
			)

	# Constraint 2: Each class has at most one subject per slot
	for c in all_classes:
		for (d, h) in time_slots:
			model.Add(
				sum(assign[(c, d, h, s)] for s in all_subjects) <= 1
			)

	# Constraint 3: No teacher is double-booked
	for t in all_teachers:
		subject = teachers[t]['subject']
		for (d, h) in time_slots:
			model.Add(
				sum(assign[(c, d, h, subject)] for c in all_classes) <= 1
			)

	# Constraint 4: Teachers only teach when available
	for t in all_teachers:
		subject = teachers[t]['subject']
		unav = set(unavailable.get(t, []))
		for c in all_classes:
			for (d, h) in unav:
				model.Add(assign[(c, d, h, subject)] == 0)

	# Constraint 5: Teacher total hours limit
	for t in all_teachers:
		subject = teachers[t]['subject']
		model.Add(
			sum(assign[(c, d, h, subject)] for c in all_classes for (d, h) in time_slots)
			<= teachers[t]['hours']
		)

	# Solve
	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
		print("❌ No feasible solution found.")
		return

	# Format output
	schedule = defaultdict(lambda: defaultdict(str))
	for c in all_classes:
		for (d, h) in time_slots:
			for s in all_subjects:
				if solver.Value(assign[(c, d, h, s)]):
					schedule[c][(d, h)] = f"{s} ({subject_to_teacher[s]})"

	# Print
	for c in all_classes:
		print(f"\n📘 Schedule for {c}")
		for day in DAYS:
			print(f"{day:>9}: ", end='')
			for h in HOURS:
				cls = schedule[c].get((day, h), "---")
				print(f"{h}:{cls:<18}", end=' | ')
			print()


# Run
schedule_teachers(classes, teachers, unavailable)
