grammar Decaf;

compileUnit
    :   program EOF
    ;

program: 'class' 'Program' '{' (declaration)* '}';

declaration: structDeclaration | varDeclaration | methodDeclaration;

structDeclaration: 'struct' ID '{' (varDeclaration)* '}';

varDeclaration: varType ID ';' | varType ID '[' NUM ']' ';';

varType: 'int' | 'char' | 'boolean' | 'struct' ID | structDeclaration | 'void';

methodDeclaration : methodType ID '(' (parameter (',' parameter)*)* ')' block  ;

methodType: 'int' | 'char' | 'boolean' | 'void';

parameter: parameterType ID | parameterType ID '[' ']';

parameterType: 'int' | 'char' | 'boolean';

block: '{' (statement)*  '}';

statement: 'if' '(' expression ')' block ('else' block)?
        | 'while' '(' expression ')' block
        | 'return' (expression)? ';'
        | methodCall ';'
        | block
        | location '=' expression
        | (expression)? ';'
        | varDeclaration
         ;


location: (ID | ID '[' expression ']') ('.' location)?;

expression: location
          | methodCall
          | literal
          | left=expression op=('*'|'/'|'%') right=expression
          | left=expression op=('+'|'-') right=expression
          | left=expression opcond right=expression
          | '-' expression
          | '!' expression
          |'(' expression ')'
          ;

methodCall :    ID '('  ')' | ID '(' arg (',' arg)*  ')' ;


arg: expression;

//op: arith_op1 | arith_op2 | rel_op | eq_op | cond_op;

arith_op1:  '*' | '/' | '%';

arith_op2: '+' | '-';

opcond: rel_op | eq_op | cond_op;

rel_op: '<' | '>' | '<=' | '>=';

eq_op: '==' | '!=';

cond_op: '&&' | '||';

literal: int_literal | char_literal | bool_literal;

int_literal: NUM;

char_literal: '"' CHAR '"';

bool_literal: 'true' | 'false';

COMMENT:  '//' ~( '\r' | '\n' )* ->channel(HIDDEN);
ID: ([a-zA-Z] [a-zA-Z0-9]*);
NUM: [0-9]+ ;
CHAR: [a-zA-Z] ;
WS : [ \t\r\n\f | ' '| '\r' | '\n' | '\t']+  ->channel(HIDDEN);
