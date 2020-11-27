import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.tree.Trees import Trees
from copy import deepcopy
from lark.tree import pydot__tree_to_png

sys.path.insert(0, "D:/Documents/ultimo semestre/compiladores 2.0/antler project/gen")
#sys.path.insert(0, "C:/Users/Usuario/Documents/Cris/compis2/antlrproyect/gen")


from DecafLexer import DecafLexer
from DecafListener import DecafListener
from DecafParser import DecafParser


class Conversion:

    # Constructor to initialize the class variables
    def __init__(self, capacity):
        self.top = -1
        self.capacity = capacity
        # This array is used a stack
        self.array = []
        # Precedence setting
        self.output = []
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

        # check if the stack is empty

    def isEmpty(self):
        return True if self.top == -1 else False

    # Return the value of the top of the stack
    def peek(self):
        return self.array[-1]

        # Pop the element from the stack

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"

    # Push the element to the stack
    def push(self, op):
        self.top += 1
        self.array.append(op)

        # A utility function to check is the given character

    # is operand
    def isOperand(self, ch):
        return ch.isalpha()

        # Check if the precedence of operator is strictly

    # less than top of stack or not
    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    # The main function that converts given infix expression
    # to postfix expression
    def infixToPostfix(self, exp):

        # Iterate over the expression for conversion
        for i in exp:
            # If the character is an operand,
            # add it to output
            if self.isOperand(i):
                self.output.append(i)

                # If the character is an '(', push it to stack
            elif i == '(':
                self.push(i)

                # If the scanned character is an ')', pop and
            # output from the stack until and '(' is found
            elif i == ')':
                while ((not self.isEmpty()) and self.peek() != '('):
                    a = self.pop()
                    self.output.append(a)
                if (not self.isEmpty() and self.peek() != '('):
                    return -1
                else:
                    self.pop()

                    # An operator is encountered
            else:
                while (not self.isEmpty() and self.notGreater(i)):
                    self.output.append(self.pop())
                self.push(i)

                # pop all the operator from the stack
        while not self.isEmpty():
            self.output.append(self.pop())


current_scope = ['global']
offset = [0]
#symbols tables
methods_table = dict()
symbols_table = dict()
types_table = dict()
params_table = dict()

#save offset for structs
structs_table = dict()

#valores iniciales establecidos
types_table['int'] = 4
types_table['boolean'] = 1
types_table['char'] = 1



###
#proyecto2
###
labels = []
#temporales = []
op_solve = []
validar_ops = []
#bloque donde se construye codigo intermedio
bloque_codigo_intermedio = []
current_scope_intermediate_code = ['global']

class Node():
    def __init__(self):
        self.data = ''
        self.value = None

    def assign_op(self, ops):
        self.value = self.data + ' = ' + ops

class Temps():
    def __init__(self):
        self.nodes = []
        self.current_node = 0
    def create_node(self):
        some_node = Node()
        #if self.current_node >= 3:
         #   self.current_node = 0
        some_node.data = 't' + str(self.current_node)
        self.current_node += 1
        return some_node


    def see_tree(self):
        for nod in self.nodes:
            #print('data: ', nod.data)
            print('value: ', nod.value)


temporales = Temps()


class Etiquetas():
    def __init__(self):
        self.nodes = []
        self.current_node = 0
    def create_node(self):
        some_node = Node()
        some_node.data = 'L' + str(self.current_node)
        self.current_node += 1
        return some_node


    def see_tree(self):
        for nod in self.nodes:
            #print('data: ', nod.data)
            print('value: ', nod.value)

etiquetas = Etiquetas()


class ImpListener(DecafListener):
    def enterMethodDeclaration(self, ctx):
        offset[0] = 0

        #current_scope.clear()
        #methods_table.append(ctx.methodType().getText())
        #set scope remove at exitMethod
        #current_scope.append(ctx.ID().getText())
        #print(methods_table)
    def exitMethodDeclaration(self, ctx):
        offset[0] = 0
        #bloque_codigo_intermedio.append('end func ' + ctx.ID().getText())

    def enterStructDeclaration(self, ctx):
        #methods_table[ctx.ID().getText()] = 'struct'
        offset[0] = 0

    def exitStructDeclaration(self, ctx):
        offset[0] = 0



    #def exitExpression(self, ctx):
        #print(ctx.getText())
     #   op_solve.append(ctx.getText())
      #  if len(op_solve[-1]) == 3:
       #     r1 =temporales.create_node()
        ##   temporales.nodes.append(r1)

        #pass
        #if ctx.left != None:
         #   print('left: ',ctx.left.getText())
        #if ctx.op != None:
         #   print(ctx.op.text)
        #if ctx.right != None:
         #   print('right: ',ctx.right.getText())




