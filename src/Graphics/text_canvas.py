from Tkinter import Tk, Canvas, BOTH
from ttk import Frame
import tkFont
# Main GUI handler class handles graphics to be displayed to user
# TODO: line numbers are not handled currently, 50 is a magic number
class text_canvas(Frame):
    def __init__(self, parent, font_size, input_handler):
        Frame.__init__(self, parent)
        self.parent = parent
        self.text_font = tkFont.Font(family='Monaco', size=font_size, weight='bold')
        self.cheight, self.cwidth, self.line_num_spacing = font_size, self.text_font.measure('c'), 50
        self.init_UI(input_handler)

    def init_UI(self, input_handler):
        self.parent.title('')
        self.pack(fill=BOTH, expand=1)
        self.init_canvas(input_handler)

    def init_canvas(self, input_handler):
        self.canvas = Canvas(self, highlightthickness=0, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg='#002B36')
        self.canvas.pack()
        self.canvas.focus_set()
        self.bind_events(input_handler)

    def bind_events(self, input_handler):
        self.canvas.bind_all('<Control-f>', input_handler.control_f)
        self.canvas.bind_all('<Control-b>', input_handler.control_b)
        self.canvas.bind('<Key>', input_handler.key)

    # write line of text at given grid co-ordinates
    def write_text_grid(self, x, y, text):
        x_val = self.cwidth * x + self.line_num_spacing
        y_val = self.cheight * y
        self.canvas.create_text(x_val, y_val, anchor='nw', text=text, font=self.text_font, fill='#839496')

    def draw_line_numbers(self, start):
        for i in range(0, (self.winfo_screenheight() / self.cheight) + 1):
            self.canvas.create_text(0, self.cheight * i, anchor='nw', text=str(start + i), font=self.text_font, fill='#839496')

    def clear_all(self):
        self.canvas.delete('all')
