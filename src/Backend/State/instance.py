import json
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
        self.meta_data = json.loads(open('.shimdata', 'r').read())
        self.undo_buffer, self.undo_index = [], -1

    def check_repeat_additions(self, diff, last_state):
        return ((diff[0] == '+' and last_state[0] == '+') and diff[1] == last_state[2]['last_addition'] + 1)

    def check_repeat_deletions(self, diff, last_state):
        return ((diff[0] == '-' and last_state[0] == '-') and diff[1] == last_state[1])

    def check_repeat_modifications(self, diff, last_state):
        return ((diff[0] == 'm' and last_state[0] == 'm') and diff[1] == last_state[1])

    def add_to_undo_buffer(self, diff):
        if self.undo_index == len(self.undo_buffer) - 1:
            try:
                last_state = self.undo_buffer[self.undo_index]
            except IndexError:
                self.undo_buffer.append(diff)
                self.undo_index += 1
                return

            # repeat addtions to the same line
            if self.check_repeat_additions(diff, last_state):
                last_state[2]['count'] += 1
                last_state[2]['last_addition'] += 1
            # repeat deletions from the same line
            elif self.check_repeat_deletions(diff, last_state):
                last_state[2]['lines'].append(diff[2]['lines'][0])
                last_state[2]['line_tokens'].append(diff[2]['line_tokens'][0])
            # repeat modifications to the same line
            elif self.check_repeat_modifications(diff, last_state):
                last_state[2]['new']['line'] = diff[2]['new']['line']
                last_state[2]['new']['line_token'] = diff[2]['new']['line_token']
            else:
                self.undo_buffer.append(diff)
                self.undo_index += 1
                if len(self.undo_buffer) > 100:
                    self.undo_buffer.pop(0)
        else:
            self.undo_buffer = (self.undo_buffer[:self.undo_index] + [diff], [diff])[self.undo_index == -1]
            self.undo_index += 1


    def undo_line_modification(self, diff):
        self.lines[diff[1]] = diff[2]['old']['line'][0]
        self.line_tokens[diff[1]] = diff[2]['old']['line_token'][0]

    def undo_line_addition(self, diff):
        for i in range(diff[2]['count']):
            self.lines.pop(diff[1])
            self.line_tokens.pop(diff[1])

    def undo_line_removal(self, diff):
        for i in range(len(diff[2]['lines'])):
            self.lines.insert(i + diff[1], diff[2]['lines'][i])
            self.line_tokens.insert(i + diff[1], diff[2]['line_tokens'][i])

    def undo_state(self):
        if self.undo_index != -1:
            # diff = self.undo_buffer.pop(-1)
            diff = self.undo_buffer[self.undo_index]
            self.undo_index -= 1
            if diff[0] == 'm':
                self.undo_line_modification(diff)
            elif diff[0] == '+':
                self.undo_line_addition(diff)
            elif diff[0] == '-':
                self.undo_line_removal(diff)

            (x, y, z)  = diff[2]['state']
            self.set_curr_top(z)
            self.set_cursor(x, y)

    def redo_line_modification(self, diff):
        self.lines[diff[1]] = diff[2]['new']['line'][0]
        self.line_tokens[diff[1]] = diff[2]['new']['line_token'][0]

    def redo_line_addition(self, diff):
        for i in range(diff[2]['count']):
            self.lines.insert(diff[1] + i, diff[2]['data']['lines'][i])
            self.line_tokens.insert(diff[1] + i, diff[2]['data']['line_tokens'][i])

    def redo_line_removal(self, diff):
        for i in range(len(diff[2]['lines'])):
            self.lines.pop(diff[1])
            self.line_tokens.pop(diff[1])

    def redo_state(self):
        if self.undo_index < len(self.undo_buffer) - 1:
            self.undo_index += 1
            diff = self.undo_buffer[self.undo_index]
            if diff[0] == 'm':
                self.redo_line_modification(diff)
            if diff[0] == '+':
                self.redo_line_addition(diff)
            if diff[0] == '-':
                self.redo_line_removal(diff)

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

    def get_meta_data(self):
        return self.meta_data

    def add_line(self, index, line):
        self.add_to_undo_buffer(('+', index,
            { 'count': 1, 'data': { 'lines': [self.lines[index]], 'line_tokens': [self.line_tokens[index]] },
            'state': self.get_page_state(), 'last_addition': index }))
        self.lines.insert(index, line)
        self.line_tokens.insert(index, self.parser.parse_string(line))

    def remove_line(self, index):
        self.add_to_undo_buffer(('-', index, { 'lines': [self.lines[index]], 'line_tokens': [self.line_tokens[index]], 'state': self.get_page_state(), }))
        self.lines.pop(index)
        self.line_tokens.pop(index)

    def set_curr_top(self, num):
        self.curr_top = num

    def set_line_height(self, num):
        self.line_height = num

    def set_line(self, ind, s):
        parsed = self.parser.parse_string(s)
        self.add_to_undo_buffer(('m', ind, { 'old': { 'line': [self.lines[ind]], 'line_token': [self.line_tokens[ind]] },
            'new': { 'line': [s], 'line_token': [parsed] }, 'state': self.get_page_state()}))
        self.lines[ind] = s
        self.line_tokens[ind] = parsed

    def set_visual_anchor(self, x=None, y=None, curr_top=None):
        self.visual_x = x if x is not None else self.cursor_x
        self.visual_y = y if y is not None else self.cursor_y
        self.visual_curr_top = curr_top if curr_top is not None else self.curr_top

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