def parse(argv):
    if len(sys.argv) > 1:
        input = FileStream(argv[1]) #read the first argument as a filestream
        lexer = DecafLexer(input) #call your lexer
        stream = CommonTokenStream(lexer)
        #stream.fill()
        #print(stream.tokens)
        #tokencitos = ([token.text for token in stream.tokens])
        #print(tokencitos)
        parser = DecafParser(stream)
        tree = parser.program() #start from the parser rule, however should be changed to your entry rule for your specific grammar
        #pydot__tree_to_png(tree, "./tree.png")

        traverse(tree, parser.ruleNames)
        traverse_intermediate_code(tree, parser.ruleNames)

        f = open('treegen.txt', 'w')
        f.write((Trees.toStringTree(tree, None, parser)))

        f.close()
        #printer = DecafListener()
        printer = ImpListener()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)

        #print(walker)
    else:
        print('Error : Expected a valid file')


def traverse_intermediate_code(tree, rule_names, indent = 0):

    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        #print("{0}TOKEN='{1}'".format("  " * indent, tree.getText()))
        #current_scope_intermediate_code.pop()
        pass
    else:
        #print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))
        if rule_names[tree.getRuleIndex()] == 'statement':
            if tree.location() != None:
                #print('woop woop: ', tree.expression().getText())
                cadena = tree.expression().getText()
                #print('cadena: ', cadena)
                pofix = Conversion(len(cadena))
                pofix.infixToPostfix(cadena)
                cadena = pofix.output
                #remplazar variables en cadena
                for indx, item in enumerate(cadena):
                    #print(current_scope_intermediate_code)
                    replace_var_inscope = symbols_table.get((item, current_scope_intermediate_code[-1]),'')
                    replace_var_inglobal = symbols_table.get((item, 'global'),'')
                    if replace_var_inscope != '':
                        cadena[indx] = 'fp[' + str(list(symbols_table.keys()).index((item, current_scope_intermediate_code[-1]))) + ']'
                    elif replace_var_inglobal != '':
                        cadena[indx] = 'gp[' + str(list(symbols_table.keys()).index((item, 'global'))) + ']'

                operaciones = ['*', '/', '%', '+', '-']
                for indx, operand in enumerate(cadena):

                    if operand in operaciones:

                        if cadena[indx-1] not in operaciones and cadena[indx-2] not in operaciones:
                            new_temp = temporales.create_node()
                            new_temp.assign_op(cadena[indx-2] + operand + cadena[indx-1])
                            temporales.nodes.append(new_temp)
                            #print(new_temp.value)
                        elif cadena[indx-1] in operaciones:
                            new_temp = temporales.create_node()
                            new_temp.assign_op(temporales.nodes[-2].data + operand + temporales.nodes[-1].data)
                            #print(new_temp.value)
                            temporales.nodes.append(new_temp)
                        #si el anterior no es operacion pero el 2do si entonces anterior + label
                        else:
                            new_temp = temporales.create_node()
                            new_temp.assign_op(temporales.nodes[-1].data + operand + cadena[indx-1])
                            temporales.nodes.append(new_temp)
                for node in temporales.nodes:
                    bloque_codigo_intermedio.append(deepcopy(node))
                temporales.nodes.clear()

            elif 'if' in tree.getText():
                current_scope_intermediate_code.append(current_scope_intermediate_code[-1])
                if 'else' in tree.getText():
                    current_scope_intermediate_code.append(current_scope_intermediate_code[-1])

                    #inicializar
                    new_temp = temporales.create_node()
                    Label0 = etiquetas.create_node()
                    Label1 = etiquetas.create_node()
                    #####
                    #print('hey there we eat pizza: ',list(tree.expression().getText()))
                    new_temp.assign_op(tree.expression().getText())
                    new_condition = 'ifZ ' + new_temp.data + ' Goto ' + Label0.data
                    line2 = tree.block()[0].getText()[1:-1]
                    line3 = 'Goto ' + Label1.data
                    Label0.value = tree.block()[1].getText()[1:-1]
                    #print('l0: ', Label0.value)
                    #temporales.nodes.append(new_temp)
                    #etiquetas.nodes.append(Label0)
                    #etiquetas.nodes.append(Label1)
                    bloque_codigo_intermedio.append(new_temp.value)
                    bloque_codigo_intermedio.append(new_condition)
                    bloque_codigo_intermedio.append(line2)
                    bloque_codigo_intermedio.append(line3)
                    bloque_codigo_intermedio.append(Label0.value)
                    bloque_codigo_intermedio.append('endIF')

            elif 'while' in tree.getText():
                current_scope_intermediate_code.append(current_scope_intermediate_code[-1])
                new_temp = temporales.create_node()
                Label0 = etiquetas.create_node()
                Label1 = etiquetas.create_node()
                ###
                chain_convert = tree.expression().getText()
                if '<=' in chain_convert:
                    chain_convert = chain_convert.replace('<=', ' ')
                    chain_convert = chain_convert.split(' ')
                    for indx, item in enumerate(chain_convert):
                        # print(current_scope_intermediate_code)
                        replace_var_inscope = symbols_table.get((item, current_scope_intermediate_code[-1]), '')
                        replace_var_inglobal = symbols_table.get((item, 'global'), '')
                        if replace_var_inscope != '':
                            chain_convert[indx] = 'fp[' + str(list(symbols_table.keys()).index((item, current_scope_intermediate_code[-1]))) + ']'
                        elif replace_var_inglobal != '':
                            chain_convert[indx] = 'gp[' + str(list(symbols_table.keys()).index((item, 'global'))) + ']'
                    chain_convert.insert(1, '<=')
                    #print(chain_convert)
                    chain_join = ''
                    chain_join = chain_join.join(chain_convert)
                    #print(chain_join)
                ###
                new_temp.assign_op(chain_join)
                new_condition = 'ifZ ' + new_temp.data + ' Goto ' + Label1.data
                #done with only 1 var len
                l3chain = list(tree.block()[0].getText()[1:-1])
                for indx, item in enumerate(l3chain):
                    # print(current_scope_intermediate_code)
                    replace_var_inscope = symbols_table.get((item, current_scope_intermediate_code[-1]), '')
                    replace_var_inglobal = symbols_table.get((item, 'global'), '')
                    if replace_var_inscope != '':
                        l3chain[indx] = 'fp[' + str(
                            list(symbols_table.keys()).index((item, current_scope_intermediate_code[-1]))) + ']'
                    elif replace_var_inglobal != '':
                        l3chain[indx] = 'gp[' + str(list(symbols_table.keys()).index((item, 'global'))) + ']'
                l3join = ''
                l3join = l3join.join(l3chain)
                #print('l3: ', l3chain)

                line3 = l3join
                line4 = 'Goto ' + Label0.data
                bloque_codigo_intermedio.append(Label0.data)
                bloque_codigo_intermedio.append(new_temp.value)
                bloque_codigo_intermedio.append(new_condition)
                bloque_codigo_intermedio.append(line3)
                bloque_codigo_intermedio.append(line4)
                bloque_codigo_intermedio.append('endWhile')

        elif rule_names[tree.getRuleIndex()] == 'methodDeclaration' or rule_names[tree.getRuleIndex()] == 'struct':
            bloque_codigo_intermedio.append('begin func ' + tree.ID().getText()+ ':')

        if rule_names[tree.getRuleIndex()] == 'methodDeclaration':
            current_scope_intermediate_code.append(tree.ID().getText())


            #print(line2)
        for child in tree.children:
            traverse_intermediate_code(child, rule_names, indent + 1)



