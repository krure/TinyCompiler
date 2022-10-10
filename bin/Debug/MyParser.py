from MyLexer import *
import ply.yacc as yacc
import sys


class Node:
    def __init__(self, tipo, children=None, leaf=None):
        self.tipo = tipo
       # print('Construccion de nodo: '+tipo)

        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def other_name(self, level=0):
        #print('\t' * level + repr(self.value))
        for child in self.children:
            child.other_name(level + 1)

    def __str__(self, level=0):

        ret = " | | " * level + repr(self.tipo) + "\n"
       # print(ret)
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
        f= open("SintaxErrors.txt","w")
        f.write("")
        f.close()
 
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
            p[0]=Node('Programa')
        else:
            p[0] = Node('Programa', [p[3],p[4]])

        #str(p)
        #print(p)
        pass

    def p_lista_declaracion(self, p):
        '''lista_declaracion :  declaracion
                                | declaracion lista_declaracion'''
        print("list-decl")
        if(len(p)==2):
            p[0]=Node("Lista-decl",[p[1]])
        else:
            p[0]=Node("Lista-decl",[p[1],p[2]])
        pass
    def p_declaracion(self, p):
        'declaracion : tipo lista_id PUNTOCOMA'
        p[0]=Node("declaracion",[p[1],p[2]])
        print("decl")
        pass

    def p_decl_err_pyc(self,p):
        'declaracion : tipo lista_id error'
        f = open("SintaxErrors.txt","a")
        f.write("Error de Sintaxis: Falta ';' "+" en la linea:" +str(p.lineno(3)-1))
        print("Error de Sintaxis: Falta ';' "+" en la linea:" +str(p.lineno(3)-1))
        pass
    def p_tipo(self, p):
        '''tipo : INT
		          | FLOAT
				  | BOOL'''
        #p[0]= Node('Tipo',[Node(p[1])])
        p[0] = Node(p[1])
        print("tipo")
        pass
    def p_lista_id(self, p):
        '''lista_id : IDENTIFIER COMA lista_id
                    | IDENTIFIER'''
        print('Lista id')
        if(len(p)==4):
           # p[0] = Node('lista de identificadores', [Node(p[1]),Node(p[3])])
            p[0] = Node(str(p[1])+str(p[2])+str(p[3]))
        else:
            #p[0]= Node('lista de identificadores',Node(p[1]))
            p[0] = Node(p[1])
        pass
    def p_lista_sentencias(self, p):
        '''lista_sentencias :  sentencia
                            | sentencia lista_sentencias
                            | '''
        print('List sentencia')
        if(len(p)==3):
            p[0]= Node('lista de sentencias',[p[1],p[2]])
        elif (len(p)==2):
            p[0]= Node('lista de sentencias',[p[1]])
        else:
            p[0]=Node('Sin sentencias')
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
        p[0]=Node('Sentencia',[p[1]])
        pass
    def p_seleccion(self, p):
        '''seleccion : IF LPAREN b_expresion RPAREN THEN bloque 
		             | IF LPAREN b_expresion RPAREN ELSE bloque FI
		             | IF LPAREN b_expresion RPAREN THEN bloque FI
		             '''
        p[0]=Node('Seleccion',[Node(p[1]),p[3],p[6]],p[0])
        pass

    def p_seleccion_error(self, p):
            '''seleccion : IF error'''
            #p[0] = Node('Seleccion', [p[1], p[3], p[6]], p[0])
            f = open("SintaxErrors.txt", "a")
            f.write("Error de Sintaxis: sentencia IF malformada; sintaxis correcta: IF (expresion) THEN {bloque} FI ")
            print("Error de Sintaxis: sentencia IF malformada; sintaxis correcta: IF (expresion) THEN {bloque} FI ")
            pass
    def p_iteracion(self, p):
        'iteracion : WHILE LPAREN b_expresion RPAREN THEN bloque'
        p[0]=Node('Iteracion',[Node(p[1]),p[3],p[6]],p[0])
        pass
    def p_repeticion(self, p):
        'repeticion : DO bloque UNTIL LPAREN b_expresion RPAREN PUNTOCOMA'
        p[0]=Node('repeticion',[p[2],Node(p[4]),p[5]])
        pass
    def p_sent_read(self, p):
        'sent_read : READ IDENTIFIER PUNTOCOMA'
        p[0]=Node('sent_read',[Node(p[2])],p[0])
        pass
    def p_sent_write(self, p):
        'sent_write : WRITE b_expresion PUNTOCOMA'
        p[0] = Node('sent_write', [Node(p[2])], p[0])
        pass
    def p_bloque(self, p):
        'bloque : LLAVEABRE lista_sentencias LLAVECIERRA'
        print('Bloque')
        p[0] = Node('bloque', [p[2]], p[0])
        pass
    def p_asignacion(self, p):
        'asignacion : IDENTIFIER IGUAL b_expresion PUNTOCOMA'
        #p[0]=p[1]=p[3]
        p[0]= Node('Asignacion',[Node(p[1]),p[3]])
        print("asignacion")
        pass

    def p_asignacion_error(self, p):
        'asignacion : IDENTIFIER IGUAL b_expresion error'
        #p[0]=p[1]=p[3]
        #p[0]= Node('Asignacion',[p[1],p[3]],p[0])
        print("Error de Sintaxis: Falta ';' despues de la asignacion")
        pass
    def p_b_expresion(self, p):
        '''b_expresion : b_term OR b_term
                    | b_term'''
        if(len(p)==4):
            p[0] = Node('b_expresion', [p[1],Node('Or'),p[3]])
        else:
            p[0]= Node('b_expresion',[p[1]])
        print("expre")
        pass
    def p_b_term(self, p):
        '''b_term : not_factor AND not_factor
                | not_factor'''
        if(len(p)==4):
            p[0] = Node('p_b_Term', [p[1] ,Node('And') , p[3]], p[0])
        else:
            p[0] = Node('p_b_term',[p[1]],p[0])
        pass
    def p_not_factor(self, p):
        '''not_factor : NOT b_factor
		                | b_factor'''
        if(len(p)==2):
            p[0] = Node('p_not_factor', [Node('Not'),p[1]], p[0])
        else:
            p[0] = Node('p_not_factor',[p[1],p[2]])
        pass    
    def p_b_factor(self, p):
        '''b_factor :  LPAREN TRUE RPAREN
		               | LPAREN FALSE RPAREN   
		               | relacion'''
        if(len(p)==4):
            p[0] = Node('p_b_factor', [Node(p[1]),Node(p[2]),Node(p[3])])
        else:
            p[0] = Node('p_b_factor', [p[1]])
        pass
    def p_relacion(self, p):
        '''relacion : expresion rel_Op expresion
		            | expresion'''
        if(len(p)==4):
            p[0]= Node('relacion',[p[1],p[2],p[3]])
        else:
            p[0]= Node('relacion',[p[1]])
        pass
    def p_rel_Op(self, p):
        '''rel_Op : MENORIGUAL 
		           | MENOR
				   | MAYOR
				   | MAYORIGUAL 
				   | IGUALIGUAL 
				   | DIFERENTE '''
        p[0]=Node(p[1])
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
        p[0] = Node('Suma_op', [Node(p[1])], p[0])

        pass
    def p_termino(self,p):
        '''termino : signoFactor multi_Op signoFactor
                    | signoFactor'''
        if(len(p)==2):
            p[0] = Node('termino', [p[1]], p[0])
        else:
            p[0] = Node('termino', [p[1],p[2],p[3]], p[0])

        pass
    def p_multi_Op(self,p):
        '''multi_Op : TIMES 
		            | DIVIDE'''
        p[0] = Node('multi OP', [Node(p[1])], p[0])
        pass
    def p_signoFactor(self,p):
        '''signoFactor : suma_Op factor
		               | factor'''
        if(len(p)==3):
            p[0] = Node('signo_factor', [p[1],p[2]], p[0])
        else:
            p[0] = Node('signoFactor',[p[1]])
        pass
    def p_factor(self,p):
       '''factor : LPAREN b_expresion RPAREN 
	   			   | NUMBER
	   			   | FLOATNUMBER
				   | IDENTIFIER'''
       if(p[1]=='('):
        p[0] = Node('Factor',[p[2]])
       else:
        p[0]=Node(p[1])
		
    def p_error(self,p):
        #print(f'ERROR SINTÁCTICO EN {p.value!r}')
      #  p[0]=p[1]
        pass