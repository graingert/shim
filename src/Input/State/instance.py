from copy import deepcopy
from SyntaxTokens import syntax_parser

# it should be kind of obvious what class is supposed to do.....
class instance():
    def __init__(self, filename):
        self.filename = filename
        self.lines = [line for line in open(filename, 'r')]
        self.parser = syntax_parser.syntax_parser(filename)
        self.line_tokens = [self.parser.parse_string(line) for line in open(filename, 'r')]
        self.cursor_x, self.cursor_y, self.curr_top = 0, 0, 0
        self.visual_x, self.visual_y, self.visual_curr_top = 0, 0, 0

    def get_line(self, index):
        return self.lines[index]

    # line numbers are 0 indexed
    def get_lines(self):
        return self.lines

    def get_line_tokens(self):
        return self.line_tokens

    def get_cursor(self):
        return self.cursor_x, self.cursor_y

    def get_curr_top(self):
        return self.curr_top

    def get_line_height(self):
        return self.line_height

    def get_line_num(self):
        return len(self.lines)

    def get_filename(self):
        return self.filename

    def get_page_state(self):
        return self.cursor_x, self.cursor_y, self.curr_top

    def get_visual_anchors(self):
        return self.visual_x, self.visual_y, self.visual_curr_top

    def add_line(self, index, line):
        self.lines.insert(index, line)
        self.line_tokens.insert(index, self.parser.parse_string(line))

    def remove_line(self, index):
        self.lines.pop(index)
        self.line_tokens.pop(index)

    def set_curr_top(self, num):
        self.curr_top = num

    def set_line_height(self, num):
        self.line_height = num

    def set_line(self, ind, s):
        self.lines[ind] = s
        self.line_tokens[ind] = self.parser.parse_string(s)

    def set_visual_anchor(self):
        self.visual_x, self.visual_y, self.visual_curr_top = self.cursor_x, self.cursor_y, self.curr_top

    def set_cursor(self, x, y):
        self.cursor_x = max(x, 0)
        if y > self.line_height:
            self.curr_top += (y - self.line_height)
            self.cursor_y = self.line_height
        elif y < 0:
            self.curr_top = max(self.curr_top + y, 0)
            self.cursor_y = 0
        else:
            self.cursor_y = y

    def mutate_state(self, x, y, curr_top, lines, line_tokens):
        print 'mutating!'
        self.cursor_x, self.cursor_y, self.curr_top = x, y, curr_top
        self.lines = lines
        self.line_tokens = line_tokens
