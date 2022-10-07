import ply.lex as lex
import ply.yacc as yacc
import sys
from ply.lex import TOKEN
 
class MyLexer():
 
 
    # CONSTRUCTOR
    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)
        self.lexer.begin('INITIAL')
 
    # DESTRUCTOR
    def __del__(self):
        print('Lexer destructor called.')
 
    # list of TOKENS
    tokens = [
	    'NUMBER',
	    'PLUS',
	    'MINUS',
 		'TIMES',
	    'DIVIDE',
	    'LPAREN',
	    'RPAREN',
	    'PUNTOCOMA',
	    'COMA',
	    'MENOR',
	    'MAYOR',
	    'MENORIGUAL',
	    'MAYORIGUAL',
	    'IGUALIGUAL',
	    'DIFERENTE',
	    'IGUAL',
	    'IDENTIFIER',
	    'RESERVADA',
	    'FLOATNUMBER',
	    'COMENTARIOSBLOQUE',
	    'COMENTARIOSLINEA',
		'IF',
		'WHILE',
		'DO',
		'READ',
		'WRITE',
		'NOT',
		'TRUE',
		'FALSE',
		'THEN',
		'UNTIL',
		'FI',
		'PROGRAM',
		'INT',
		'FLOAT',
		'BOOL',
		'AND',
		'OR',
		'ELSE',
		'LLAVEABRE',
		'LLAVECIERRA',
		'SEP'
	]

 
    # tokens DEFINITION
 
	# Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_PUNTOCOMA = r';'
    t_COMA = r','
    t_MENOR = r'<'
    t_MAYOR = r'>'
    t_MENORIGUAL = r'<='
    t_MAYORIGUAL = r'>='
    t_IGUALIGUAL = r'=='
    t_DIFERENTE = r'!='
    t_IGUAL = r'='
    t_IF = r'if'
    t_WHILE = r'while'
    t_DO = r'do'
    t_READ = r'read'
    t_WRITE = r'write'
    t_NOT = r'not'
    t_TRUE = r'true'
    t_FALSE = r'false'
    t_THEN = r'then'
    t_UNTIL = r'until'
    t_FI = r'fi'
    t_PROGRAM = r'program'
    t_INT = r'int'
    t_FLOAT = r'float'
    t_BOOL = r'bool'
    t_AND = r'and'
    t_OR = r'or'
    t_ELSE = r'else'
    t_LLAVEABRE = r'{'
    t_LLAVECIERRA = r'}'
    
    # A regular expression rule with some action code
    def t_COMENTARIOSBLOQUE(self, t):
        r'/[*]([^*]|([*][^/]))*[*]/'
        pass

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMENTARIOSLINEA(self,t):
        r'//[^\n]*'
        pass
	
    def t_RESERVADA(self, t):
        r'program|if|then|else|fi|do|until|while|read|write|float|int|bool|not|and|or'

        t.value = t.value.upper()
        t.type = t.value.upper()
        return t

    def t_NUMBER(self, t):
        r'\d+'
        return t

    def t_FLOATNUMBER(self,t):
        r'[0-9]*\.?[0-9]+'
        return t



    def t_IDENTIFIER(self,t):
        r'[a-zA-Z]([a-zA-Z]|[0-9])*'
        return t

    def t_SEP(self,t):
        r'\%'
        return t

    def t_nl(self,t):
        r'(\n|\r|\r\n)|\s|\t'
        pass

    # every symbol that doesn't match with almost one of the previous tokens is considered an error
    def t_error(self,t):
        r'.'
        print("ERROR:", t.value)
        return t