#proyecto1
def traverse(tree, rule_names, indent = 0):

    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        #print("{0}TOKEN='{1} '".format("  " * indent, tree.getText()))
        if tree.getText() == '}':
            #if in struct save struct length
            if methods_table.get(current_scope[-1]) == 'struct':
                #print('offset: ', offset[0])
                structs_table[current_scope[-1]] = offset[0]

            #pop scope
            current_scope.pop()
            offset[0] = 0
        pass
    else:
        #print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))
        #methods
        if rule_names[tree.getRuleIndex()] == 'methodDeclaration':
            #reset offset
            #offset[0] = 0
            #push scope
            current_scope.append(tree.ID().getText())
            #fill methods table
            methods_table[tree.ID().getText()] = tree.methodType().getText()

            if (tree.parameter()) != []:
                insert_params = []
                for indx, item in enumerate(tree.parameter()):
                    #print('hmmm: ', item.getText())
                    if 'int' in tree.parameter(indx).getText():
                        insert_params.append('int')
                    elif 'boolean' in tree.parameter(indx).getText():
                        insert_params.append('boolean')
                    elif 'char' in tree.parameter(indx).getText():
                        insert_params.append('char')
                params_table[tree.ID().getText()] = deepcopy(insert_params)
                #insert_params.clear()
                    #print(tree.parameter(indx).getText())
        elif rule_names[tree.getRuleIndex()] == 'methodCall':
            noargs = ['false']
            try:
                tree.arg1()
            except:
                noargs[0] = 'true'

            if noargs[0] == 'false' and  tree.arg1() != None:
                params_list = tree.arg1().getText().split(",")
                #print('list of params ', params_list)
                #fetch params from params table
                if params_list != ['']:
                    if tree.ID().getText() not in methods_table:
                        print('metodo {} no tiene return y fue llamado en {}'.format(tree.ID().getText(), current_scope[-1]))
                    else:
                        temp_params_table = params_table[tree.ID().getText()]
                        if len(params_list) != len(temp_params_table):
                            print('diferencia en cantidad de valores en llamada a metodo {} \n'.format(tree.ID().getText()))
                        else:
                            #check matching types
                            for indx, item in enumerate(params_list):
                            #check for ids first, no check simultaneously
                                    type_extract = symbols_table.get((item,current_scope[-1]))
                                    #print(tree.ID().getText())
                                    if type_extract != None and temp_params_table[indx] != type_extract[0]:
                                        print('mismatch entre {} y tipo {}'.format(temp_params_table[indx], type_extract[0]))
                                    #si entra aca es porque no es un ID
                                    elif type_extract != None and temp_params_table[indx] == type_extract[0]:
                                        pass
                                    else:
                                        if temp_params_table[indx] == 'int':
                                            if(len(item)==1):
                                                int(item)
                                            else:
                                                params_list[indx] = eval(item)
                                                print('expresion {} convertida a {} en llamada a metodo {}'.format(item,params_list[indx], tree.ID().getText()))
                                        elif temp_params_table[indx] == 'boolean':
                                            bool(item)

        #symbols table
        elif rule_names[tree.getRuleIndex()] == 'varDeclaration':
            #revisar que los arrays no se inicialicen con 0
            if (tree.NUM()) != None:
                if (tree.NUM().getText()) == '0':
                    print('array {} inicializado con valor 0'.format(tree.ID().getText()))
            #revisar que no este duplicada
            if (tree.ID().getText(), current_scope[-1]) not in symbols_table:
                #print('woah: ', tree.ID().getText())
                #print('var type: ', tree.varType().getText())
                remove_struct = tree.varType().getText()
                if 'struct' in remove_struct:
                    remove_struct = remove_struct[-1]

                    if remove_struct not in methods_table:
                        #print('run: ', methods_table)

                        print('variable {} utiliza struct {} no existente en metodo {}'.format(tree.ID().getText(), remove_struct, current_scope[-1]))
                    else:
                        #print('remstruct: ', remove_struct)
                        struct_offset = structs_table.get(remove_struct)
                        offset[0] = struct_offset
                        #symbols_table[tree.ID().getText(), current_scope[-1]] = [remove_struct, struct_offset]


                if (tree.NUM()) == None:
                    symbols_table[tree.ID().getText(), current_scope[-1]] = [remove_struct, offset[0]]

                else:
                    symbols_table[tree.ID().getText(), current_scope[-1]] = [remove_struct, offset[0], 'array']

                # update offset
                if tree.varType().getText() == 'int':
                    if tree.NUM() != None:
                        offset[0] = offset[0] + (4 * int(tree.NUM().getText()))
                        #print('offset', offset[0])
                    else:
                        #print('nope ', tree.getText())
                        offset[0] = offset[0] + 4

                elif tree.varType().getText() == 'char':
                    if tree.NUM() != None:
                        offset[0] = offset[0] + (1 * int(tree.NUM().getText()))
                    else:
                        offset[0] = offset[0] + 1

                # else boolean
                elif tree.varType().getText() == 'boolean':
                    if tree.NUM() != None:
                        offset[0] = offset[0] + (1 * int(tree.NUM().getText()))
                    else:
                        offset[0] = offset[0] + 1

            else:
                print('variable {} duplicada en metodo {}\n'.format(tree.ID().getText(), current_scope[-1]))


        #structs
        elif rule_names[tree.getRuleIndex()] == 'structDeclaration':
            #reset offset
            #offset[0] = 0
            #push the id as scope
            #print('oh nyo: ', tree.ID().getText())
            current_scope.append(tree.ID().getText())
            methods_table[tree.ID().getText()] = 'struct'
            #for var in tree.varDeclaration():
                #print(var.getText())

        #asignacion
        elif rule_names[tree.getRuleIndex()] == 'statement':
            #check that void type methods dont return stuff

            #rule 10
            bool_check = ['1','0','false','true', '<=', '>=', '<', '>', '!=', '==', '||', '&&']
            bool_flag = False
            if 'if' in tree.getText():
                #print('umm: ', (tree.expression().getText()))
                if_bool_check = tree.expression().getText()
                #print(if_bool_check)
                #print(len(if_bool_check))
                #check all
                for condicion in bool_check:
                    if condicion in if_bool_check:
                        bool_flag = True

                if bool_flag == False:
                    print('expresion: "{}" en if no se resuelve a booleano'.format(if_bool_check))
                #append dummies
                current_scope.append(current_scope[-1])
                #if  type(eval(tree.expression().getText())) != bool:
                 #   print('expresion {} no se resuelve a booleano'.format(tree.expression().getText()))

            if 'else' in tree.getText():
                current_scope.append(current_scope[-1])

            if 'while' in tree.getText():
                # print('umm: ', (tree.expression().getText()))
                while_bool_check = tree.expression().getText()
                # print(if_bool_check)
                # print(len(if_bool_check))
                # check all
                for condicion in bool_check:
                    if condicion in while_bool_check:
                        bool_flag = True

                if bool_flag == False:
                    print('expresion: "{}" en while no se resuelve a booleano'.format(while_bool_check))

                current_scope.append(current_scope[-1])

            if 'return' in tree.getText():
                #check expression
                #if tree.expression() != None:
                    #print('check this out ',tree.expression().getText())
                #void check
                if methods_table[current_scope[-1]] == 'void' and tree.expression() != None:
                    print('metodo {} de tipo void no puede tener valores de retorno'.format(current_scope[-1]))
                #check for matching method types to return statement
                elif methods_table[current_scope[-1]] != 'void' and tree.expression() != None:
                    #print(tree.expression().getText())
                    if methods_table[current_scope[-1]] == 'int':
                        try:
                            tree.expression().getText()
                            if len(tree.expression().getText())==1:
                                int(tree.expression().getText())
                        except:
                            print('tipo de return no coincide para metodo {} de tipo {}'.format(current_scope[-1],methods_table[current_scope[-1]]))

                    elif methods_table[current_scope[-1]] == 'boolean':
                        #print(tree.expression().getText())
                        if tree.expression().getText() != 'false' or tree.expression().getText() != 'true':
                            print('tipo de return no coincide para metodo {} de tipo {}'.format(current_scope[-1],methods_table[current_scope[-1]]))
            #print(tree.getText())
            if tree.location() != None:
                #check for methodcall with a type
                #if '(' in tree.expression().getText():
                check_for_method = tree.expression().getText()
                if methods_table.get(check_for_method) == 'void':
                    print('metodo {} de tipo void no puede ser llamado en asignacion'.format(tree.expression().getText()))

                #regla 9
                #print('rule9: ', tree.getText())
                #print(tree.location().getText())
                #print(tree.expression().getText())
                if '[' in tree.location().getText() and '.' not in tree.location().getText():
                    array_id = tree.location().getText()[:tree.location().getText().index('[')]
                    array_expr = tree.location().getText()[tree.location().getText().index('[')+1:tree.location().getText().index(']')]
                    #print('arrid: ', array_id)
                    #print('arrexpr: ', array_expr)
                    check_for_array = symbols_table.get((array_id, current_scope[-1]))
                    if len(check_for_array) < 3:
                        print('{} no es un array'.format(array_id))

                    #check that arrexper is of type int
                    check_for_int =  symbols_table.get((array_expr, current_scope[-1]))
                    if check_for_int != None:
                        if check_for_int[0] != 'int':
                            print('la expresion dentro del array {} no es de tipo int'.format(array_id))
                    else:
                        try:
                            int(array_expr)
                        except:
                            print('la expresion dentro del array {} no es un numero'.format(array_id))

                if (tree.location().getText(), current_scope[-1]) not in symbols_table and '.' not in tree.location().getText() and '[' not in tree.location().getText():
                    print('variable {} referenciada antes de ser declarada en metodo {}\n'.format(tree.location().getText(), current_scope[-1]))

                elif '.' in tree.location().getText():
                    pass
                    #print('br: ', tree.location().getText())

                elif '[' in tree.location().getText():
                    pass

                else:
                    type_chek = symbols_table.get((tree.location().getText(), current_scope[-1]))
                    #print('typecheck ', type_chek[0])
                    #print('leftvar: ', tree.location().getText())
                    #print('rightvar: ', tree.expression().getText())
                    leftvar = tree.location().getText()
                    rightvar = tree.expression().getText()

                    left_check = symbols_table.get((leftvar, current_scope[-1]))
                    right_check = symbols_table.get((rightvar, current_scope[-1]))
                    if left_check != None and right_check != None:
                        #print(left_check)
                        #print(right_check)
                        if left_check[0] != right_check[0]:
                            print('asignacion distinta en {}'.format(tree.getText()))
                    try:
                        if type_chek[0] == 'int':
                            if tree.expression().getText() != 'false' or tree.expression().getText() != 'true':
                                try:
                                  int(tree.expression().getText())
                                except:
                                    print('variable {} tipo int no coincide con {}'.format(tree.expression().getText()))
                            else:
                                print('tipo int no coincide con {}'.format(tree.expression().getText()))
                        elif type_chek[0] == 'boolean':
                            bool(tree.expression().getText())
                        elif type_chek[0] == 'char':
                            char_flag_int = [True]
                            char_flag_bool = [True]
                            try:
                                int(tree.expression().getText())
                                char_flag_int[0] = False
                            except:
                                pass

                            if tree.expression().getText() == 'True' or tree.expression().getText() == 'False':
                                char_flag_bool[0] = False

                            #try:
                             #   print(bool(tree.expression().getText()))
                             #   char_flag_bool[0] = False
                            #except:
                            #    pass
                            if char_flag_int[0] == False or char_flag_bool[0] == False:
                                print('{} no es de tipo char para variable {}'.format(tree.expression().getText(), tree.location().getText()))



                    except:
                        pass
                        #print('asignacion de tipos distintos')
                #print(tree.location().getText())
                #print('valor: ', tree.expression().getText())

        elif rule_names[tree.getRuleIndex()] == 'parameter':
            if current_scope[-1] == 'main':
                print('parametro {} declarado ilegalmente en metodo main\n'.format(tree.ID().getText()))
            #print(tree.getText())

        #expresiones
        elif rule_names[tree.getRuleIndex()] == 'expression':
            if tree.expression() != [] and tree.expression() != None:
                try:
                    #print('hey: ', tree.expression().getText())
                    tree.expression().getText()
                except:
                    #print('12: ',tree.getText())
                    #rule 11
                    ops = ['*', '/', '%', '+', '-', '<=', '>=', '<', '>' ]
                    #rule 12
                    #eq_ops = ['==', '!=']
                    strx_expr = ''
                    for indx, express in enumerate(tree.expression()):
                        #print('this one ',tree.expression()[indx].getText())
                        if any(char.isdigit() for char in tree.expression()[indx].getText()) != True and any(x in tree.expression()[indx].getText() for x in ops) != True:
                            if '==' not in tree.getText() and '!=' not in tree.getText() and '||' not in tree.getText() and '&&' not in tree.getText():
                                if '||' not in tree.getText() and '&&' not in tree.getText():
                                    #try:
                                        #print('int problem: ', tree.expression()[indx].getText())
                                    #except:
                                     #   pass
                                    if (tree.expression()[indx].getText(), current_scope[-1]) not in symbols_table and '(' not in tree.expression()[indx].getText():
                                        print('{} no es de tipo int'.format(tree.expression()[indx].getText()))

                                    elif '(' in tree.expression()[indx].getText():
                                        method_name = tree.expression()[indx].getText()[:-2]
                                        #print(methods_table)
                                        gettem_method = methods_table.get(method_name)
                                        #print('methType: ', gettem_method)
                                        if gettem_method == None:
                                            print('metodo {} aun no se ha declarado'.format(method_name))
                                        elif gettem_method != None:
                                            if gettem_method != 'int':
                                                print('metodo {} no es de tipo int'.format(method_name))

                            elif '!='  in tree.getText() or '=='  in tree.getText():
                                arr_split = tree.getText().split('!=')
                                if len(arr_split) == 1:
                                    arr_split = tree.getText().split('==')
                                #print('arrspl: ', arr_split)
                                checkvar1 = symbols_table.get((arr_split[0], current_scope[-1]))
                                checkvar2 = symbols_table.get((arr_split[1], current_scope[-1]))
                                if checkvar1 != None and checkvar2 != None:
                                    if checkvar1[0] != checkvar2[0]:
                                        print('mismatch de tipos para {}'.format(tree.getText()))
                            #rule 13
                            elif '||' in tree.getText() or '&&'  in tree.getText():

                                arr_split = tree.getText().split('||')
                                if len(arr_split) == 1:
                                    arr_split = tree.getText().split('&&')
                                #print('dim: ', arr_split)
                                bool_var1 = arr_split[0]
                                bool_var2 = arr_split[1]
                                if bool_var1  in ['true', 'false']:
                                    bool_var1 = 'boolean'
                                else:
                                    bool_var1 = symbols_table.get((arr_split[0], current_scope[-1]))


                                if bool_var2  in ['true', 'false']:
                                    bool_var2 = 'boolean'
                                else:
                                    bool_var2 = symbols_table.get((arr_split[1], current_scope[-1]))


                                if bool_var1 != bool_var2:
                                    print('{} uno de los dos lados no es booleano'.format(tree.getText()))
                                else:
                                    #print(' {} vs {}'.format(bool_var1, bool_var2))
                                    pass

                        #if any(x in tree.expression()[indx].getText() for x in ops):
                        #strx_expr = strx_expr + tree.expression()[indx].getText()
                        #print('wut', strx_expr)
                        #for op in ops:
                        #    strx_expr = strx_expr.replace(op, '')
                       # strx_expr = strx_expr.replace('(', '')
                      #  strx_expr = strx_expr.replace(')', '')

                    #try:
                      #  int(strx_expr)
                     #   print('ok', strx_expr)
                    #except:
                        #print('operaciones entre tipo distinto a int')

        for child in tree.children:
            traverse(child, rule_names, indent + 1)



