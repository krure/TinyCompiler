from MyLexer import *
import ply.yacc as yacc
import sys


class Node:
    def __init__(self, tipo, children=None, leaf=None):
        self.tipo = tipo
        print('Construccion de nodo: '+tipo)

        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def other_name(self, level=0):
        print('\t' * level + repr(self.value))
        for child in self.children:
            child.other_name(level + 1)

    def __str__(self, level=0):

        ret = "\t" * level + repr(self.tipo) + "\n"
        #print(ret)
        #print('Numero de hijos en : '+self.tipo+': '+str(len(self.children)))
        for child in self.children:
       #     print('Tipo actual: '+self.tipo)
        #    print(ret)
       #     print("nivel actual : " + str(level))
            ret += child.__str__(level=level + 1)

        return ret

    def __repr__(self):
        return '<Representacion de nodo de arbol>'

#SintaxTree=Node('Program')

class MyParser:

    # CONSTRUCTOR
    def __init__(self,lexer):
        #print("Parser constructor called")
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer
 
    # DESTRUCTOR
    def __del__(self):
        print('Parser destructor called.')
 
 
    tokens = MyLexer.tokens

    class Expr: pass

    class BinOp(Expr):
        def __init__(self, left, op, right):
            self.type = "binop"
            self.left = left
            self.right = right
            self.op = op

    class Number(Expr):
        def __init__(self, value):
            self.type = "number"
            self.value = value



    # GRAMMAR START

    def p_programa(self, p):
        '''programa : PROGRAM LLAVEABRE lista_declaracion lista_sentencias LLAVECIERRA
                    | PROGRAM LLAVEABRE LLAVECIERRA
                    | PROGRAM LLAVEABRE lista_declaracion LLAVECIERRA'''
        print("programa")
        if (len(p)==5):
            print("Solo hay declaraciones")
            #p[0]=Node("Programa",[Node('lista-declaracion',[Node('Decla')]),Node('lista-sentencias')],None)#[Node('lista-declaracion',[Node('Decla')]),Node('lista-sentencias')]
            p[0]=Node('Programa',[p[3]])
        elif (len(p)==4):
            #p[0] = Node("Programa", [Node('lista-declaracion')], None)
            p[0]=p[3]
        #str(p)
        #print(p)
        pass

    def p_lista_declaracion(self, p):
        '''lista_declaracion :  declaracion
                                | declaracion lista_declaracion'''
        print("list-decl")
        p[0]=Node("Lista-decl",[p[1]])
        pass
    def p_declaracion(self, p):
        'declaracion : tipo lista_id PUNTOCOMA'
        p[0]=Node("declaracion",[p[1],p[2]])
        print("decl")
        pass

    def p_decl_err_pyc(self,p):
        'declaracion : tipo lista_id error'
        print("Error de Sintaxis: Falta ';' "+" en la linea:" +str(p.lineno(3)-1))
        pass
    def p_tipo(self, p):
        '''tipo : INT
		          | FLOAT
				  | BOOL'''
        #p[0]= Node('Tipo',[Node(p[1])])
        p[0] = Node('Tipo')
        print("tipo")
        pass
    def p_lista_id(self, p):
        '''lista_id : IDENTIFIER COMA IDENTIFIER
                    | IDENTIFIER'''
        print('Lista id')
        if(len(p)==3):
           # p[0] = Node('lista de identificadores', [Node(p[1]),Node(p[3])])
            p[0] = Node('lista de identificadores')
        else:
            #p[0]= Node('lista de identificadores',Node(p[1]))
            p[0] = Node('lista de identificadores')
        pass
    def p_lista_sentencias(self, p):
        '''lista_sentencias :  sentencia
                            | sentencia lista_sentencias'''
        print('List sentencia')
        if(len(p)==2):
            p[0]= Node('lista de sentencias',[p[1],p[2]])
        else:
            p[0]= Node('lista de sentencias',[p[1]])
        pass
    def p_sentencia(self, p):
        '''sentencia : seleccion 
					   | iteracion 
					   | repeticion 
					   | sent_read 
					   | sent_write 
					   | bloque 
					   | asignacion'''
        print('Sentencia')
        p[0]=Node('Sentencia',[p[1]],p[0])
        pass
    def p_seleccion(self, p):
        '''seleccion : IF LPAREN b_expresion RPAREN THEN bloque 
		             | IF LPAREN b_expresion RPAREN ELSE bloque FI
		             | IF LPAREN b_expresion RPAREN THEN bloque FI'''
        p[0]=Node('Seleccion',[p[1],p[3],p[6]],p[0])
        pass
    def p_iteracion(self, p):
        'iteracion : WHILE LPAREN b_expresion RPAREN THEN bloque'
        p[0]=Node('Iteracion',[p[1],p[3],p[6]],p[0])
        pass
    def p_repeticion(self, p):
        'repeticion : DO bloque UNTIL LPAREN b_expresion RPAREN PUNTOCOMA'
        p[0]=Node('repeticion',[p[2]],p[0])
        pass
    def p_sent_read(self, p):
        'sent_read : READ IDENTIFIER PUNTOCOMA'
        p[0]=Node('sent_read',[p[2]],p[0])
        pass
    def p_sent_write(self, p):
        'sent_write : WRITE b_expresion PUNTOCOMA'
        p[0] = Node('sent_write', [p[2]], p[0])
        pass
    def p_bloque(self, p):
        'bloque : LLAVEABRE lista_sentencias LLAVECIERRA'
        print('Bloque')
        p[0] = Node('bloque', [p[2]], p[0])
        pass
    def p_asignacion(self, p):
        'asignacion : IDENTIFIER IGUAL b_expresion PUNTOCOMA'
        #p[0]=p[1]=p[3]
        p[0]= Node('Asignacion',[p[1],p[3]],p[0])
        print("asignacion")
        pass
    def p_b_expresion(self, p):
        '''b_expresion : b_term OR b_term
                    | b_term'''
        if(len(p)==3):
            p[0] = Node('expresion', [p[1],p[3]], p[0])
        else:
            p[0]= Node('expresion',[p[1]])
        print("expre")
        pass
    def p_b_term(self, p):
        '''b_term : not_factor AND not_factor
                | not_factor'''
        if(len(p)==3):
            p[0] = Node('p_b_Term', [p[1],p[3]], p[0])
        else:
            p[0] = Node('p_b_term',[p[1]],p[0])
        pass
    def p_not_factor(self, p):
        '''not_factor : NOT b_factor
		                | b_factor'''
        if(len(p)==1):
            p[0] = Node('sent_read', [p[1]], p[0])
        else:
            p[0] = Node('p_not_factor',[])
        pass    
    def p_b_factor(self, p):
        '''b_factor :  LPAREN TRUE RPAREN
		               | LPAREN FALSE RPAREN   
		               | relacion'''
        p[0] = Node('p_b_factor', [p[2]], p[0])
        pass
    def p_relacion(self, p):
        '''relacion : expresion rel_Op expresion
		            | expresion'''

        pass
    def p_rel_Op(self, p):
        '''rel_Op : MENORIGUAL 
		           | MENOR
				   | MAYOR
				   | MAYORIGUAL 
				   | IGUALIGUAL 
				   | DIFERENTE '''
        pass
    def p_expresion(self,p):
        '''expresion : termino suma_Op termino
                        | termino'''

        if len(p)==4:
            p[0] = Node('Expresion',[p[1],p[2],p[3]],p[0])
        elif len(p)==2:
            p[0]= Node('Expresion',[p[1]],p[0])

    def p_suma_Op(self,p):
        '''suma_Op : PLUS 
		           | MINUS'''
        p[0] = Node('Suma_op', [p[1]], p[0])

        pass
    def p_termino(self,p):
        '''termino : signoFactor multi_Op signoFactor
                    | signoFactor'''
        if(len(p)==1):
            p[0] = Node('termino', [p[1]], p[0])
        else:
            p[0] = Node('sent_read', [p[1],p[2],p[3]], p[0])

        pass
    def p_multi_Op(self,p):
        '''multi_Op : TIMES 
		            | DIVIDE'''
        p[0] = Node('multi OP', [p[1]], p[0])
        pass
    def p_signoFactor(self,p):
        '''signoFactor : suma_Op factor
		               | factor'''
        if(len(p)==2):
            p[0] = Node('signo_factor', [p[1],p[2]], p[0])
        else:
            p[0] = Node('signoFactor',[p[1]],p[0])
        pass
    def p_factor(self,p):
       '''factor : LPAREN b_expresion RPAREN 
	   			   | NUMBER
	   			   | FLOATNUMBER
				   | IDENTIFIER'''
       if(p[1]=='('):
        p[0] = p[2]
       else:
        p[0]=p[1]
		
    def p_error(self,p):
        #print(f'ERROR SINTÁCTICO EN {p.value!r}')
      #  p[0]=p[1]
        pass