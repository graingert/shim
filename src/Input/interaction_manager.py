# routes keyboard input to appropriate interaction manager
# events are fed directly from user_input
# interaction manager should not have to parse user input keys directly

def render_page(gui_reference, instance):
    lines = instance.get_lines()
    x, y = instance.get_cursor()