parse(sys.argv)

bloque_codigo_intermedio.append('end func main')
#for block in bloque_codigo_intermedio:
 #   try:
  #      print(block.value)
   # except:
    #    try:
     #       print(block)
      #      if 'func' in bloque_codigo_intermedio[bloque_codigo_intermedio.index(block) + 1] and \
       #             bloque_codigo_intermedio[
        #                bloque_codigo_intermedio.index(block) + 1] != 'end func main':
         #       print('end func ' + bloque_codigo_intermedio[bloque_codigo_intermedio.index(block)].split()[-1][:-1])
        #except:
         #   pass
    #print('\n')

for block in bloque_codigo_intermedio:
    try:
        block.value
        if 't' not in bloque_codigo_intermedio[bloque_codigo_intermedio.index(block)-1].value[5:]:
            reutilizar = bloque_codigo_intermedio[bloque_codigo_intermedio.index(block)-1].value[5:]
            actual_reutilizar = bloque_codigo_intermedio[bloque_codigo_intermedio.index(block)-1].value[:2]
        if block.value[5:] == reutilizar:
            block.value = block.value[:5] + actual_reutilizar
    except:
        pass

#print again
for block in bloque_codigo_intermedio:
    try:
        print(block.value)
    except:
        try:
            print(block)
            if 'func' in bloque_codigo_intermedio[bloque_codigo_intermedio.index(block) + 1] and \
                    bloque_codigo_intermedio[
                        bloque_codigo_intermedio.index(block) + 1] != 'end func main':
                print('end func ' + bloque_codigo_intermedio[bloque_codigo_intermedio.index(block)].split()[-1][:-1])
        except:
            pass


