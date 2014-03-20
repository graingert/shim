import re

def goto_line_num(s):
    ind = s.find('gg')
    if ind == 0:
        return 'move_cursor_begin_file'
    else:
        count = 'n' + s[:ind]
        return ':'.join([count, 'move_cursor_line_num'])


def seek_char(s):
    print ':'.join(['c' + s[1], 'move_cursor_seek_char'])
    # assumption is that the regex will only return a string of length 2, seems kind of reasonable
    return ':'.join(['c' + s[1], 'move_cursor_seek_char'])


command_list = {
                   re.compile('[0-9]*gg'): goto_line_num,
                   re.compile('f.'): seek_char
               }

def parse(s):
    for r, func in command_list.items():
        s_par = r.search(s)
        if bool(s_par):
            return func(s_par.group())
    return None
