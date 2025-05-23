from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

class CreatePDF:
	def __init__(self):
		self.width, self.height = letter
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
	
	def create_pdf_with_colors(self, output_path, text, highlight_chars):
		c = canvas.Canvas(output_path, pagesize=letter)
		
		x, y = 50, self.height - 50
		line_height = 16  # Adjusted for better spacing
		font_size = 12  # Font size
		
		c.setFont("Helvetica", font_size)
		
		for char in text:
			if x > self.width - 50:  # Wrap text to the next line
				x = 50
				y -= line_height
			
			if y < 50:  # Start a new page if reaching bottom margin
				c.showPage()
				x, y = 50, self.height - 50
			
			char_width = c.stringWidth(char, "Helvetica", font_size)
			
			if char in highlight_chars:
				# Adjusted yellow rectangle alignment and dimensions
				c.setFillColor(self.available_colors["yellow"])
				rect_padding = 1
				rect_height = font_size + rect_padding * 2
				c.rect(
					x - rect_padding, 
					y - font_size - rect_padding, 
					char_width + rect_padding * 2, 
					rect_height, 
					fill=1, 
					stroke=0
				)
				
				c.setFillColor(self.available_colors["red"])
				c.setFont("Helvetica-Bold", font_size)
			else:
				c.setFillColor(self.available_colors["black"])
				c.setFont("Helvetica", font_size)
			
			c.drawString(x, y, char)
			x += char_width
		
		c.save()

# Example usage
if __name__ == '__main__':
	create_pdf = CreatePDF()
	output_file = "highlighted_text_with_refined_alignment.pdf"
	text = "Hello, World! This is a test of the CreatePDF class with multiple lines and highlighted characters."
	highlighted_chars = {'e', 'o', 'W'}
	create_pdf.create_pdf_with_colors(output_file, text, highlighted_chars)