print('resulting params table: ', params_table)
print('resulting method table: ', methods_table)
print('resulting symbols table: ', symbols_table)
print('resulting structs table: ', structs_table)
if 'main' not in methods_table:
    print('metodo main faltante')

for key in methods_table.keys():
    labels.append('Function ' + key + ':')

#print('labels: ', labels)
#temporales.see_tree()

nasm_build = []

#funciones
#
#ascii to integer function
sprintflf = "sprintLF:\n" \
            "    call    sprint\n" \
            "    push    eax\n" \
            "    mov     eax, 0Ah\n" \
            "    push    eax\n" \
            "    mov     eax, esp\n" \
            "    call    sprint\n" \
            "    pop     eax\n" \
            "    pop     eax\n" \
            "    ret"

sprint = "sprint:\n" \
         "    push    edx\n" \
         "    push    ecx\n" \
         "    push    ebx\n" \
         "    push    eax\n" \
         "    call    slen\n" \
         "    mov     edx, eax\n" \
         "    pop     eax\n" \
         "    mov     ecx, eax\n" \
         "    mov     ebx, 1\n" \
         "    mov     eax, 4\n" \
         "    int     80h\n" \
         "    pop     ebx\n" \
         "    pop     ecx\n" \
         "    pop     edx\n" \
         "    ret"

