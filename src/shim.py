#!/usr/bin/python
from Tkinter import Tk, Image
from Frontend import text_canvas
from Backend import user_input

if __name__ == '__main__':
    root = Tk()
    input_handler = user_input.user_input()

    input_handler.start_instance('test.py')
    app = text_canvas.text_canvas(root, 12, input_handler, 'test.py')

    root.wm_attributes('-fullscreen', 1)
    root.title('shim')
    root.overrideredirect()


    root.mainloop()

