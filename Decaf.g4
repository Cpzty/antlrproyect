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

block: '{' (varDeclaration)* (statement)* '}';

statement: 'if' '(' expression ')' block ('else' block)?
         | 'while' '(' expression ')' block
         | 'return' (expression)? ';'
         | methodCall ';'
         | block
         | location '=' expression
         | (expression)? ';'
         ;


location: (ID | ID '[' expression ']') ('.' location)?;

expression: location
          | methodCall
          | literal
          |'(' expression ')'
          //| left_num=int_literal op=('*'|'/'|'%') right_num=int_literal
          //| left_num=int_literal op=('+'|'-') right_num=int_literal
          //| left_num=int_literal|methodCall|ID op=('*'|'/'|'%') right_num=int_literal|methodCall|ID
          //| left_num=int_literal|methodCall|ID op=('+'|'-') right_num=int_literal|methodCall|ID
          | int_literal | methodCall | ID op=('*'|'/'|'%') int_literal | methodCall | ID
          | int_literal | methodCall | ID op=('+'|'-') int_literal | methodCall | ID
          | left_rel=int_literal|ID rel_op right_rel=int_literal|ID
          | left_num=int_literal eq_op right_num=int_literal
          | left_num=int_literal|location eq_op right_num=int_literal|location
          | left_bool=bool_literal|ID eq_op right_bool=bool_literal|ID
          | left_char=char_literal|ID eq_op right_char=char_literal|ID
          | left_bool=bool_literal|ID cond_op right_bool=bool_literal|ID
          | '-' expression
          | '!' expression
          ;

methodCall :    ID '('  ')' | ID '(' arg1 ')' ;

arg1    :   arg2 | ;

arg2    :   (arg) (',' arg)* ;

arg: expression;

//op: arith_op1 | arith_op2 | rel_op | eq_op | cond_op;

arith_op1:  '*' | '/' | '%';

arith_op2: '+' | '-';

opcond: rel_op | eq_op;

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
