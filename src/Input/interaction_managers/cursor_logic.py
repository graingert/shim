def move_cursor_left(instance):
    x, y = instance.get_cursor()
    x = (0, x - 1)[x - 1 > 0]
    instance.set_cursor(x, y)

def move_cursor_right(instance):
    x, y = instance.get_cursor()
    curr_top = instance.get_curr_top()
    lines = instance.get_lines()
    try:
        nxt_char = lines[curr_top + y][x + 1]
    except:
        nxt_char = '\n'
    x = (x, x + 1)[nxt_char != '\n']
    instance.set_cursor(x, y)

def move_cursor_up(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()

    try:
        previous_line = instance.get_line(y + curr_top - 1)
        # last character is a new line
        x = min(x, len(previous_line) - 2)
    except IndexError:
         pass

    if y > 0:
        instance.set_cursor(x, y - 1)
    elif curr_top > 0:
        instance.set_curr_top(curr_top - 1)
        instance.set_cursor(x, y)

def move_cursor_down(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()

    try:
        next_line = instance.get_line(y + curr_top + 1)
        # last character is a new line
        x = min(x, len(next_line) - 2)
    except IndexError:
         pass

    if y < instance.get_line_height():
        instance.set_cursor(x, y + 1)
    elif curr_top + y < instance.get_line_num():
        instance.set_curr_top(curr_top + 1)
        instance.set_cursor(x, y)
