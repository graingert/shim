def insert_text_str(s, instance):
    curr_top = instance.get_curr_top()
    x, y = instance.get_cursor()
    curr_line = instance.get_line(y + curr_top)
    instance.set_line(curr_top + y, curr_line[:x] + s + curr_line[x:])
    instance.set_cursor(x + len(s), y)
