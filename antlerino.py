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

#class ImpListener(DecafListener):
    #def enterMethodDeclaration(self, ctx):
        #print(ctx.methodType().getText() + ' ' + ctx.ID().getText())
        #current_scope.clear()
        #methods_table.append(ctx.methodType().getText())
        #set scope remove at exitMethod
        #current_scope.append(ctx.ID().getText())
        #print(methods_table)
    #def enterVarDeclaration(self, ctx):
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
        printer = DecafListener()
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
        pass
    else:
        #print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))
        #methods
        if rule_names[tree.getRuleIndex()] == 'methodDeclaration':
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
            params_list = tree.arg1().getText().split(",")
            #print('list of params ', params_list)
            #fetch params from params table
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
                symbols_table[tree.ID().getText(), current_scope[-1]] = [tree.varType().getText(), offset[0]]

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


        #asignacion
        elif rule_names[tree.getRuleIndex()] == 'statement':
            #check that void type methods dont return stuff

            if 'if' in tree.getText():
                print((tree.expression().getText()))
                #append dummies
                current_scope.append(current_scope[-1])
                if  type(eval(tree.expression().getText())) != bool:
                    print('expresion {} no se resuelve a booleano'.format(tree.expression().getText()))


            if 'while' in tree.getText():
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
                            #print(tree.expression())
                            int(tree.expression().getText())
                        except:
                            print('tipo de return no coincide para metodo {} de tipo {}'.format(current_scope[-1],methods_table[current_scope[-1]]))

                    elif methods_table[current_scope[-1]] == 'boolean':
                        if tree.expression().getText() != 'False' or tree.expression().getText() != 'True':
                            print('tipo de return no coincide para metodo {} de tipo {}'.format(current_scope[-1],methods_table[current_scope[-1]]))
            #print(tree.getText())
            if tree.location() != None:
                if (tree.location().getText(), current_scope[-1]) not in symbols_table:
                    print('variable {} referenciada antes de ser declarada en metodo {}\n'.format(tree.location().getText(), current_scope[-1]))
                else:
                    #print('wut ',tree.getText())
                    type_chek = symbols_table.get((tree.location().getText(), current_scope[-1]))
                    #print('typecheck ', type_chek[0])
                    try:
                        if type_chek[0] == 'int':
                            int(tree.expression().getText())
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
                                print('{} no es de tipo char para varialbe {}'.format(tree.expression().getText(), tree.location().getText()))



                    except:
                        print('asignacion de tipos distintos')
                #print(tree.location().getText())
                #print('valor: ', tree.expression().getText())

        elif rule_names[tree.getRuleIndex()] == 'parameter':
            if current_scope[-1] == 'main':
                print('parametro {} declarado ilegalmente en metodo main\n'.format(tree.ID().getText()))
            #print(tree.getText())

        #expresiones
        elif rule_names[tree.getRuleIndex()] == 'expression':
            if tree.expression() != []:
                ops = ['*', '/', '%', '+', '-']
                strx_expr = ''
                for indx, express in enumerate(tree.expression()):
                    #print('this one ',tree.expression()[indx].getText())
                    if any(char.isdigit() for char in tree.expression()[indx].getText()) != True and any(x in tree.expression()[indx].getText() for x in ops) != True:
                        print('{} no es de tipo int'.format(tree.expression()[indx].getText()))
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