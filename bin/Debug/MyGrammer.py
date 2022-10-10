from MyLexer import *
import ply.yacc as yacc
import sys
import re


class Node:
    def __init__(self, tipo, children=None,Simb=None):
        self.tipo = tipo
        #print('Construccion de nodo: ' + tipo)

        if children:
            self.children = children
        else:
            self.children = []
        self.Simb = Simb


    def imp(self):
        ret =  repr(self.tipo)
        return ret

    def __str__(self, level=0):

        ret = " | | " * level + repr(self.tipo) + "\n"
        print(ret)
        # print('Numero de hijos en : '+self.tipo+': '+str(len(self.children)))
        for child in self.children:
            #     print('Tipo actual: '+self.tipo)
            #    print(ret)
            #     print("nivel actual : " + str(level))
            ret += child.__str__(level=level + 1)

        return ret

    def __repr__(self):
        return '<Representacion de nodo de arbol>'

class Simb:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        print('Construccion de simbolo: ' + tipo)

        self.valor = valor
    def __str__(self):
        return "(Tipo: "+repr(self.tipo)+" , Valor: "+repr(self.valor)+" )"
    def __repr__(self):
        return "(Tipo: "+repr(self.tipo)+" , Valor: "+repr(self.valor)+" )"


#Variables; su valor y su tipo
TablaSimb = {}




