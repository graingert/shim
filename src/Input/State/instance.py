class instance():
    def __init__(self, filename):
        self.lines = [line for line in open(filename, 'r')]
        self.cursor_x, self.cursor_y = 0, 0
        self.curr_top = 0
    # line numbers are 0 indexed
    def get_lines(self):
        return self.lines

    def get_line(self, index):
        return self.lines[index]

    def get_cursor(self):
        return self.cursor_x, self.cursor_y

    def get_curr_top(self):
        return self.curr_top

    def get_line_height(self):
        return self.line_height

    def get_line_num(self):
        return len(self.lines)

    def set_curr_top(self, num):
        self.curr_top = num

    def set_cursor(self, x, y):
        self.cursor_x = max(x, 0)
        self.cursor_y = max(y, 0)

    def set_line_height(self, num):
        self.line_height = num