slen = "slen:\n" \
       "    push    ebx\n" \
       "    mov     ebx, eax"

nextchar = "nextchar:\n" \
           "    cmp     byte [eax], 0\n" \
           "    jz      finished\n" \
           "    inc     eax\n" \
           "    jmp     nextchar"

finished = "finished:\n" \
           "    sub     eax, ebx\n" \
           "    pop     ebx\n" \
           "    ret"


atoi = "atoi: \n" \
       "    push    ebx \n" \
       "    push    ecx\n" \
       "    push    edx\n" \
       "    push    esi\n" \
       "    mov     esi, eax\n" \
       "    mov     eax, 0\n" \
       "    mov     ecx, 0\n" \
       ".multiplyLoop: \n" \
       "    xor     ebx, ebx\n" \
       "    mov     bl, [esi+ecx]\n" \
       "    cmp     bl, 48\n" \
       "    jl      .finished\n" \
       "    cmp     bl, 57\n" \
       "    jg      .finished\n" \
       "    sub     bl, 48\n" \
       "    add     eax, ebx\n" \
       "    mov     ebx, 10\n" \
       "    mul     ebx\n" \
       "    inc     ecx\n" \
       "    jmp     .multiplyLoop\n" \
       ".finished:\n" \
       "    cmp     ecx, 0\n" \
       "    je      .restore\n" \
       "    mov     ebx, 10\n" \
       "    div     ebx\n" \
       ".restore:\n" \
       "    pop     esi\n" \
       "    pop     edx\n" \
       "    pop     ecx\n" \
       "    pop     ebx\n" \
       "    ret"


