import cursor_logic


def insert_text_str(s, local_state):
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(curr_top + y)
    local_state.set_line(curr_top + y, curr_line[:x] + s + curr_line[x:])
    local_state.set_cursor(x + len(s), y)


def insert_text_strs(local_state, global_state):
    x, y, curr_top = local_state.get_page_state()
    paste_txt = global_state.get_copy_buffer()

    curr_line = local_state.get_line(curr_top + y)
    local_state.set_line(curr_top + y, curr_line[:x] + paste_txt[0].strip('\n') + curr_line[x:])
    for i in range(len(paste_txt) - 1):
        local_state.add_line(curr_top + y + i + 1, paste_txt[i + 1])


def delete_text_highlight(local_state):
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(curr_top + y)
    local_state.set_line(curr_top + y, curr_line[:x] + curr_line[x + 1:])


def delete_current_line(local_state):
    x, y, curr_top = local_state.get_page_state()
    local_state.remove_line(curr_top + y)
    local_state.set_cursor(0, y)


def insert_new_line_below(local_state):
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(curr_top + y)

    new_line = (' ' * (len(curr_line) - len(curr_line.lstrip()))) + '\n'
    local_state.add_line(y + curr_top + 1, new_line)
    local_state.set_cursor(len(curr_line) - len(curr_line.lstrip()), y + 1)


def insert_new_line_above(local_state):
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(curr_top + y)

    new_line = (' ' * (len(curr_line) - len(curr_line.lstrip()))) + '\n'
    local_state.add_line(y + curr_top, new_line)
    local_state.set_cursor(len(curr_line) - len(curr_line.lstrip()), y)

# TODO: LOOK AT THE MAGIC NUMBERS HERE
def shift_selection_right(local_state):
    px, py, pt = local_state.get_visual_anchors()
    nx, ny, nt = local_state.get_page_state()

    start, end = ((py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
    for n in range(start, end + 1):
        l = local_state.get_line(n)
        local_state.set_line(n, ' ' * 4 + l)


def shift_selection_left(local_state):
    px, py, pt = local_state.get_visual_anchors()
    nx, ny, nt = local_state.get_page_state()

    start, end = ((py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
    for n in range(start, end + 1):
        l = local_state.get_line(n)
        local_state.set_line(n, l[:4].strip() + l[4:])


def delete_text_char(local_state):
    x, y, curr_top = local_state.get_page_state()
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


def get_text_range(px, py, pt, nx, ny, nt, local_state):
    txt = []
    fx, fy = ((px, py), (nx, ny))[(ny + nt) < (py + pt)]

    if py + pt == ny + nt:
        start, end = ((px, nx), (nx, px))[nx < px]
        curr_line = local_state.get_line(py + pt)
        txt.append(curr_line[start:end + 1])
    else:
        start, end = ((py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
        count = 0
        for n in range(start, end + 1):
            if (n == py + pt) and (px, py) == (fx, fy):
                txt.append(local_state.get_line(n)[:px])
            elif (n  == py + pt) and (px, py) != (fx, fy):
                txt.append(local_state.get_line(n)[px:])
            elif (n == ny + nt) and (nx, ny) == (fx, fy):
                txt.append(local_state.get_line(n)[:nx])
            elif (n == ny + nt) and (nx, ny) != (fx, fy):
                txt.append(local_state.get_line(n)[nx:])
            else:
                txt.append(local_state.get_line(n))
    return txt



def add_new_line_char(local_state):
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(y + curr_top)

    #  this should be safe I think, no need to perform new line check because python string splicing doesn't toss index exceptions if curr_line[x] != '\n':
    local_state.set_line(y + curr_top, curr_line[:x] + '\n')
    local_state.add_line(y + curr_top + 1, curr_line[x:])

    local_state.set_cursor(0, y + 1)
