# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import codecs
import sys
import os

import ply.lex as lex

tokens = ["ID", "NUMBER", "PLUS", "MINUS", "TIMES", "DIVIDE", "ODD",
          "ASSIGN", "NE", "LT", "LTE", "GT", "GTE", "LPARENT", "RPARENT", "COMMA", "SEMMICOLON", "DOT",
          "LKEY", "RKEY"]

reservadas = [ "program","if", "else", "fi", "do",
               "until", "while", "read", "write",
              "float", "int", "bool", "not", "and", "or"]
tokens = tokens + reservadas

t_ignore = '\t| |\n'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_ODD = r'ODD'
t_ASSIGN = r'='
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMMICOLON = r';'
t_DOT = r'\.'
t_LKEY = r'\{'
t_RKEY = r'\}'

def t_NUMBER(t):
    r'\d'
    return t

def t_COMMENT(t):
    r'(\/\*.*\/\*)|(//.*\n)'
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if ( t.value in reservadas):
        print("T es reservada!!!! %s", t)
        t.value = t.value
        t.type = t.value
    return t

def t_error(t):
    print("caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    #for i in enumerate(sys.argv):
    print(sys.argv[1]);
    fp = codecs.open(sys.argv[1],"r","utf-8");
    cadena = fp.read()
    fp.close()
    analizador= lex.lex()
    analizador.input(cadena)
    while True:
        tok = analizador.token()
        if not tok:break
        print (tok)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
