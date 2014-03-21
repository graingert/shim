import interaction_manager, command_list, command_parser
from State import instance
import re

DEFAULT_MOVEMENTS = command_list.DEFAULT_MOVEMENTS
BREAK_MOVEMENTS = command_list.BREAK_MOVEMENTS
COMMAND_MAP = command_list.COMMAND_MAP

# parses keyboard input for meaningful instructions
# sends "completed" instructions to interaction_manager router
class user_input():
    def __init__(self):
        self.graphics = None
        self.curr_state = 'Default'
        self.command_buffer = ''
        self.curr_instance = 0
        self.instances = []

    def start_instance(self, filename):
        self.instances.append(instance.instance(filename))

    def set_GUI_reference(self, canvas):
        self.graphics = canvas
        self.instances[self.curr_instance].set_line_height(self.graphics.line_height)

# checks if key input an integer greater than 0 and less than 10
    def is_digit(self, k):
        return (len(k) == 1) and (ord(k) >= 49 and ord(k) <= 57)

    def key(self, event):
        # if key is not in [a-zA-Z0-9] length of keysym will be greater than one
        key = event.keysym
        if key != '??':
            if len(key) > 1:
                try:
                    k = COMMAND_MAP[key]
                    self.user_key_pressed(k)
                except KeyError:
                    pass
            else:
                self.user_key_pressed(key)

    def control_f(self, event):
        # drop on floor for now
        a = 1

    def control_b(self, event):
        # drop on floor for now
        a = 1

    def escape(self, event):
        self.curr_state = 'Default'
        self.command_buffer = ''

    def user_key_pressed(self, key):
        if self.curr_state == 'Default':
            self.user_key_default(key)
        elif self.curr_state == 'Insert':
            self.user_key_insert(key)

    def user_key_default(self, key):
        # To be buffered
        if key in ['g', 'f'] or self.is_digit(key) or len(self.command_buffer):
            self.command_buffer += key
            s_par = command_parser.parse(self.command_buffer)

            if s_par != None:
                interaction_manager.input_command(s_par, self.graphics, self.instances[self.curr_instance])
                self.command_buffer = ''
            elif BREAK_MOVEMENTS.has_key(key):
                interaction_manager.input_command(BREAK_MOVEMENTS[key], self.graphics, self.instances[self.curr_instance])
                self.command_buffer = ''

        # default movement requested
        elif DEFAULT_MOVEMENTS.has_key(key):
            interaction_manager.input_command(DEFAULT_MOVEMENTS[key], self.graphics, self.instances[self.curr_instance])
            self.command_buffer = ''
        elif key == 'i':
            self.curr_state = 'Insert'

    def user_key_insert(self, key):
        cmd = 's' + key + ':' + 'insert_text'
        interaction_manager.input_command(cmd, self.graphics, self.instances[self.curr_instance])
