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
    gui_reference.draw_line_numbers(curr_top + 1)

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


def move_beginning_line(gui_reference, instance):
    cursor_logic.move_cursor_beginning_line(instance)
    render_page(gui_reference, instance)


def move_end_line(gui_reference, instance):
    cursor_logic.move_cursor_end_line(instance)
    render_page(gui_reference, instance)


def move_next_word_front(gui_reference, instance):
    cursor_logic.move_cursor_next_word_front(instance)
    render_page(gui_reference, instance)


def move_next_word_end(gui_reference, instance):
    cursor_logic.move_cursor_next_word_end(instance)
    render_page(gui_reference, instance)

def move_prev_word_front(gui_reference, instance):
    cursor_logic.move_cursor_move_prev_word_front(instance)
    render_page(gui_reference, instance)


def move_end_file(gui_reference, instance):
    cursor_logic.move_cursor_end_file(instance)
    render_page(gui_reference, instance)


def move_begin_file(gui_reference, instance):
    cursor_logic.move_cursor_begin_file(instance)
    render_page(gui_reference, instance)


def move_next_paragraph(gui_reference, instance):
    cursor_logic.move_cursor_next_paragraph(instance)
    render_page(gui_reference, instance)


def move_prev_paragraph(gui_reference, instance):
    cursor_logic.move_cursor_prev_paragraph(instance)
    render_page(gui_reference, instance)


def move_line_num(n_arg, gui_reference, instance):
    cursor_logic.move_cursor_line_num(n_arg, instance)
    render_page(gui_reference, instance)


def move_seek_char(c_arg, gui_reference, instance):
    cursor_logic.move_cursor_seek_char(c_arg, instance)
    render_page(gui_reference, instance)


COMMAND_MAP = {
                  'move_cursor_up': move_up,
                  'move_cursor_left': move_left,
                  'move_cursor_down': move_down,
                  'move_cursor_right': move_right,
                  'move_cursor_line_num': move_line_num,
                  'move_cursor_end_line': move_end_line,
                  'move_cursor_end_file': move_end_file,
                  'move_cursor_seek_char': move_seek_char,
                  'move_cursor_begin_file': move_begin_file,
                  'move_cursor_next_word_end': move_next_word_end,
                  'move_cursor_beginning_line': move_beginning_line,
                  'move_cursor_next_word_front': move_next_word_front,
                  'move_cursor_prev_word_front': move_prev_word_front,
                  'move_cursor_next_paragraph': move_next_paragraph,
                  'move_cursor_prev_paragraph': move_prev_paragraph
              }

def input_command(command, gui_reference, instance):
    commands = command.split(':')
    if len(commands) == 1:
        COMMAND_MAP[command](gui_reference, instance)
        # try:
        #     COMMAND_MAP[command](gui_reference, instance)
        # except:
        #     pass
    else:
        input_command_num(commands, gui_reference, instance)


def input_command_num(commands, gui_reference, instance):
    opt_arg = commands[0][1:]
    in_arg = commands[1]
    # n denotes numerical arguments
    if commands[0].startswith('n'):
        COMMAND_MAP[in_arg](int(opt_arg), gui_reference, instance)
    # r denotes repeat arguments i.e 3j means run the 'j' command 3 times
    if commands[0].startswith('r'):
        for i in range(int(opt_arg)):
            COMMAND_MAP[in_arg](gui_reference, instance)
    # c denotes character arguments
    elif commands[0].startswith('c'):
        # This should be a single character argument anyway
        COMMAND_MAP[in_arg](opt_arg, gui_reference, instance)
