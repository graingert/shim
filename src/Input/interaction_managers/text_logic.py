import cursor_logic

def insert_text_str(s, instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()
    curr_line = instance.get_line(y + curr_top)
    instance.set_line(curr_top + y, curr_line[:x] + s + curr_line[x:])
    instance.set_cursor(x + len(s), y)


def delete_text_char(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()
    curr_line = instance.get_line(y + curr_top)

    if x > 0:
        instance.set_line(curr_top + y, curr_line[:x - 1] + curr_line[x:])
        instance.set_cursor(x - 1, y)
    # do not delete character on first line of page
    elif y > 0 or curr_top > 0:
        if curr_line == '\n':
            instance.remove_line(curr_top + y)
            instance.set_cursor(0, y - 1)
            cursor_logic.move_cursor_end_line(instance)
        else:
            prev_line = instance.get_line(y + curr_top - 1)
            instance.remove_line(curr_top + y)
            # slice off new line + last character
            instance.set_line(curr_top + y - 1, prev_line[:-1] + curr_line)
            instance.set_cursor(len(prev_line) - 1, y - 1)


def delete_text_range(px, py, pt, nx, ny, nt, instance):
    # final cursor location should be at fx, fy depending on which comes first
    fx, fy = ((px, py), (nx, ny))[(ny + nt) < (py + pt)]
    (start, end) = ((py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]

    if py + pt == ny + nt:
        curr_line = instance.get_line(py + pt)
        instance.set_line(py + pt, curr_line[:px] + curr_line[nx:])
    else:
        count = 0
        for n in range(start, end + 1):
            if (n == py + pt) and (px, py) == (fx, fy):
                instance.set_line(n, instance.get_line(n)[:px] + '\n')
            elif (n  == py + pt) and (px, py) != (fx, fy):
                instance.set_line(n, instance.get_line(n)[px:])
            elif (n == ny + nt) and (nx, ny) == (fx, fy):
                instance.set_line(n, instance.get_line(n)[:nx] + '\n')
            elif (n == ny + nt) and (nx, ny) != (fx, fy):
                instance.set_line(n, instance.get_line(n)[nx:])
            else:
                count += 1

        for i in range(count):
            instance.remove_line(start + 1)

    instance.set_cursor(fx, fy)


def add_new_line_char(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()
    curr_line = instance.get_line(y + curr_top)

    if curr_line[x] != '\n':
        instance.set_line(y + curr_top, curr_line[:x] + '\n')
        instance.add_line(y + curr_top + 1, curr_line[x:])

    instance.set_cursor(0, y + 1)
