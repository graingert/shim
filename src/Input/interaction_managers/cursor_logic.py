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