ack1 = "ack1:\n" \
       "    inc ebx\n" \
       "    mov     ecx, ebx\n" \
       "    add     ecx, 48\n" \
       "    push    ecx\n" \
       "    mov     ecx, esp\n" \
       "    call    sprintLF\n" \
       "    pop ecx\n" \
       "    ret"

ack2 = "ack2:\n" \
       "    dec eax    ;m-1\n" \
       "    mov ebx, 1 ;convertir n a 1\n" \
       "    call ackermann"

ack3 = "ack3: \n" \
       "mov edx, 0\n" \
       "dec eax\n" \
       "call ackermann"

quitfunc = "quit:\n" \
           "    mov     ebx, 0\n" \
           "    mov     eax, 1\n" \
           "    int     80h\n" \
           "    ret"

#funciones independientes
nasm_build.append(atoi)
nasm_build.append(sprintflf)
nasm_build.append(sprint)
nasm_build.append(slen)
nasm_build.append(nextchar)
nasm_build.append(finished)
nasm_build.append(quitfunc)
###
name = ''

all_funcs = list(methods_table.keys())
for func in all_funcs:
    if func != 'main':
        nasm_build.append(func + ':')
        if func == 'ackermann':
            name = 'ackermann'
            nasm_build.append('    cmp eax, 0')
            nasm_build.append('    je ack1')
            nasm_build.append('    cmp ebx, 0')
            nasm_build.append('    je ack2')
            nasm_build.append('    cmp edx, 1')
            nasm_build.append('    je ack3')
            nasm_build.append('    dec ebx')
            nasm_build.append('    mov edx, 1')
            nasm_build.append('    jmp ackermann')
            nasm_build.append(ack1)
            nasm_build.append(ack2)
            nasm_build.append(ack3)



