import ply.lex as lex
import ply.yacc as yacc
import sys


from MyLexer import *
from MyParser import *

myLex = MyLexer()
myPars = MyParser(myLex)

lex = myLex.lexer
parser = myPars.parser

myFile = open(sys.argv[1])

SintaxTree= parser.parse(myFile.read(),debug=True)
print("Termino de Análisis Sintáctico!!")
#print(SintaxTree)
#str(SintaxTree)
print(SintaxTree)
#other_name(SintaxTree)