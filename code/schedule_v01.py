import random
from collections import defaultdict

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
HOURS_PER_DAY = 7  # time slots 1 to 7

# Sample Inputs
classes = {
	'class-1': {'math': 3, 'grammar': 4, 'physics': 5, 'chemistry': 4},
}

teachers = {
	'Shaul': {'subject': 'math', 'hours': 11},
	'Galit': {'subject': 'grammar', 'hours': 20},
	'Neta': {'subject': 'physics', 'hours': 15},
	'Yuval': {'subject': 'chemistry', 'hours': 12},
}

unavailable = {
	'Shaul': [('Sunday', i) for i in range(1, 8)] + [('Monday', i) for i in range(1, 8)],
	'Galit': [('Tuesday', i) for i in [1, 2, 3]],
	'Neta': [('Wednesday', i) for i in [6, 7]] + [('Thursday', i) for i in [1, 2, 3]],
	'Yuval': [('Monday', i) for i in [3, 4]] + [('Thursday', i) for i in [1, 2, 3]],
}


def build_teacher_schedule(teachers, unavailable):
	schedule = {}
	for name in teachers:
		unavail = set(unavailable.get(name, []))
		avail_slots = []
		for day in DAYS:
			for hour in range(1, HOURS_PER_DAY + 1):
				if (day, hour) not in unavail:
					avail_slots.append((day, hour))
		schedule[name] = avail_slots
	return schedule


def assign_schedule(classes, teachers, unavailable):
	teacher_schedule = build_teacher_schedule(teachers, unavailable)
	final_schedule = defaultdict(lambda: defaultdict(str))  # class -> (day, hour) -> teacher/subject

	for class_name, subjects in classes.items():
		assigned_slots = set()
		for subject, hours_needed in subjects.items():
			# find the teacher who teaches this subject
			teacher = next((t for t, info in teachers.items() if info['subject'] == subject), None)
			if not teacher:
				print(f"No teacher found for subject: {subject}")
				continue

			available = teacher_schedule[teacher]
			teacher_hours_left = teachers[teacher]['hours']

			random.shuffle(available)  # randomize to avoid biased early allocation

			hours_assigned = 0
			for slot in available:
				if slot in assigned_slots:
					continue
				if hours_assigned >= hours_needed or teacher_hours_left <= 0:
					break

				final_schedule[class_name][slot] = f'{subject} ({teacher})'
				assigned_slots.add(slot)
				hours_assigned += 1
				teacher_hours_left -= 1

			teachers[teacher]['hours'] = teacher_hours_left

	return final_schedule


def print_schedule(schedule):
	for class_name, slots in schedule.items():
		print(f'\nSchedule for {class_name}')
		for day in DAYS:
			print(f'{day}: ', end='')
			for hour in range(1, HOURS_PER_DAY + 1):
				slot = (day, hour)
				subject_info = slots.get(slot, '---')
				print(f'{hour}:{subject_info:<20}', end=' | ')
			print()


# Run the scheduling
schedule = assign_schedule(classes, teachers, unavailable)
print_schedule(schedule)
