import cursor_logic

def insert_text_str(s, local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    curr_line = local_state.get_line(curr_top + y)
    local_state.set_line(curr_top + y, curr_line[:x] + s + curr_line[x:])
    local_state.set_cursor(x + len(s), y)


def delete_text_highlight(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    curr_line = local_state.get_line(curr_top + y)
    local_state.set_line(curr_top + y, curr_line[:x] + curr_line[x + 1:])


def delete_current_line(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    local_state.remove_line(curr_top + y)
    local_state.set_cursor(0, y)


def insert_new_line_below(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    curr_line = local_state.get_line(curr_top + y)

    new_line = (' ' * (len(curr_line) - len(curr_line.lstrip()))) + '\n'
    local_state.add_line(y + curr_top + 1, new_line)
    local_state.set_cursor(len(curr_line) - len(curr_line.lstrip()), y + 1)


def insert_new_line_above(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    curr_line = local_state.get_line(curr_top + y)

    new_line = (' ' * (len(curr_line) - len(curr_line.lstrip()))) + '\n'
    local_state.add_line(y + curr_top, new_line)
    local_state.set_cursor(len(curr_line) - len(curr_line.lstrip()), y)




def delete_text_char(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    curr_line = local_state.get_line(y + curr_top)

    if x > 0:
        local_state.set_line(curr_top + y, curr_line[:x - 1] + curr_line[x:])
        local_state.set_cursor(x - 1, y)
    # do not delete character on first line of page
    elif y > 0 or curr_top > 0:
        if curr_line == '\n':
            local_state.remove_line(curr_top + y)
            local_state.set_cursor(0, y - 1)
            cursor_logic.move_cursor_end_line(local_state)
        else:
            prev_line = local_state.get_line(y + curr_top - 1)
            local_state.remove_line(curr_top + y)
            # slice off new line + last character
            local_state.set_line(curr_top + y - 1, prev_line[:-1] + curr_line)
            local_state.set_cursor(len(prev_line) - 1, y - 1)


def delete_text_range(px, py, pt, nx, ny, nt, local_state):
    # final cursor location should be at fx, fy depending on which comes first
    fx, fy = ((px, py), (nx, ny))[(ny + nt) < (py + pt)]

    if py + pt == ny + nt:
        start, end = ((px, nx), (nx, px))[nx < px]
        curr_line = local_state.get_line(py + pt)
        local_state.set_line(py + pt, curr_line[:start] + curr_line[end:])
        local_state.set_cursor(start, py)
    else:
        start, end = ((py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
        count = 0
        for n in range(start, end + 1):
            if (n == py + pt) and (px, py) == (fx, fy):
                local_state.set_line(n, local_state.get_line(n)[:px] + '\n')
            elif (n  == py + pt) and (px, py) != (fx, fy):
                local_state.set_line(n, local_state.get_line(n)[px:])
            elif (n == ny + nt) and (nx, ny) == (fx, fy):
                local_state.set_line(n, local_state.get_line(n)[:nx] + '\n')
            elif (n == ny + nt) and (nx, ny) != (fx, fy):
                local_state.set_line(n, local_state.get_line(n)[nx:])
            else:
                count += 1

        for i in range(count):
            local_state.remove_line(start + 1)

        local_state.set_cursor(fx, fy)


def add_new_line_char(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    curr_line = local_state.get_line(y + curr_top)

    if curr_line[x] != '\n':
        local_state.set_line(y + curr_top, curr_line[:x] + '\n')
        local_state.add_line(y + curr_top + 1, curr_line[x:])

    local_state.set_cursor(0, y + 1)