class MyGrammer:

    # CONSTRUCTOR
    def __init__(self, lexer):
        # print("Parser constructor called")
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer

    # DESTRUCTOR
    def __del__(self):
        print('Parser destructor called.')

    tokens = MyLexer.tokens



    # GRAMMAR START

    def p_programa(self, p):
        '''programa : PROGRAM LLAVEABRE lista_declaracion lista_sentencias LLAVECIERRA
                    | PROGRAM LLAVEABRE LLAVECIERRA
                    | PROGRAM LLAVEABRE lista_declaracion LLAVECIERRA'''
        print("programa")
        if (len(p) == 5):
            print("Solo hay declaraciones")
            # p[0]=Node("Programa",[Node('lista-declaracion',[Node('Decla')]),Node('lista-sentencias')],None)#[Node('lista-declaracion',[Node('Decla')]),Node('lista-sentencias')]
            p[0] = Node('Programa', [p[3]])
        elif (len(p) == 4):
            # p[0] = Node("Programa", [Node('lista-declaracion')], None)
            p[0] = Node('Programa')
        else:
            p[0] = Node('Programa', [p[3], p[4]])

        # str(p)
        # print(p)
        pass

    def p_lista_declaracion(self, p):
        '''lista_declaracion :  declaracion
                                | declaracion lista_declaracion'''
        print("list-decl")
        if (len(p) == 2):
            p[0] = Node("Lista-decl", [p[1]])
        else:
            p[0] = Node("Lista-decl", [p[1], p[2]])
        pass

    def p_declaracion(self, p):
        'declaracion : tipo lista_id PUNTOCOMA'
        p[0] = Node("declaracion")
        listaid=re.split(',',p[2])
        for iden in listaid:
            TablaSimb[iden]=Simb(p[1])
        print("decl")
        pass

    def p_decl_err_pyc(self, p):
        'declaracion : tipo lista_id error'
        print("Error de Sintaxis: Falta ';' " + " en la linea:" + str(p.lineno(3) - 1))
        pass

    def p_tipo(self, p):
        '''tipo : INT
		          | FLOAT
				  | BOOL'''
        # p[0]= Node('Tipo',[Node(p[1])])
        p[0] = p[1]
        print("tipo")
        pass

    def p_lista_id(self, p):
        '''lista_id : IDENTIFIER COMA lista_id
                    | IDENTIFIER'''
        print('Lista id')
        if (len(p) == 4):
            # p[0] = Node('lista de identificadores', [Node(p[1]),Node(p[3])])
            #p[0] = Node(p[1] + "," + str(p[3]))
            p[0]=p[1]+p[2]+p[3]
            #print("Nodo lista-id: "+re.sub(r'("\n")|\'|\\|\"', ' ', p[0]) )
        else:
            # p[0]= Node('lista de identificadores',Node(p[1]))
            p[0] = p[1]
        pass

    def p_lista_sentencias(self, p):
        '''lista_sentencias :  sentencia
                            | sentencia lista_sentencias
                            | '''
        print('List sentencia')
        if (len(p) == 3):
            p[0] = Node('lista de sentencias', [p[1], p[2]])
        elif (len(p) == 2):
            p[0] = Node('lista de sentencias', [p[1]])
        else:
            p[0] = Node('Sin sentencias')
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
        p[0] = Node('Sentencia', [p[1]])
        pass

    def p_seleccion(self, p):
        '''seleccion : IF LPAREN b_expresion RPAREN THEN bloque
		             | IF LPAREN b_expresion RPAREN ELSE bloque FI
		             | IF LPAREN b_expresion RPAREN THEN bloque FI
		             '''
        p[0] = Node('Seleccion', [Node(p[1]), p[3], p[6]], p[0])
        pass

    def p_seleccion_error(self, p):
        '''seleccion : IF error'''
        # p[0] = Node('Seleccion', [p[1], p[3], p[6]], p[0])
        print("Error de Sintaxis: sentencia IF malformada; sintaxis correcta: IF (expresion) THEN {bloque} FI ")
        pass

    def p_iteracion(self, p):
        'iteracion : WHILE LPAREN b_expresion RPAREN THEN bloque'
        p[0] = Node('Iteracion', [Node(p[1]), p[3], p[6]], p[0])
        pass

    def p_repeticion(self, p):
        'repeticion : DO bloque UNTIL LPAREN b_expresion RPAREN PUNTOCOMA'
        p[0] = Node('repeticion', [p[2], Node(p[4]), p[5]])
        pass

    def p_sent_read(self, p):
        'sent_read : READ IDENTIFIER PUNTOCOMA'
        p[0] = Node('sent_read', [Node(p[2])], p[0])
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
        # p[0]=p[1]=p[3]
        p[0] = Node('Asignacion', [Node(p[1]), p[3]])

        TablaSimb[p[1]]=p[3]
        print("asignacion")
        pass

    def p_asignacion_error(self, p):
        'asignacion : IDENTIFIER IGUAL b_expresion error'
        # p[0]=p[1]=p[3]
        # p[0]= Node('Asignacion',[p[1],p[3]],p[0])
        print("Error de Sintaxis: Falta ';' despues de la asignacion")
        pass

    def p_b_expresion(self, p):
        '''b_expresion : b_term OR b_term
                    | b_term'''
        if (len(p) == 4):
            #p[0] = Node('b_expresion', [p[1], Node('Or'), p[3]])
            p[0]=Simb('booleano',p[1]|p[3])

        else:
            #p[0] = Node('b_expresion', [p[1]])
            p[0]=p[1]
        print("expre")
        pass

    def p_b_term(self, p):
        '''b_term : not_factor AND not_factor
                | not_factor'''
        if (len(p) == 4):
            #p[0] = Node('p_b_Term', [p[1], Node('And'), p[3]], p[0])
            p[0]=Simb('booleano',p[1]&p[3])
        else:
            #p[0] = Node('p_b_term', [p[1]], p[0])
            p[0]=p[1]
        pass

    def p_not_factor(self, p):
        '''not_factor : NOT b_factor
		                | b_factor'''
        if (len(p) == 3):
            #p[0] = Node('p_not_factor', [Node('Not'), p[1]], p[0])
            print('Negando')
            p[0]=Simb('booleano',not p[2])
        else:
           # p[0] = Node('p_not_factor', [p[1], p[2]])
            print("nada por aqui en not fact")
            p[0]=p[1]
        pass

    def p_b_factor(self, p):
        '''b_factor :  LPAREN TRUE RPAREN
		               | LPAREN FALSE RPAREN
		               | relacion'''
        if (len(p) == 4):
            #p[0] = Node('p_b_factor', [Node(p[1]), Node(p[2]), Node(p[3])])
            p[0]= Simb('booleano',p[2])
        else:
            #p[0] = Node('p_b_factor', [p[1]])
            p[0]=p[1]
        pass

    def p_relacion1(self, p):
        '''relacion : expresion MENORIGUAL expresion
		            '''
        p[0]=Simb('booleano',p[1]<=p[3])
        pass

    def p_relacion2(self, p):
        '''relacion : expresion MENOR expresion
                    '''
        #p[0]=p[1]<p[3]
        p[0] = Simb('booleano', p[1] < p[3])

    def p_relacion3(self, p):
        '''relacion : expresion MAYOR expresion
                   '''
        #p[0]=p[1]>p[3]
        p[0] = Simb('booleano', p[1].valor > p[3].valor)
        pass

    def p_relacion4(self, p):
        '''relacion : expresion MAYORIGUAL expresion
                    '''
       # p[0]=p[1]>=p[3]
        p[0] = Simb('booleano', p[1] >= p[3])
        pass

    def p_relacion5(self, p):
        '''relacion : expresion IGUALIGUAL expresion
                    '''
        #p[0]=p[1]==p[3]
        p[0] = Simb('booleano', p[1] == p[3])
        pass

    def p_relacion6(self, p):
        '''relacion : expresion DIFERENTE expresion
                    '''
        #p[0]=p[1]!=p[3]
        p[0] = Simb('booleano', p[1].valor != p[3].valor)
        pass
    def p_relacion7(self, p):
        '''relacion : expresion
                    '''

        p[0]=p[1]
        pass


    def p_expresionS(self, p):
        '''expresion : termino PLUS termino
                        '''
        if p[1].tipo=='Float' | p[3].tipo=='Float':
            p[0] = Simb('Float',p[1].valor+p[3].valor)
        else:
            p[0] = Simb('Int', p[1].valor+p[3].valor)
        pass

    def p_expresionR(self, p):
        '''expresion : termino MINUS termino
                        '''

        if p[1].tipo == 'Float' | p[3].tipo == 'Float':
            p[0] = Simb('Float', p[1].valor - p[3].valor)
        else:
            p[0] = Simb('Int', p[1].valor - p[3].valor)
        pass

    def p_expresiont(self, p):
        '''expresion : termino
                        '''
        p[0] = p[1]
        pass


    def p_terminoM(self, p):
        '''termino : signoFactor TIMES signoFactor
                    '''

        if p[1].tipo == 'Float' | p[3].tipo == 'Float':
            p[0] = Simb('Float', p[1].valor * p[3].valor)
        else:
            p[0] = Simb('Int', p[1].valor * p[3].valor)

        pass

    def p_terminoD(self, p):
        '''termino : signoFactor DIVIDE signoFactor
                    '''

        if p[1].tipo == 'Float' | p[3].tipo == 'Float':
            p[0] = Simb('Float', p[1] / p[3])
        elif isinstance(p[1].valor/p[3].valor,float) :
            p[0]= Simb('Float', p[1] / p[3])
        else:
            p[0] = Simb('Int', p[1] / p[3])

        pass

    def p_terminoSF(self, p):
        '''termino : signoFactor'''
        p[0]=p[1]
        pass



    def p_signoFactorP(self, p):
        '''signoFactor : PLUS factor
		               '''
        p[0]=p[2]
        pass

    def p_signoFactorN(self, p):
        '''signoFactor : MINUS factor
                       '''
        p[0]=-p[2]
        pass

    def p_signoFactor(self, p):
        '''signoFactor : factor'''
        p[0]=p[1]
        pass

    def p_factor(self, p):
        '''factor : LPAREN b_expresion RPAREN
                       | NUMBER
                       | FLOATNUMBER
                    '''
        if (p[1] == '('):
            p[0] = p[2]
        elif "." in p[1]:
            p[0] = Simb('Float',float(p[1]))
        else:
            p[0] = Simb('Int', int(p[1]))
        pass

    def p_factorID(self, p):
        '''factor : IDENTIFIER'''
        p[0]=TablaSimb[p[1]]
        pass

    def p_error(self, p):
        # print(f'ERROR SINTÁCTICO EN {p.value!r}')
        #  p[0]=p[1]
        pass