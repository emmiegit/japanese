from ply.lex import lex
from ply.yacc import yacc

from .types import *

# Tokenizer

tokens = (
    'NAME',
    'NUMBER',
)

literals = ['+', '/', '*', '~', '(', ')', '[', ']']

t_ignore = ' \t\n'
t_NAME = r'[a-zA-Z]([ ]*[\w\-]+)*'  # names, including spaces inside (e.g. "make a deal" or "fortune-telling")

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character: {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex()

# Parser

precedence = (
    ('left', '+'),
    ('left', '/'),
    ('left', '~'),
    ('left', '*'),
)

def p_expression_name(p):
    '''
    expression : NAME
    '''

    p[0] = p[1]

def p_expression_group(p):
    '''
    expression : '(' expression ')'
               | '[' expression ']'
    '''

    p[0] = p[2]

def p_expression_multiple(p):
    '''
    expression : NUMBER '*' expression
    '''

    p[0] = Multiplied(count=p[1], expression=p[3])

def p_expression_list(p):
    '''
    expression : list_horizontal
               | list_vertical
    '''

    p[0] = p[1]

def p_expression_within(p):
    '''
    expression : within
    '''

    p[0] = p[1]

def p_list_horizontal(p):
    '''
    list_horizontal : list_item '+' list_item
                    | list_item '+' list_horizontal
    '''

    p[0] = merge_lists(HorizontalList, p[1], p[3])

def p_list_vertical(p):
    '''
    list_vertical : list_item '/' list_item
                  | list_item '/' list_vertical
    '''

    p[0] = merge_lists(VerticalList, p[1], p[3])

def p_list_item_name(p):
    '''
    list_item : NAME
    '''

    p[0] = p[1]

def p_list_item_group(p):
    '''
    list_item : '(' expression ')'
              | '[' expression ']'
    '''

    p[0] = p[2]

def p_within(p):
    '''
    within : expression '~' expression
    '''

    p[0] = Within(outer=p[1], inner=p[3])

def p_error(p):
    print(f"Syntax error at {p.value!r}")

parser = yacc()
