import interaction_manager, command_list
from State import instance
import re

DEFAULT_MOVEMENTS = command_list.DEFAULT_MOVEMENTS

# parses keyboard input for meaningful instructions
# sends "completed" instructions to interaction_manager router
class user_input():
    def __init__(self):
        self.graphics = None
        self.curr_state = 'Default'
        self.char_buf = ''
        self.curr_instance = 0
        self.instances = []

    def start_instance(self, filename):
        self.instances.append(instance.instance(filename))

    def set_GUI_reference(self, canvas):
        self.graphics = canvas
        self.instances[self.curr_instance].set_line_height(self.graphics.line_height)

    def key(self, event):
        self.user_key_pressed(event.keysym)

    def control_f(self, event):
        # drop on floor for now
        a = 1

    def control_b(self, event):
        # drop on floor for now
        a = 1

    def user_key_pressed(self, key):
        if self.curr_state == 'Default':
            self.user_key_default(key)

    def user_key_default(self, key):
        # default movement requested
        if DEFAULT_MOVEMENTS.has_key(key):
            interaction_manager.input_command(DEFAULT_MOVEMENTS[key], self.graphics, self.instances[self.curr_instance])
