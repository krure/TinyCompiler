import ply.lex as lex
import ply.yacc as yacc
import sys


from MyLexer import *
from MyGrammer import *

myLex = MyLexer()
myGram = MyGrammer(myLex)

lex = myLex.lexer
parser = myGram.parser

myFile = open(sys.argv[1])

GrammTree= parser.parse(myFile.read(),debug=True)
print("Término de Análisis Gramático!!")
#print(GrammTree)
#str(SintaxTree)
print(TablaSimb)
#other_name(SintaxTree)