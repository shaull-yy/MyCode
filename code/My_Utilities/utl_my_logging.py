import sys
import time
from datetime import timedelta, datetime

class my_logging:

	# Constructor method (runs when an object is created)
	def __init__(self, show_validation_info, main_file_name=''):
		self.start_time = time.time()
		self.show_validation_info = show_validation_info #True will print validation messages, False will not print them  
		self.err_level = ''
		self.msg_text = ''
		self.validation_command = ''
		self.errors_count = 0
		self.warnings_count = 0
		self.info_count = 0
		self.validation_count = 0
		self.fatal_count = 0
		self.take_action_count = 0
		self.prefix_len = 11
		self.delimiter1 = ' - ' 
		self.delimiter1_len = 3
		self.main_file_name = main_file_name
		self.log_file_name = ''
		self.upd_log_file = False
		self.font_colors_dict = {'black': '\033[0m', 
							'red': '\033[31m', 
							'green': '\033[32m',
							'yellow': '\033[33m',
							'blue': '\033[34m',
							'magenta': '\033[35m',
							'cyan': '\033[36m'
							}
		self.font_colors = self.font_colors_dict['black']
		self.check_duration_start_time = 0

	def time_and_run_duration(self, debug_start_time_arg=None):
		end_time = time.time()
		
		if debug_start_time_arg == None:
			run_duration_seconds = end_time - self.start_time
			formated_end_time = datetime.fromtimestamp(end_time).strftime("%d-%b-%Y %H:%M:%S") + ' / '
		else:
			run_duration_seconds = end_time - debug_start_time_arg
			formated_end_time = ''
		run_duration = str(timedelta(seconds=int(run_duration_seconds))) # Convert to hh:mm:ss format
		
		return formated_end_time + run_duration
	
	def open_log_file(self, log_file_name):
		if log_file_name:
			self.log_file_name = log_file_name
			self.log_file = open(self.log_file_name, 'w')
			txt = self.format_str_with_dots(' ', 4, 'File', 15, self.main_file_name, '.')
			self.log_file.write(txt + '\n')
			txt = time.time()
			txt = datetime.fromtimestamp(txt).strftime('%d-%b-%Y %H:%M:%S')
			txt = self.format_str_with_dots(' ', 4, 'Start Time', 15, txt, '.')
			self.log_file.write(txt + '\n')
			self.upd_log_file = True
	
	def close_log_file(self):
		if self.upd_log_file: # this means that the log file was opened
			self.upd_log_file = False
			if not self.log_file.close():  # making sure the file is open
				self.log_file.close()

	def print_terminal_log(self, txt=''):
		txt = self.font_colors + txt + self.font_colors_dict['black']
		print(txt)
		if self.upd_log_file:
			self.log_file.write(txt + '\n')

	def format_str_with_dots(self, pad_b4_text1_str_val, pad_b4_text1_count, text1, print_col_2_position, text2, pad_after_text1_val='.'):
		if isinstance(text1, str) == False: text1 = f'{text1: ,}'
		if isinstance(text2, str) == False: text2 = f'{text2: ,}'
		text1 = ' ' + text1 + ' '
		text2 = ' ' + text2 + ' '
		rslt = pad_b4_text1_str_val * pad_b4_text1_count
		rslt = rslt + text1
		fill_by_dots_len = print_col_2_position - len(rslt)
		if fill_by_dots_len > 0:
			rslt = rslt + pad_after_text1_val * fill_by_dots_len
		else:
			rslt = rslt + ' '
		rslt = rslt + text2
		return rslt

	def print_running_statistics(self, list_of_text, list_of_Values, print_col_2_position=0):
		if print_col_2_position == 0:
			print_col_2_position = max(len(s) for s in list_of_text) + 6
			if print_col_2_position > 130:
				print_col_2_position = 130
				
		self.font_colors = self.font_colors_dict['black']
		# end_time = time.time()
		# formated_end_time = datetime.fromtimestamp(end_time).strftime('"%d-%b-%Y %H:%M:%S"')
		# run_duration_seconds = end_time - self.start_time
		# run_duration = str(timedelta(seconds=int(run_duration_seconds))) # Convert to hh:mm:ss format
		# time_stamp_duration = formated_end_time + ' / ' + run_duration
		time_stamp_duration = self.time_and_run_duration()
		self.print_terminal_log()
		self.print_terminal_log(self.format_str_with_dots('=', 4, 'Running Statistics', print_col_2_position, '','='))
		for msg, val in zip(list_of_text, list_of_Values):
			self.print_terminal_log(self.format_str_with_dots('-', 2, msg, print_col_2_position, val, '.'))
		self.print_terminal_log(self.format_str_with_dots(' ', 4, 'Time / Rund Duration (HH:MM:SS)', print_col_2_position, time_stamp_duration, '.'))
		#self.print_terminal_log(self.format_str_with_dots('=', 4, 'End of Running Statistics', print_col_2_position, ' ', '='))
		self.print_terminal_log()


	def print_msg_statistics(self):
		self.font_colors = self.font_colors_dict['black']
		prefix_length = 50
		# end_time = time.time()
		# formated_end_time = datetime.fromtimestamp(end_time).strftime('"%d-%b-%Y %H:%M:%S"')
		# run_duration_seconds = end_time - self.start_time
		# run_duration = str(timedelta(seconds=int(run_duration_seconds))) # Convert to hh:mm:ss format
		# time_stamp_duration = formated_end_time + ' / ' + run_duration
		time_stamp_duration = self.time_and_run_duration()
		self.print_terminal_log()
		self.print_terminal_log(self.format_str_with_dots('=', 4, 'Messages Statistics', prefix_length, '='))
		self.print_terminal_log(self.format_str_with_dots('-', 4, 'Number of Error messages', prefix_length, self.errors_count))
		self.print_terminal_log(self.format_str_with_dots('-', 4, 'Number of Warning messages', prefix_length, self.warnings_count))
		self.print_terminal_log(self.format_str_with_dots('-', 4, 'Number of Info messages', prefix_length, self.info_count))
		self.print_terminal_log(self.format_str_with_dots('-', 4, 'Number of Validation messages', prefix_length, self.validation_count))
		self.print_terminal_log(self.format_str_with_dots('-', 4, 'Number of User Take Action msg', prefix_length, self.take_action_count))
		self.print_terminal_log(self.format_str_with_dots('-', 4, 'Number of Fatal messages', prefix_length, self.fatal_count))
		self.print_terminal_log(self.format_str_with_dots(' ', 4, 'Time / Run Duration (HH:MM:SS)', prefix_length, time_stamp_duration, '.'))
		#self.print_terminal_log(self.format_str_with_dots('=', 4, 'End Messages Statistics', prefix_length, ' ', '='))
		self.print_terminal_log()

	def start_program_msg(self):
		formated_end_time = datetime.fromtimestamp(self.start_time).strftime('"%d-%b-%Y %H:%M:%S"')
		self.print_terminal_log()
		self.print_terminal_log(self.format_str_with_dots('=', 4, 'Start Running Program', 50,' ', '='))
		self.print_terminal_log(self.format_str_with_dots(' ', 4, 'File', 15, self.main_file_name, '.'))
		self.print_terminal_log(self.format_str_with_dots(' ', 4, 'Time', 15, formated_end_time, '.'))
		self.print_terminal_log()

	def stop_program_msg(self, aborting_ind='N'):
		self.font_colors = self.font_colors_dict['black']
		self.print_terminal_log()
		self.print_terminal_log('Program Ends - Summary')
		self.print_terminal_log(self.format_str_with_dots(' ', 4, 'File', 15, self.main_file_name, '.'))
		self.print_msg_statistics()
		if aborting_ind != 'Y':
			self.font_colors = self.font_colors_dict['green']
			self.print_terminal_log(self.format_str_with_dots('=', 4, 'Program Ended Successfully', 50,' ', '='))
			self.close_log_file()
		else:
			self.font_colors = self.font_colors_dict['red']
			self.print_terminal_log(self.format_str_with_dots('=', 4, 'ABORTING - Program Ended Due To a FATAL Error', 50,' ', '='))
			self.close_log_file()
			sys.exit(1)
		
		
		


	def print_message(self, err_level, msg_text, validation_command=''):  
		self.err_level = err_level  #Valuse are: I - INFO, W - WRNING, E - ERROR, V - Validation, 
									#F - Fatal error message + statistics & trminating program, A - User to take an action message S - Statistics
		self.msg_text = msg_text
		self.validation_command = validation_command
		prefix_length = self.prefix_len
		msg_prefix = ''
		msg_newline_before = False
		msg_newline_after = False
		self.font_colors = self.font_colors_dict['black']
		
		if self.err_level == 'V':
			if self.show_validation_info == True:
				msg_prefix='>>>Validation'
				self.validation_count +=1
			else:
				return
		elif err_level == 'I':
			msg_prefix = '>>>Info'
			self.info_count +=1
		elif self.err_level == 'W':
			msg_prefix = '>>>Warning'
			self.warnings_count +=1
		elif self.err_level == 'E':
			msg_prefix = '>>>ERROR>>>'
			msg_newline_before = True
			msg_newline_after = True
			self.errors_count +=1
			self.font_colors = self.font_colors_dict['yellow']
		elif self.err_level == 'A':
			msg_prefix = ''
			msg_newline_before = True
			self.take_action_count += 1
			self.font_colors = self.font_colors_dict['green']
		elif self.err_level == 'F':
			msg_newline_before = True
			msg_newline_after = True
			msg_prefix = '>>>FATAL ERROR - Aborting>>>'
			self.fatal_count += 1
			self.font_colors = self.font_colors_dict['red']
		elif self.err_level == 'S':
			msg_prefix = '>>>Statistics'
			msg_newline_before = True
		elif self.err_level == 'D-S':
			msg_prefix = '>>>Debugging, Duration-Check-Start'
			self.check_duration_start_time = time.time()
		elif self.err_level == 'D-E':
			time_stamp_duration = self.time_and_run_duration(self.check_duration_start_time)
			msg_prefix = '>>>Debugging, Duration-Check-End>> ' + time_stamp_duration
		
		if msg_newline_before: self.print_terminal_log()
		if self.err_level == 'A':
			self.print_terminal_log('>>>Action - User to take an action...')
			prefix_length = 2
			msg_prefix = ''
		if self.err_level == 'D-E':
			pass  #do not set the msg_prefix in this case
		elif msg_prefix != '':
			time_stamp_duration = self.time_and_run_duration()
			msg_prefix = msg_prefix + ' (Time/RunDuration ' + time_stamp_duration + ') '
		self.print_terminal_log(f'{msg_prefix:<{prefix_length}}{self.delimiter1:<{self.delimiter1_len}} {self.msg_text}')  #
		if msg_newline_after: self.print_terminal_log()
		if self.validation_command != "":
			self.validation_command()
			self.print_terminal_log()
		if self.err_level == 'S': self.print_msg_statistics()
		if self.err_level == 'F': self.stop_program_msg('Y')
			

if __name__ == '__main__':
	my_logging_test = my_logging(False)
	
	my_logging_test.start_program_msg()
	my_logging_test.stop_program_msg()
	test_str = 'Test xxx yyy ppppppppppppppppppppppppppppppppppppppppppppppppppp'
	my_logging_test.print_message('I', test_str, '')
	my_logging_test.print_message('W', test_str, '')
	my_logging_test.print_message('I', test_str, '')
	my_logging_test.print_message('V', test_str, '')
	my_logging_test.print_message('E', test_str, '')
	my_logging_test.print_message('I', test_str, '')
	my_logging_test.print_message('A', test_str, '')
	my_logging_test.print_message('I', test_str, '')
	my_logging_test.print_message('S', test_str, '')
	
	list_of_text = ['aaa', 'bbbbb', 'ccccc'] 
	list_of_Values = [1000,200,300000]
	my_logging_test.print_running_statistics(list_of_text, list_of_Values, 40)

	my_logging_test.print_message('F', test_str, '')