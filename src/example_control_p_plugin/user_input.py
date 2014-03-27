    def init_fuzzy_matching(self):
        if self.curr_state != 'fuzzy_file_selection':
            self.curr_state = 'fuzzy_file_selection'
            self.command_buffer = ''
            self.get_curr_instance().set_visual_anchor(y=2)
            cmd = ['s' + self.command_buffer, 'fuzzy_file_select']
            interaction_manager.input_command(cmd, self.graphics, self.get_curr_instance(), self)

    def user_key_fuzzy_file_select(self, key):
        if key == 'Return':
            self.command_buffer = ''
            self.curr_state = 'Default'
            cmd = ['fuzzy_file_enter']
        elif key == 'BackSpace':
            self.command_buffer = self.command_buffer[:-1]
            cmd = ['s' + self.command_buffer, 'fuzzy_file_select']
        elif key == '<Up>' or key == '<Down>':
            inst = self.get_curr_instance()
            _, vy, _ = inst.get_visual_anchors()
            vy = vy + 1 if key == '<Down>' else vy - 1
            vy = min(21, max(vy, 2))
            inst.set_visual_anchor(y=vy)
            cmd = ['s' + self.command_buffer, 'fuzzy_file_select']
        else:
            self.command_buffer += key
            cmd = ['s' + self.command_buffer, 'fuzzy_file_select']

        interaction_manager.input_command(cmd, self.graphics, self.get_curr_instance(), self)
