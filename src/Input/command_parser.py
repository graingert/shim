import re, command_list

def goto_line_num(s):
    ind = s.find('gg')
    if ind == 0:
        return 'move_cursor_begin_file'
    else:
        count = 'n' + s[:ind]
        return ':'.join([count, 'move_cursor_line_num'])


def seek_char(s):
    # assumption is that the regex will only return a string of length 2, seems kind of reasonable
    return ':'.join(['c' + s[1], 'move_cursor_seek_char'])


def repeat_default_movement(s):
    n_arg = re.search('[0-9]*', s).group()
    return ':'.join(['r' + n_arg, command_list.DEFAULT_MOVEMENTS[s[len(n_arg):]]])


def delete_text_movement(s):
    return ':'.join(['s' + command_list.DEFAULT_MOVEMENTS[s[1:]], 'delete_text_movement'])


def delete_curr_line(s):
    return 'delete_curr_line'


COMMAND_MAP = {
                   re.compile('[0-9]*gg'): goto_line_num,
                   re.compile('f.'): seek_char,
                   re.compile('[0-9]+[h|j|k|l|\{|\}]'): repeat_default_movement,
                   re.compile('d[h|j|k|l|{|}|w|b|e]'): delete_text_movement,
                   re.compile('dd'): delete_curr_line
              }


def parse(s):
    for r, func in COMMAND_MAP.items():
        s_par = r.search(s)
        if bool(s_par):
            return func(s_par.group())
    return ''
