from interaction_managers import cursor_logic, text_logic
# routes keyboard input to appropriate interaction manager to mutate instance state, page is then re-rendered given new state
# events are fed directly from user_input
# interaction manager should not have to parse user input keys directly
def render_page(gui_reference, local_state):
    gui_reference.clear_all()
    lines = local_state.get_lines()
    x, y = local_state.get_cursor()
    curr_top = local_state.get_curr_top()
    buff_line_count = gui_reference.get_line_height()

    gui_reference.draw_cursor(x, y)
    # top is zero indexed and line numbers are one indexed
    gui_reference.draw_line_numbers(curr_top + 1)

    for i in range(buff_line_count + 1):
        # Might have index errors. catch them and move on with life for now
        try:
            gui_reference.write_text_grid(0, i, lines[curr_top + i], '#839496')
        except IndexError:
            break


def move_left(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_left(local_state)
    render_page(gui_reference, local_state)


def move_right(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_right(local_state)
    render_page(gui_reference, local_state)


def move_down(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_down(local_state)
    render_page(gui_reference, local_state)


def move_up(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_up(local_state)
    render_page(gui_reference, local_state)


def move_beginning_line(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_beginning_line(local_state)
    render_page(gui_reference, local_state)


def move_end_line(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_end_line(local_state)
    render_page(gui_reference, local_state)


def move_next_word_front(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_next_word_front(local_state)
    render_page(gui_reference, local_state)


def move_next_word_end(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_next_word_end(local_state)
    render_page(gui_reference, local_state)

def move_prev_word_front(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_move_prev_word_front(local_state)
    render_page(gui_reference, local_state)


def move_end_file(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_end_file(local_state)
    render_page(gui_reference, local_state)


def move_begin_file(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_begin_file(local_state)
    render_page(gui_reference, local_state)


def move_next_paragraph(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_next_paragraph(local_state)
    render_page(gui_reference, local_state)


def move_prev_paragraph(gui_reference, local_state, global_state):
    cursor_logic.move_cursor_prev_paragraph(local_state)
    render_page(gui_reference, local_state)


def move_line_num(n_arg, gui_reference, local_state, global_state):
    cursor_logic.move_cursor_line_num(n_arg, local_state)
    render_page(gui_reference, local_state)


def move_seek_char(c_arg, gui_reference, local_state, global_state):
    cursor_logic.move_cursor_seek_char(c_arg, local_state)
    render_page(gui_reference, local_state)


def insert_text(s_arg, gui_reference, local_state, global_state):
    text_logic.insert_text_str(s_arg, local_state)
    render_page(gui_reference, local_state)


def delete_char(gui_reference, local_state, global_state):
    text_logic.delete_text_char(local_state)
    render_page(gui_reference, local_state)


def add_new_line(gui_reference, local_state, global_state):
    text_logic.add_new_line_char(local_state)
    render_page(gui_reference, local_state)

def delete_text_movement(movement, gui_reference, local_state, global_state):
    pt = local_state.get_curr_top()
    px, py = local_state.get_cursor()
    COMMAND_MAP[movement](gui_reference, local_state, global_state)
    nt = local_state.get_curr_top()
    nx, ny = local_state.get_cursor()

    text_logic.delete_text_range(px, py, pt, nx, ny, nt, local_state)
    render_page(gui_reference, local_state)


def delete_text_highlight(gui_reference, local_state, global_state):
    text_logic.delete_text_highlight(local_state)
    render_page(gui_reference, local_state)


def delete_curr_line(gui_reference, local_state, global_state):
    text_logic.delete_current_line(local_state)
    render_page(gui_reference, local_state)


def insert_new_line_above(gui_reference, local_state, global_state):
    global_state.curr_state = 'Insert'
    text_logic.insert_new_line_above(local_state)
    render_page(gui_reference, local_state)


def insert_new_line_below(gui_reference, local_state, global_state):
    global_state.curr_state = 'Insert'
    text_logic.insert_new_line_below(local_state)
    render_page(gui_reference, local_state)


def insert_end_of_line(gui_reference, local_state, global_state):
    global_state.curr_state = 'Insert'
    cursor_logic.move_cursor_past_end_line(local_state)
    render_page(gui_reference, local_state)


def mouse_scroll(delta, gui_reference, local_state, global_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    if y + int(delta) + curr_top <= local_state.get_line_num() - 2:
        local_state.set_cursor(x, y + int(delta))
        render_page(gui_reference, local_state)
    else:
        move_end_file(gui_reference, local_state, global_state)


COMMAND_MAP = {
                  'move_cursor_up': move_up,
                  'insert_text': insert_text,
                  'delete_char': delete_char,
                  'mouse_scroll': mouse_scroll,
                  'add_new_line': add_new_line,
                  'move_cursor_left': move_left,
                  'move_cursor_down': move_down,
                  'move_cursor_right': move_right,
                  'delete_curr_line': delete_curr_line,
                  'move_cursor_end_line': move_end_line,
                  'move_cursor_end_file': move_end_file,
                  'move_cursor_line_num': move_line_num,
                  'move_cursor_seek_char': move_seek_char,
                  'insert_end_of_line': insert_end_of_line,
                  'move_cursor_begin_file': move_begin_file,
                  'delete_text_movement': delete_text_movement,
                  'insert_new_line_above': insert_new_line_above,
                  'insert_new_line_below': insert_new_line_below,
                  'delete_text_highlight': delete_text_highlight,
                  'move_cursor_next_word_end': move_next_word_end,
                  'move_cursor_next_paragraph': move_next_paragraph,
                  'move_cursor_prev_paragraph': move_prev_paragraph,
                  'move_cursor_beginning_line': move_beginning_line,
                  'move_cursor_next_word_front': move_next_word_front,
                  'move_cursor_prev_word_front': move_prev_word_front
              }


def input_command(command, gui_reference, local_state, global_state):
    commands = command.split(':')
    if len(commands) == 1:
        COMMAND_MAP[command](gui_reference, local_state, global_state)
        # try:
        #     COMMAND_MAP[command](gui_reference, instance)
        # except:
        #     pass
    else:
        input_command_arg(commands, gui_reference, local_state, global_state)


# c denotes character arguments i.e fa maps to find a
# n denotes numerical arguments i.e 123gg maps to jump to line 123
# r denotes repeat arguments i.e 3j means run the 'j' command 3 times
# s denotes character arguments i.e text insert
def input_command_arg(commands, gui_reference, local_state, global_state):
    opt_arg = commands[0][1:]
    in_arg = commands[1]
    if commands[0].startswith('n'):
        COMMAND_MAP[in_arg](int(opt_arg), gui_reference, local_state, global_state)
    elif commands[0].startswith('r'):
        for i in range(int(opt_arg)):
            COMMAND_MAP[in_arg](gui_reference, local_state, global_state)
    elif commands[0].startswith('c'):
        # This should be a single character argument anyway
        COMMAND_MAP[in_arg](opt_arg, gui_reference, local_state, global_state)
    elif commands[0].startswith('s'):
        COMMAND_MAP[in_arg](opt_arg, gui_reference, local_state, global_state)
