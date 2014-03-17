from Tkinter import Tk, Canvas, BOTH
from ttk import Frame
import tkFont

class text_canvas(Frame):
    def __init__(self, parent, font_size):
        Frame.__init__(self, parent)
        self.parent = parent
        self.text_font = tkFont.Font(family='Monaco', size=font_size, weight='bold')
        self.cheight = font_size
        self.cwidth = self.text_font.measure('c')
        self.init_UI()

    def init_UI(self):
        self.parent.title('shitty vim')
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, highlightthickness=0, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg='#002B36')
        self.canvas.pack()

    def write_line(self, x, y, txt):
        self.canvas.create_text(x, y, anchor='nw', text=txt, font=self.text_font, fill='#839496')
    # write line of text at given grid co-ordinates
    def write_text_grid(self, x, y, text):
        x_val = self.cwidth * x
        y_val = self.cheight * y
        print (self.winfo_screenheight() / self.cheight)
        self.canvas.create_text(x_val, y_val, anchor='nw', text=text, font=self.text_font, fill='#839496')

    def draw_grid_lines(self, spacing):
        cwidth, cheight = self.text_font.measure('c'), self.cheight
#        for i in range(1, (self.winfo_screenheight() - 1) / (cheight + 1) + 1):
        for i in range(1, 80):
            self.canvas.create_line(0, cheight * i + 2, self.winfo_screenwidth(), cheight * i + 2)
#        for i in range(1, (self.winfo_screenwidth()) / (cwidth + 1) + 1):
        for i in range(1, 250):
            self.canvas.create_line(cwidth * i - .5, 0, cwidth * i - .5, self.winfo_screenheight(), )
