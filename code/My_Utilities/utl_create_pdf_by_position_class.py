from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
import os
import sys

class CreatePDF:
	def __init__(self, output_path, background_ind = False):
		self.width, self.height = letter
		self.line_height = 16 
		self.y_last_written_line = self.height - 50 + self.line_height #self.y_last_written_line: keep last y coordinate fo rnext line written to the pdf
		self.font_size = 12  # Font size
		self.c = canvas.Canvas(output_path, pagesize=letter)
		self.background_ind = background_ind
		self.available_colors = {
			"red": colors.red,
			"yellow": colors.yellow,
			"blue": colors.blue,
			"green": colors.green,
			"black": colors.black,
			"white": colors.white,
			"purple": colors.purple,
			"cyan": colors.cyan,
			"magenta": colors.magenta,
			"orange": colors.orange,
			"pink": colors.pink,
			"brown": colors.brown,
			"gray": colors.gray,
			"lightgray": colors.lightgrey,
			"darkgray": colors.darkgrey,
		}
	
	def handle_position_arg(self, highlight_positions):
	#accept only list or integer as argument
		if not (isinstance(highlight_positions, list) or isinstance(highlight_positions, int)):
			print(f'Aborting - The "highlight_positions" arguments is invalid, it should be a list or an integer. \nArgument value is {highlight_positions} \n Argument type is {type(highlight_positions)}')
			sys.exit(1)
		else:
			if isinstance(highlight_positions, int):
				highlight_positions = [highlight_positions]
	#Reduce 1 from each position since python index starts from 0 not 1
		tmp_lst= []
		for num in highlight_positions:
			tmp_num = num - 1
			tmp_lst.append(tmp_num)
		return tmp_lst

	def print_string_to_pdf(self, text, highlight_positions): 
		
		highlight_positions = self.handle_position_arg(highlight_positions)
		x, y = 50, self.y_last_written_line
		y -= self.line_height  # advance to the next line
		if y < 50:  # Start a new page if reaching bottom margin
				self.c.showPage()
				x, y = 50, self.height - 50
				self.y_last_written_line = y
		
		font = pdfmetrics.getFont("Helvetica")
		self.c.setFont("Helvetica", self.font_size)
		
		for i, char in enumerate(text):
			if x > self.width - 50:  # Wrap text to the next line
				x = 50
				y -= self.line_height
			
			if y < 50:  # Start a new page if reaching bottom margin
				self.c.showPage()
				x, y = 50, self.height - 50
			
			char_width = self.c.stringWidth(char, "Helvetica", self.font_size)
			font_ascent = font.face.ascent * (self.font_size / 1000)  # Scale ascent by font size
			font_descent = font.face.descent * (self.font_size / 1000)  # Scale descent by font size
			char_height = font_ascent - font_descent  # Approximate character height
			#char_height = self.c._font.fontHeight(char)
			
			if i in highlight_positions:
				if self.background_ind:
					# Adjusted yellow rectangle alignment and dimensions
					self.c.setFillColor(self.available_colors["yellow"])
					rect_padding = 1
					rect_height = char_height # self.font_size # + rect_padding # * 2
					self.c.rect(
						x - rect_padding, 
						y - rect_padding, 
						char_width + rect_padding * 2, 
						rect_height, 
						fill=1, 
						stroke=0
					)
				
				self.c.setFillColor(self.available_colors["red"])
				self.c.setFont("Helvetica-Bold", self.font_size)
			else:
				self.c.setFillColor(self.available_colors["black"])
				self.c.setFont("Helvetica", self.font_size)
			
			self.c.drawString(x, y, char)
			x += char_width
		
		self.y_last_written_line = y
				
	def save_pdf(self):
		self.c.save()
	
def replace_chars(dna_seq, pos, alternate):
	if pos < 1 or pos > len(dna_seq):
		print(f'invalid postion - position value {pos} is invalid')
		return '', ''
	pos = pos - 1
#Build new string
	rslt = dna_seq[:pos] + alternate + dna_seq[pos + 1:]

# Handle the positions to be highlight (in case 'alt' made of several chars)
	alternate_len = len(alt)
	if alternate_len == 1:
		pos_list = pos + 1
	else:
		pos_list = []
		for k in range(1, alternate_len + 1):
			pos_list.append(pos + k)

	return rslt, pos_list

# Example usage
if __name__ == '__main__':
# Runnig test on the 1234... string
	output_file = "highlighted_text_by_position_numbers.pdf"
	dna_sequence = '01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
	create_pdf = CreatePDF(output_file, True)
	for i in range(1, 10):
		create_pdf.print_string_to_pdf( f'DNA input position value: {i}', [])
		pos = i
		if pos % 2 == 0: #if pos is even number
			alt = 'AAAA'
		else:
			alt = 'B'
		replaced_text, pos_list = replace_chars(dna_sequence, pos, alt)
		create_pdf.print_string_to_pdf( replaced_text, pos_list)

	create_pdf.save_pdf()
	del create_pdf

#Running test on the dna from the file
	output_file = "highlighted_text_by_position_dna_file.pdf"
	input_dna_seq_file_name = 'C:/_Shaul/Python/_Shani/data/MNL1_dna_seq_allel_A.txt'
	with open(input_dna_seq_file_name, "r") as file:
		dna_sequence = file.read().strip()
	create_pdf = CreatePDF(output_file, True)
	for i in range(1, 10):
		create_pdf.print_string_to_pdf( f'DNA input position value: {i}', [])
		pos = i
		if pos % 2 == 0: #if pos is even number
			alt = 'AAAA'
		else:
			alt = 'B'
		replaced_text, pos_list = replace_chars(dna_sequence, pos, alt)
		create_pdf.print_string_to_pdf( replaced_text, pos_list)

	create_pdf.save_pdf()
	#os.startfile(output_file)