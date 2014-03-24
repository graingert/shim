from interaction_managers import cursor_logic, text_logic, graphics_logic

# routes keyboard input to appropriate interaction manager to mutate instance state, page is then re-rendered given new state
# events are fed directly from user_input
# interaction manager should not have to parse user input keys directly

def render_default_graphics(graphics_state, local_state, global_state):
    lines = local_state.get_line_tokens()
    x, y, curr_top = local_state.get_page_state()
    buff_line_count = graphics_state.get_line_height()

    graphics_state.draw_cursor(x, y)
    # top is zero indexed and line numbers are one indexed
    graphics_state.draw_line_numbers(curr_top + 1)

    for i in range(buff_line_count + 1):
        # Might have index errors. catch them and move on with life for now
        try:
            graphics_state.write_line_grid(i, lines[curr_top + i])
        except IndexError:
            break


def render_page(pre, post, graphics_state, local_state, global_state):
    graphics_state.clear_all()
    for func in pre:
        func()
    render_default_graphics(graphics_state, local_state, global_state)
    for func in post:
        func()


def move_left(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_left(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_right(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_right(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_down(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_down(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_up(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_up(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_beginning_line(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_beginning_line(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_end_line(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_end_line(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_next_word_front(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_next_word_front(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_next_word_end(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_next_word_end(local_state)
    render_page([], [], graphics_state, local_state, global_state)

def move_prev_word_front(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_move_prev_word_front(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_end_file(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_end_file(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_begin_file(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_begin_file(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_next_paragraph(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_next_paragraph(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_prev_paragraph(graphics_state, local_state, global_state):
    cursor_logic.move_cursor_prev_paragraph(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_line_num(n_arg, graphics_state, local_state, global_state):
    cursor_logic.move_cursor_line_num(n_arg, local_state)
    render_page([], [], graphics_state, local_state, global_state)


def move_seek_char(c_arg, graphics_state, local_state, global_state):
    cursor_logic.move_cursor_seek_char(c_arg, local_state)
    render_page([], [], graphics_state, local_state, global_state)


def insert_text(s_arg, graphics_state, local_state, global_state):
    text_logic.insert_text_str(s_arg, local_state)
    render_page([], [], graphics_state, local_state, global_state)


def delete_char(graphics_state, local_state, global_state):
    text_logic.delete_text_char(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def add_new_line(graphics_state, local_state, global_state):
    text_logic.add_new_line_char(local_state)
    render_page([], [], graphics_state, local_state, global_state)

def delete_text_movement(movement, graphics_state, local_state, global_state):
    px, py, pt = local_state.get_page_state()
    COMMAND_MAP[movement](graphics_state, local_state, global_state)
    nx, ny, nt = local_state.get_page_state()

    text_logic.delete_text_range(px, py, pt, nx, ny, nt, local_state)
    render_page([], [], graphics_state, local_state, global_state)


def delete_text_highlight(graphics_state, local_state, global_state):
    if global_state.curr_state == 'Visual':
        global_state.add_undo_buffer()
        px, py, pt = local_state.get_visual_anchors()
        nx, ny, nt = local_state.get_page_state()
        global_state.add_copy_buffer(text_logic.get_text_range(px, py, pt, nx, ny, nt, local_state))
        text_logic.delete_text_range(px, py, pt, nx, ny, nt, local_state)
        # this makes sense to be set here i think
        global_state.curr_state = 'Default'
    else:
        text_logic.delete_text_highlight(local_state)

    render_page([], [], graphics_state, local_state, global_state)


def delete_curr_line(graphics_state, local_state, global_state):
    text_logic.delete_current_line(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def insert_new_line_above(graphics_state, local_state, global_state):
    global_state.curr_state = 'Insert'
    text_logic.insert_new_line_above(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def insert_new_line_below(graphics_state, local_state, global_state):
    global_state.curr_state = 'Insert'
    text_logic.insert_new_line_below(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def insert_end_of_line(graphics_state, local_state, global_state):
    global_state.curr_state = 'Insert'
    cursor_logic.move_cursor_past_end_line(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def mouse_scroll(delta, graphics_state, local_state, global_state):
    x, y, curr_top = local_state.get_page_state()
    if y + int(delta) + curr_top <= local_state.get_line_num() - 2:
        local_state.set_cursor(x, y + int(delta))
        render_page([], [], graphics_state, local_state, global_state)
    else:
        move_end_file(graphics_state, local_state, global_state)


def visual_movement(motion, graphics_state, local_state, global_state):
    COMMAND_MAP[motion](graphics_state, local_state, global_state)
    # some commands break out of visual mode
    if global_state.curr_state == 'Visual':
        render_page([], [lambda: graphics_logic.highlight_visual_mode(graphics_state, local_state)], graphics_state, local_state, global_state)


def paste(graphics_state, local_state, global_state):
    text_logic.insert_text_strs(local_state, global_state)
    render_page([], [], graphics_state, local_state, global_state)


def yank_curr_line(graphics_state, local_state, global_state):
    x, y, curr_top = local_state.get_page_state()
    global_state.add_copy_buffer([local_state.get_line(curr_top + y)])


def shift_selection_right(graphics_state, local_state, global_state):
    text_logic.shift_selection_right(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def shift_selection_left(graphics_state, local_state, global_state):
    text_logic.shift_selection_left(local_state)
    render_page([], [], graphics_state, local_state, global_state)


def quit(graphics_state, local_state, global_state):
    import sys
    sys.exit(1)


def write(graphics_state, local_state, global_state):
    lines = ''.join(local_state.get_lines())
    with open(local_state.get_filename(), 'w') as f:
        f.write(lines)


def undo_command(graphics_state, local_state, global_state):
    prev = global_state.get_undo_state()
    if prev != None:
        print 1
        local_state.mutate_state(prev['x'], prev['y'], prev['curr_top'], prev['lines'], prev['line_tokens'])
        render_page([], [], graphics_state, local_state, global_state)


COMMAND_MAP = {
                  'quit': quit,
                  'write': write,
                  'paste': paste,
                  'move_cursor_up': move_up,
                  'insert_text': insert_text,
                  'delete_char': delete_char,
                  'undo_command': undo_command,
                  'mouse_scroll': mouse_scroll,
                  'add_new_line': add_new_line,
                  'move_cursor_left': move_left,
                  'move_cursor_down': move_down,
                  'move_cursor_right': move_right,
                  'yank_curr_line': yank_curr_line,
                  'visual_movement': visual_movement,
                  'delete_curr_line': delete_curr_line,
                  'move_cursor_end_line': move_end_line,
                  'move_cursor_end_file': move_end_file,
                  'move_cursor_line_num': move_line_num,
                  'move_cursor_seek_char': move_seek_char,
                  'insert_end_of_line': insert_end_of_line,
                  'move_cursor_begin_file': move_begin_file,
                  'shift_selection_left': shift_selection_left,
                  'delete_text_movement': delete_text_movement,
                  'insert_new_line_above': insert_new_line_above,
                  'insert_new_line_below': insert_new_line_below,
                  'delete_text_highlight': delete_text_highlight,
                  'shift_selection_right': shift_selection_right,
                  'move_cursor_next_word_end': move_next_word_end,
                  'move_cursor_next_paragraph': move_next_paragraph,
                  'move_cursor_prev_paragraph': move_prev_paragraph,
                  'move_cursor_beginning_line': move_beginning_line,
                  'move_cursor_next_word_front': move_next_word_front,
                  'move_cursor_prev_word_front': move_prev_word_front,
              }


def input_command(command, graphics_state, local_state, global_state):
    commands = command.split(':')
    if len(commands) == 1:
        COMMAND_MAP[command](graphics_state, local_state, global_state)
        # try:
        #     COMMAND_MAP[command](graphics_state, instance)
        # except:
        #     pass
    else:
        input_command_arg(commands, graphics_state, local_state, global_state)


# c denotes character arguments i.e fa maps to find a
# n denotes numerical arguments i.e 123gg maps to jump to line 123
# r denotes repeat arguments i.e 3j means run the 'j' command 3 times
# s denotes character arguments i.e text insert
def input_command_arg(commands, graphics_state, local_state, global_state):
    opt_arg = commands[0][1:]
    in_arg = commands[1]
    if commands[0].startswith('n'):
        COMMAND_MAP[in_arg](int(opt_arg), graphics_state, local_state, global_state)
    elif commands[0].startswith('r'):
        for i in range(int(opt_arg)):
            COMMAND_MAP[in_arg](graphics_state, local_state, global_state)
    elif commands[0].startswith('c'):
        # This should be a single character argument anyway
        COMMAND_MAP[in_arg](opt_arg, graphics_state, local_state, global_state)
    elif commands[0].startswith('s'):
        COMMAND_MAP[in_arg](opt_arg, graphics_state, local_state, global_state)
