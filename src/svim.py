#!/usr/bin/python
from Tkinter import Tk
from Graphics import text_canvas
from Input import user_input

if __name__ == '__main__':
    root = Tk()
    input_handler = user_input.user_input()
    input_handler.start_instance('test.py')
    app = text_canvas.text_canvas(root, 12, input_handler)
    app.draw_cursor(0, 0)
    app.write_text_grid(0, 0, 'lololooool', '#839496')
    app.write_text_grid(0, 1, 'qqqqqqq','#839496')
    app.write_text_grid(0, 2, 'gggggg', '#839496')
    app.write_text_grid(0, 3, 'wcwcwcwc', '#839496')
    app.draw_cursor_values(0, 0)
    app.draw_line_numbers(1)
    root.mainloop()

