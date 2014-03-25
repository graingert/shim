from pygments import lex
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.token import Token
# TODO: JANKY DUPLICATE IMPORT
from color_config import options

class syntax_parser():
    # init by getting a lexer for file name
    def __init__(self, filename):
        self.lexer = get_lexer_for_filename(filename)

    def parse_string(self, s):
        start = 0
        ret_list = []
        for token in lex(s, self.lexer):
            color = self.determine_color(token[0])
            ret_list.append((start, token[1], color))
            start += len(token[1])
        return ret_list

    def determine_color(self, t):
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
