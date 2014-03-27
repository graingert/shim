# an attempt to approximate of pygments parser runtime
from pygments import lex
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.token import Token
from color_config import options

import time

def determine_color(t):
    print t
    if t is Token.Name.Class or t is Token.Name.Function:
        return options['function_name_color']
    elif t is Token.Keyword:
        return options['keyword_color']
    elif t is Token.String or t is Token.Literal.String.Interpol:
        return options['string_color']
    elif t is Token.Comment:
        return options['comment_color']
    elif t is Token.Keyword.Namespace:
        return options['namespace_color']
    else:
        return options['text_color']


l = get_lexer_for_filename('test.c')
def parse(s, l):
    ret_list = []
    start = 0
    for token in lex(s, l):
        color = determine_color(token[0])
        ret_list.append((start, token[1], color))
        start += len(token[1])
    print ret_list


# time1 = time.time()
# parse('i', l)
# parse('im', l)
# parse('imp', l)
# parse('impo', l)
# parse('impor', l)
# parse('import', l)
# parse('import test from lol', l)
# parse('def wat(lolblah):', l)
# parse('for line in gg:', l)
# parse('for lin in gg:', l)
# parse('for li in gg:', l)
# parse('for l in gg:', l)
# time2 = time.time()
# print 'function took %0.3f ms' % ((time2-time1)*1000.0)


parse('static int A_is_a(int cur_c)', l)
