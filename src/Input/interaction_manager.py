import re
# routes keyboard input to appropriate interaction manager
# events are fed directly from user_input
# interaction manager should not have to parse user input keys directly
class interaction_manager():
    def __init__(self):
        self.mode = 'Default'
