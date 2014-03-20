def move_cursor_beginning_line(instance):
    x, y = instance.get_cursor()
    instance.set_cursor(0, y)

def move_cursor_end_line(instance):
    x, y = instance.get_cursor()
    curr_top = instance.get_curr_top()
    curr_line = instance.get_line(y + curr_top)
    instance.set_cursor(len(curr_line) - 2, y)

def move_cursor_end_file(instance):
    x, y = instance.get_cursor()
    curr_top = instance.get_curr_top()
    # line num and curr top are both 1 indexed
    instance.set_curr_top(instance.get_line_num() - instance.get_line_height() - 2)
    instance.set_cursor(0, instance.get_line_height())


def move_cursor_begin_file(instance):
    instance.set_curr_top(0)
    x, y = instance.get_cursor()
    instance.set_cursor(0, 0)


def move_cursor_left(instance):
    x, y = instance.get_cursor()
    x = (0, x - 1)[x - 1 > 0]
    instance.set_cursor(x, y)


def move_cursor_line_num(n, instance):
    instance.set_curr_top(min(n - 1, instance.get_line_num() - 2))
    instance.set_cursor(0, 0)

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

    instance.set_cursor(x, y - 1)


def move_cursor_next_paragraph(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()

    for offset, line_num in enumerate(range(y + curr_top + 1, instance.get_line_num() - 1)):
        l = instance.get_line(line_num)
        # break if line is empty, does not mirror vim's behavior fully
        if l == '\n':
            return instance.set_cursor(0, y + offset + 1)

    instance.set_curr_top(instance.get_line_num() - instance.get_line_height() - 2)
    instance.set_cursor(0,  instance.get_line_height())


def move_cursor_prev_paragraph(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()

    for offset, line_num in enumerate(range(y + curr_top - 1, -1, -1)):
        l = instance.get_line(line_num)
        # break if line is empty, does not mirror vim's behavior fully
        if l == '\n':
            return instance.set_cursor(0, y - offset - 1)

    instance.set_curr_top(0)
    instance.set_cursor(0, 0)


def move_cursor_next_paragraph(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()

    for offset, line_num in enumerate(range(y + curr_top + 1, instance.get_line_num() - 1)):
        l = instance.get_line(line_num)
        # break if line is empty, does not mirror vim's behavior fully
        if l == '\n':
            return instance.set_cursor(0, y + offset + 1)

    instance.set_curr_top(instance.get_line_num() - instance.get_line_height() - 2)
    instance.set_cursor(0,  instance.get_line_height())



def move_cursor_down(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()

    try:
        next_line = instance.get_line(y + curr_top + 1)
        # last character is a new line
        x = min(x, len(next_line) - 2)
    except IndexError:
         pass
    # if curr line + 1 is < total line numbers then move cursor down
    if (curr_top + y + 1) < instance.get_line_num() - 1:
        instance.set_cursor(x, y + 1)


def move_cursor_next_word_front(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()
    accept_all = False

    # this is definitely not optimal... there must be a smarter way to do this.
    for index, char in enumerate((instance.get_line(y + curr_top)[x + 1:])):
        if (accept_all and char != ' ') or (char in ["'", '[', ']', '(', ')', '-', '+', '{', '}']):
            return instance.set_cursor(x + index + 1, y)
        elif char == ' ':
            accept_all = True

    for offset, line_num in enumerate(range(y + curr_top + 1, instance.get_line_num() - 1)):
        l = instance.get_line(line_num)
        for index, char in enumerate(l):
            if char != ' ':
                return instance.set_cursor(index, y + offset + 1)


def move_cursor_move_prev_word_front(instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()
    accept_all = False

    # Same as above, I'm pretty sure this can be cleaner.
    curr_str = instance.get_line(y + curr_top)
    for dx in range(x - 1, -1, -1):
        if (curr_str[dx] != ' ' and curr_str[dx - 1] == ' ') or (curr_str[dx] in ["'", '[', ']', '(', ')', '-', '+', '{', '}']):
            return instance.set_cursor(dx, y)
        elif (curr_str[dx] != ' ') and dx == 0:
            return instance.set_cursor(dx, y)

    for dy, line_num in enumerate(range(y + curr_top - 1, -1, -1)):
        curr_str = instance.get_line(line_num)
        for dx in range(len(curr_str) - 1, 0, -1):
            if (curr_str[dx] != ' ' and curr_str[dx - 1] == ' ') or (curr_str[dx] in ["'", '[', ']', '(', ')', '-', '+', '{', '}']):
                return instance.set_cursor(dx, y - dy - 1)
