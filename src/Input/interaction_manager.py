from interaction_managers import cursor_logic
# routes keyboard input to appropriate interaction manager to mutate instance state, page is then re-rendered given new state
# events are fed directly from user_input
# interaction manager should not have to parse user input keys directly

def render_page(gui_reference, instance):
    gui_reference.clear_all()
    lines = instance.get_lines()
    x, y = instance.get_cursor()
    curr_top = instance.get_curr_top()
    buff_line_count = gui_reference.get_line_height()

    gui_reference.draw_cursor(x, y)
    # top is zero indexed and line numbers are one indexed
    gui_reference.draw_line_numbers(curr_top)

    for i in range(buff_line_count + 1):
        # Might have index errors. catch them and move on with life for now
        try:
            gui_reference.write_text_grid(0, i, lines[curr_top + i], '#839496')
        except IndexError:
            break


def move_left(gui_reference, instance):
    cursor_logic.move_cursor_left(instance)
    render_page(gui_reference, instance)


def move_right(gui_reference, instance):
    cursor_logic.move_cursor_right(instance)
    render_page(gui_reference, instance)

def move_down(gui_reference, instance):
    cursor_logic.move_cursor_down(instance)
    render_page(gui_reference, instance)

def move_up(gui_reference, instance):
    cursor_logic.move_cursor_up(instance)
    render_page(gui_reference, instance)

COMMAND_MAP = {
                'move_cursor_left': move_left,
                'move_cursor_right': move_right,
                'move_cursor_up': move_up,
                'move_cursor_down': move_down
              }

def input_command(command, gui_reference, instance):
    try:
        COMMAND_MAP[command](gui_reference, instance)
    except:
        pass

