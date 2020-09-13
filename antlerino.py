import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.tree.Trees import Trees
from copy import deepcopy
from lark.tree import pydot__tree_to_png

sys.path.insert(0, "D:/Documents/ultimo semestre/compiladores 2.0/antler project/gen")

from DecafLexer import DecafLexer
from DecafListener import DecafListener
from DecafParser import DecafParser

current_scope = ['global']
offset = [0]
#symbols tables
methods_table = dict()
symbols_table = dict()
types_table = dict()
params_table = dict()
#valores iniciales establecidos
types_table['int'] = 4
types_table['boolean'] = 1
types_table['char'] = 1

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

    def enterStructDeclaration(self, ctx):
        offset[0] = 0

    def exitStructDeclaration(self, ctx):
        offset[0] = 0

        #print()

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
        f = open('treegen.txt', 'w')
        f.write((Trees.toStringTree(tree, None, parser)))

        f.close()
        #printer = DecafListener()
        printer = ImpListener()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)

        #printer.enterVarDeclaration()
        #print(walker)
    else:
        print('Error : Expected a valid file')

def traverse(tree, rule_names, indent = 0):

    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        #print("{0}TOKEN='{1} '".format("  " * indent, tree.getText()))
        if tree.getText() == '}':
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
                                    #if (tree.location().getText(), current_scope[-1]) not in symbols_table:
                                        print('{} no es de tipo int'.format(tree.expression()[indx].getText()))
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

print('resulting params table: ', params_table)
print('resulting method table: ', methods_table)
print('resulting symbols table: ', symbols_table)
if 'main' not in methods_table:
    print('metodo main faltante')