#!/usr/bin/python
from Tkinter import Tk
from Graphics import text_canvas

if __name__ == '__main__':
    root = Tk()
    app = text_canvas(root, 20)
    app.write_text_grid(0, 0,'lolo')
    app.write_text_grid(0, 1,'lolololololololol')
    app.write_text_grid(3, 5,'lolololololololol')
    app.draw_grid_lines(0)
    root.mainloop()
