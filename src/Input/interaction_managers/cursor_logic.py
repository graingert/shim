def move_cursor_beginning_line(local_state):
    x, y = local_state.get_cursor()
    local_state.set_cursor(0, y)

def move_cursor_end_line(local_state):
    x, y = local_state.get_cursor()
    curr_top = local_state.get_curr_top()
    curr_line = local_state.get_line(y + curr_top)
    local_state.set_cursor(len(curr_line) - 2, y)


def move_cursor_past_end_line(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    curr_line = local_state.get_line(y + curr_top)
    local_state.set_cursor(len(curr_line) - 1, y)


def move_cursor_end_file(local_state):
    x, y = local_state.get_cursor()
    curr_top = local_state.get_curr_top()
    local_state.set_curr_top(max(0, local_state.get_line_num() - local_state.get_line_height() - 2))
    local_state.set_cursor(0, min(local_state.get_line_num() -2, local_state.get_line_height()))


def move_cursor_begin_file(local_state):
    local_state.set_curr_top(0)
    x, y = local_state.get_cursor()
    local_state.set_cursor(0, 0)


def move_cursor_left(local_state):
    x, y = local_state.get_cursor()
    x = (0, x - 1)[x - 1 > 0]
    local_state.set_cursor(x, y)


def move_cursor_line_num(n, local_state):
    total = local_state.get_line_num()
    per_page = local_state.get_line_height()
    if n > (total - per_page):
        if total < per_page:
            local_state.set_cursor(0, min(local_state.get_line_num() - 2, n - 1))
        else:
            local_state.set_cursor(0, min(local_state.get_line_num() - 2, per_page - (total - n - 1)))
            local_state.set_curr_top(max(0, total - per_page - 2))
    else:
        local_state.set_curr_top(max(0, min(n - 1, local_state.get_line_num() - 2)))
        local_state.set_cursor(0, 0)


def move_cursor_seek_char(c, local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()

    curr_line = local_state.get_line(y + curr_top)
    for offset, char, in enumerate(curr_line[x + 1:]):
        if char == c:
            local_state.set_cursor(x + offset + 1, y)
            break


def move_cursor_right(local_state):
    x, y = local_state.get_cursor()
    curr_top = local_state.get_curr_top()
    lines = local_state.get_lines()
    try:
        nxt_char = lines[curr_top + y][x + 1]
    except:
        nxt_char = '\n'
    x = (x, x + 1)[nxt_char != '\n']
    local_state.set_cursor(x, y)


def move_cursor_up(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()

    try:
        previous_line = local_state.get_line(y + curr_top - 1)
        # last character is a new line
        x = min(x, len(previous_line) - 2)
    except IndexError:
         pass

    local_state.set_cursor(x, y - 1)


def move_cursor_next_paragraph(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    accept_all = False

    for offset, line_num in enumerate(range(y + curr_top + 1, local_state.get_line_num() - 1)):
        l = local_state.get_line(line_num)
        if (l == '\n') and accept_all:
            return local_state.set_cursor(0, y + offset + 1)
        elif l != '\n':
            accept_all = True

    local_state.set_curr_top(max(0, local_state.get_line_num() - local_state.get_line_height() - 2))
    local_state.set_cursor(0,  min(local_state.get_line_num() - 2, local_state.get_line_height()))


def move_cursor_prev_paragraph(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    accept_all = False

    for offset, line_num in enumerate(range(y + curr_top - 1, -1, -1)):
        l = local_state.get_line(line_num)

        if l == '\n' and accept_all:
            return local_state.set_cursor(0, y - offset - 1)
        elif l != '\n':
            accept_all = True

    local_state.set_curr_top(0)
    local_state.set_cursor(0, 0)


def move_cursor_down(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()

    try:
        next_line = local_state.get_line(y + curr_top + 1)
        # last character is a new line
        x = min(x, len(next_line) - 2)
    except IndexError:
         pass
    # if curr line + 1 is < total line numbers then move cursor down
    if (curr_top + y + 1) < local_state.get_line_num() - 1:
        local_state.set_cursor(x, y + 1)


def move_cursor_next_word_front(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    accept_all = False

    # this is definitely not optimal... there must be a smarter way to do this.
    for index, char in enumerate((local_state.get_line(y + curr_top)[x + 1:])):
        if (accept_all and char != ' ') or (char in ["'", '[', ']', '(', ')', '-', '+', '{', '}']):
            return local_state.set_cursor(x + index + 1, y)
        elif char == ' ':
            accept_all = True

    for offset, line_num in enumerate(range(y + curr_top + 1, local_state.get_line_num() - 1)):
        l = local_state.get_line(line_num)
        for index, char in enumerate(l):
            if char != ' ':
                return local_state.set_cursor(index, y + offset + 1)


def move_cursor_move_prev_word_front(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    accept_all = False

    # Same as above, I'm pretty sure this can be cleaner.
    curr_str = local_state.get_line(y + curr_top)
    for dx in range(x - 1, -1, -1):
        if (curr_str[dx] != ' ' and curr_str[dx - 1] == ' ') or (curr_str[dx] in ["'", '[', ']', '(', ')', '-', '+', '{', '}']):
            return local_state.set_cursor(dx, y)
        elif (curr_str[dx] != ' ') and dx == 0:
            return local_state.set_cursor(dx, y)

    for dy, line_num in enumerate(range(y + curr_top - 1, -1, -1)):
        curr_str = local_state.get_line(line_num)
        for dx in range(len(curr_str) - 1, 0, -1):
            if (curr_str[dx] != ' ' and curr_str[dx - 1] == ' ') or (curr_str[dx] in ["'", '[', ']', '(', ')', '-', '+', '{', '}']):
                return local_state.set_cursor(dx, y - dy - 1)


def move_cursor_next_word_end(local_state):
    curr_top = local_state.get_curr_top()
    x, y = local_state.get_cursor()
    accept_all = False
    curr_str = local_state.get_line(curr_top + y)

    for dx in range(x + 2, len(curr_str) - 1):
        if (curr_str[dx] == ' ' and curr_str[dx - 1] != ' ') or (curr_str[dx] in ["'", '[', ']', '(', ')', '-', '+', '{', '}']):
            return local_state.set_cursor(dx - 1, y)

    for dy, line_num in enumerate(range(y + curr_top + 1, local_state.get_line_num() - 1)):
        curr_str = local_state.get_line(line_num)
        for dx in range(len(curr_str)):
            if (curr_str[dx] == ' ' and curr_str[dx - 1] != ' ') or (curr_str[dx] in ["'", '[', ']', '(', ')', '-', '+', '{', '}']):
                return local_state.set_cursor(dx - 1, y + dy + 1)
