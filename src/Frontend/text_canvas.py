from Tkinter import Tk, Canvas, BOTH
from color_config import options
from ttk import Frame
import tkFont

# this is hacky as shit but the math doesn't seem to be working out so far
LINEMAPPING = { 12: 58, 18: 39, 20: 35 }
# Main GUI handler class handles graphics to be displayed to user
class text_canvas(Frame):
    def __init__(self, parent, font_size, input_handler, filename):
        Frame.__init__(self, parent)
        self.parent = parent
        self.text_font = tkFont.Font(family='Monaco', size=font_size, weight='bold')
        self.filename = filename
        self.cheight, self.cwidth, self.line_num_spacing, self.line_height = font_size, self.text_font.measure('c'), 50, LINEMAPPING[font_size]
        self.init_UI(input_handler)

    def init_UI(self, input_handler):
        self.parent.title('')
        self.pack(fill=BOTH, expand=1)
        self.init_canvas(input_handler)

    def get_dimensions(self):
        return {
                   'cheight': self.cheight,
                   'cwidth': self.cwidth,
                   'line_num_spacing':self.line_num_spacing,
                   'line_height': self.line_height,
                   'screen_width': self.winfo_screenwidth(),
                   'screen_height': self.winfo_screenheight()
               }

    def init_canvas(self, input_handler):
        self.canvas = Canvas(self, highlightthickness=0, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg=options['background_color'])
        self.canvas.pack()
        self.canvas.focus_set()
        self.bind_events(input_handler)

    def clear_all(self):
        self.canvas.delete('all')

    def get_line_height(self):
        return self.line_height

    def get_grid_y(self, y):
        return self.cheight * y + (y * 2)

    def bind_events(self, input_handler):
        # TODO: this should be cleaned up ideally into a separate handler list
        input_handler.set_GUI_reference(self)
        self.canvas.bind('<Key>', input_handler.key)
        self.canvas.bind_all('<Escape>', input_handler.escape)
        self.canvas.bind_all("<MouseWheel>", input_handler.mouse_scroll)
        self.canvas.bind_all('<Control-p>', input_handler.control_p)

    def write_line_grid(self, y, line):
        for token in line:
            self.write_text_grid(token[0], y, token[1], token[2])

    # write line of text at given grid co-ordinates
    def write_text_grid(self, x, y, text, color=options['text_color']):
        x_val = self.cwidth * x + self.line_num_spacing
        # 2 pixel spacing between each line
        y_val = self.cheight * y + (y * 2)
        self.canvas.create_text(x_val, y_val, anchor='nw', text=text, font=self.text_font, fill=color)

    def write_status_line(self, text, textcolor=options['status_text_color'], backgroundcolor=options['status_background_color']):
        y = self.line_height + 1
        self.canvas.create_rectangle(0, self.cheight * y + (y * 2), self.winfo_screenwidth(), self.cheight * y + (y * 2) + self.cheight + 4, fill=backgroundcolor, outline=backgroundcolor)
        self.write_text_grid(0, self.line_height + 1, text, textcolor)

    def draw_highlight_grid(self, y, x1, x2, highlightcolor=options['text_highlight_color']):
        y_val = self.cheight * y + (y * 2)
        x1_val = self.cwidth * x1 + self.line_num_spacing
        x2_val = self.cwidth * x2 + self.line_num_spacing
        self.canvas.create_rectangle(x1_val, y_val, x2_val, y_val + self.cheight + 4, fill=highlightcolor, outline=highlightcolor)

    def draw_line_numbers(self, start, highlightcolor=options['line_num_highlight_color'], textcolor=options['line_num_text_color']):
        self.canvas.create_rectangle(0, 0, self.line_num_spacing / 2, self.winfo_screenheight(), fill=highlightcolor, outline=highlightcolor)
        for i in range(self.line_height + 1):
            self.canvas.create_text(0, self.cheight * i + (i * 2), anchor='nw', text=str(start + i), font=self.text_font, fill=textcolor)

    def draw_cursor(self, x, y, highlightcolor=options['cursor_highlight_color'], cursorcolor=options['cursor_color']):
        x_val = self.cwidth * x + self.line_num_spacing
        y_val = self.cheight * y + (y * 2)

        self.canvas.create_rectangle(0, y_val, self.winfo_screenwidth(), y_val + self.cheight + 4, fill=highlightcolor, outline=highlightcolor)
        self.canvas.create_rectangle(x_val, 0, x_val + self.cwidth, self.winfo_screenheight(), fill=highlightcolor, outline=highlightcolor)
        self.canvas.create_rectangle(x_val, y_val, x_val + self.cwidth, y_val + self.cheight + 4, fill=cursorcolor, outline=cursorcolor)

    def draw_rectangle_absolute(self, x1, y1, x2, y2, color):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
