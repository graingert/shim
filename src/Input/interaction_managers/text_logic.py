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

    if x > 0:
        curr_line = instance.get_line(y + curr_top)
        instance.set_line(curr_top + y, curr_line[:x - 1] + curr_line[x:])
        instance.set_cursor(x - 1, y)
    # do not delete character on first line of page
    elif y > 0 or curr_top > 0:
        prev_line = instance.get_line(y + curr_top - 1)
        # slice off new line + last character
        instance.set_line(curr_top + y - 1, prev_line[:-2] + '\n')
        instance.set_cursor(x, y - 1)
        cursor_logic.move_cursor_end_line(instance)
