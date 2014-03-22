COMMAND_MAP = {
                  'dollar': '$',
                  'braceright': '}',
                  'braceleft': '{',
                  'bracketright': ']',
                  'bracketleft': '[',
                  'parenright': ')',
                  'parenleft': '(',
                  'colon': ':',
                  'semicolon': ';',
                  'bar': '|',
                  'greater': '>',
                  'less': '<',
                  'comma': ',',
                  'period': '.',
                  'slash': '/',
                  'question': '?',
                  'plus': '+',
                  'equal': '=',
                  'minus': '-',
                  'underscore': '_',
                  'exclam': '!',
                  'at': '@',
                  'percent': '%',
                  'asciicircum': '^',
                  'ampersand': '&',
                  'asterisk': '*',
                  'quoteright': "'",
                  'quotedbl': '"',
                  'BackSpace': 'BackSpace',
                  'Return': 'Return',
                  'space': ' '
               }


DEFAULT_MOVEMENTS = {
                        'h': 'move_cursor_left',
                        'j': 'move_cursor_down',
                        'k': 'move_cursor_up',
                        'l': 'move_cursor_right',
                        'G': 'move_cursor_end_file',
                        '$': 'move_cursor_end_line',
                        'gg': 'move_cursor_begin_file',
                        'e': 'move_cursor_next_word_end',
                        '}': 'move_cursor_next_paragraph',
                        '{': 'move_cursor_prev_paragraph',
                        '0': 'move_cursor_beginning_line',
                        'w': 'move_cursor_next_word_front',
                        'b': 'move_cursor_prev_word_front',
                        'x': 'delete_text_highlight'
                    }


BREAK_MOVEMENTS = {
                      'h': 'move_cursor_left',
                      'j': 'move_cursor_down',
                      'k': 'move_cursor_up',
                      'l': 'move_cursor_right',
                      'w': 'move_cursor_next_word_front',
                      'b': 'move_cursor_prev_word_front',
                      'x': 'delete_text_highlight'
                  }