text_section = 'SECTION .text'
start = 'global _start'
label_start = '_start:'
nasm_build.append(text_section)
nasm_build.append(start)
nasm_build.append(label_start)

if len(all_funcs)==1:
    name = 'factorial'
    #factorial
    nasm_build.append('    mov eax, 0') #i
    nasm_build.append('    mov ebx, 1') #f
    nasm_build.append('    mov ecx, 61') #num
    nasm_build.append('    call factorial')
    nasm_build.append('factorial:')
    nasm_build.append('    mul ebx') #multiplicacion siempre toma eax y el segundo registro
    nasm_build.append('    inc eax')
    nasm_build.append('    cmp eax, ecx') #compare i, num
    nasm_build.append('    jne factorial')
    nasm_build.append('    mov eax, ebx') #move f to eax to print
    #convertir entero a ascii
    nasm_build.append('    add    eax, 48')
    nasm_build.append('    push eax')
    nasm_build.append('    mov eax, esp')
    nasm_build.append('    call sprintLF') #problemas con la funcion de print hay que convertir de entero a ascii
    nasm_build.append('    pop eax')

if 'ackermann:' in nasm_build:
    nasm_build.append('    mov eax, 0')
    nasm_build.append('    mov ebx, 0')
    nasm_build.append('    call ackermann')
#print(nasm_build)
#quit
nasm_build.append('call quit')

data_section = 'SECTION .data'
nasm_build.append(data_section)
#agregar variables
msg1 = "msg1        db      'Ingresar cantidad de llamadas: ', 0h"
nasm_build.append(msg1)

#bss section for data input
bss_section = 'SECTION .bss'
sinput = 'sinput:   resb 255'

nasm_build.append(bss_section)
nasm_build.append(sinput)




f3 = open("proyecto3/" + name +'.txt','w')
for line in nasm_build:
    f3.write(line + '\n')
f3.close()