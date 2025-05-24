import sys

class my_logging:

    # Constructor method (runs when an object is created)
    def __init__(self, show_validation_info):
        self.show_validation_info = show_validation_info #True will print validation messages, False will not print them  
        self.err_level = ''
        self.msg_text = ''
        self.validation_command = ''
        self.errors_count = 0
        self.warnings_count = 0
        self.info_count = 0
        self.validation_count = 0
        self.fatal_count = 0

    # Method
    def print_message(self, err_level, msg_text, validation_command=''):  
        self.err_level = err_level  #Valuse are: I - INFO, W - WRNING, E - ERROR, V - Validation, F - Fatal error message + statistics & trminating program
        self.msg_text = msg_text
        self.validation_command = validation_command
        #validation_command=''
        if self.show_validation_info == True and self.err_level == 'V':
            print('>>>Validation: ' + self.msg_text)
            if self.validation_command != "":
                self.validation_command()
                self.validation_count +=1
        elif err_level == 'I':
            print('>>>Info: ' + self.msg_text)
            self.info_count +=1
        elif self.err_level == 'W':
            print('>>>Wrning: ' + self.msg_text)
            self.warnings_count +=1
        elif self.err_level == 'E':
            print('\n>>>ERROR>>>:\n' + self.msg_text)
            print()
            self.errors_count +=1
        elif self.err_level == 'F':
            print('\n>>>FATAL ERROR - Aborting>>>:\n' + self.msg_text)
            print()
            self.fatal_count += 1
            self.print_statistics('Y')
            sys.exit(1)
    
    def print_statistics(self, aborting_ind='N'):
        print()
        print('Messages Statistics:')
        print(f'  Number of Error messages:      {self.errors_count}')
        print(f'  Number of Warning messages:    {self.warnings_count}')
        print(f'  Number of Info messages:       {self.info_count}')
        print(f'  Number of Validation messages: {self.validation_count}')
        print(f'  Number of Fatal messages:      {self.fatal_count}')
        if aborting_ind != 'Y':
            print('End of Messages Statistics')
        else:
            print('Aborting - Program ended due to FATAL Error')
