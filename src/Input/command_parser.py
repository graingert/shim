import re

def goto_line_num(s):
    ind = s.find('gg')
    if ind == 0:
        return 'move_cursor_begin_file'
    else:
        count = 'n' + s[:ind]
        return ':'.join([count, 'move_cursor_line_num'])

command_list = {
                   re.compile('[0-9]*gg'): goto_line_num
               }

def parse(s):
    for r, func in command_list.items():
        s_par = r.search(s)
        if bool(s_par):
            return goto_line_num(s_par.group())
    return None
