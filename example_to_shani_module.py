from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
import os

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
	
	def print_string_to_pdf(self, text, highlight_positions): 
		
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
		pass
		
	def save_pdf(self):
		self.c.save()

# Example usage

print('dummy')

if __name__ == '__main__':
	print('importing class of pdf')

""""
if __name__ == '__main__':
	output_file = "highlighted_text_by_position.pdf"
	create_pdf = CreatePDF(output_file, True)
	for i in range(70):
		create_pdf.print_string_to_pdf( f'DNA string1 loop: {i}', [])
		text = "Hello, World! This is a test of the CreatePDF class with multiple lines and highlighted"# characters. Hello, World! This is a test"
		highlight_positions = {1, 4, 7, 10, 15, 25, 50, 150}  # Highlight characters by their positions (0-based index)
		create_pdf.print_string_to_pdf( text, highlight_positions)
		create_pdf.print_string_to_pdf( f'DNA string2 loop: {i}', [])
		text = '01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
		create_pdf.print_string_to_pdf( text, highlight_positions)
	create_pdf.save_pdf()
	os.startfile(output_file)
"""