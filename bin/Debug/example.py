import ply.lex as lex
import ply.yacc as yacc
import sys


from MyLexer import *
from MyParser import *

 
# create objects MY LEXER and MY PARSER
myLex = MyLexer()
myPars = MyParser(myLex)
 
lex = myLex.lexer
parser = myPars.parser
 
# reading INPUT FILE
 
myFile = open(sys.argv[1])
cadena = myFile.read()
myFile.close()

analizador =  myLex.lexer
analizador.input(cadena)
while True:
    print("analizando")
    tok = analizador.token()
    if not tok: break
    print(tok)


