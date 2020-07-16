from graphviz import Digraph

g = Digraph('G', filename='tree.gv')

g.edge('program', 'declaration')
g.edge('declaration', 'methodDeclaration')
g.edge('methodDeclaration', 'methodType')
g.edge('methodDeclaration', 'block')
g.edge('block', 'statement')
g.edge('statement', 'expression')
g.edge('expression', 'expression1')
g.edge('expression', 'op')
g.edge('expression', 'expression2')
g.edge('expression1', 'literal')
g.edge('expression1', 'int_literal')
g.edge('op', 'arith_op')
g.edge('expression2', 'literal')
g.edge('expression2', 'int_literal')


g.view()